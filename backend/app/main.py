import json
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv

from .database import init_db, get_connection
from .auth import DEMO_MODE, create_session, get_session, delete_session, hash_password, verify_password
from .schemas import (
    Credentials, ChatRequest, ChatResponse,
    AnalyzeRequest, FormulationDNA,
    TwoSidedRequest, TwoSidedResponse,
    RiskRadarRequest, RiskRadarResponse,
    PathwayRequest, PathwayResponse,
    SaveAnalysisRequest, AnalysisRecord
)
from .data import retrieve
from .services.gemini_service import enabled, generate_chat, generate_dna, generate_two_sided, generate_risk_radar, generate_pathway
from .services.fallback_service import fallback_chat, fallback_dna, fallback_two_sided, fallback_risk_radar, fallback_pathway

load_dotenv(Path(__file__).resolve().parents[1] / '.env')
load_dotenv()
init_db()

app = FastAPI(title='IP-SAKTI Sahayak API', version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

def get_current_user(authorization: str | None = None):
    token = authorization.replace('Bearer ', '', 1).strip() if authorization else None
    s = get_session(token)
    if not s:
        raise HTTPException(401, 'Session expired or not authenticated')
    return s, token

def get_user_id(email: str) -> int:
    c = get_connection()
    row = c.execute('SELECT id FROM users WHERE email=?', (email.lower(),)).fetchone()
    if not row:
        c.execute('INSERT INTO users(email, password_hash) VALUES (?, NULL)', (email.lower(),))
        c.commit()
        row = c.execute('SELECT id FROM users WHERE email=?', (email.lower(),)).fetchone()
    c.close()
    return row['id']

@app.get('/api/health')
def health():
    try:
        c = get_connection()
        c.execute('SELECT 1')
        c.close()
        db = 'ok'
    except Exception:
        db = 'error'
    return {
        'status': 'ok' if db == 'ok' else 'degraded',
        'database': db,
        'gemini': 'enabled' if enabled() else 'fallback',
        'demo_mode': DEMO_MODE
    }

@app.post('/api/auth/login')
def login(x: Credentials):
    email = x.email.strip().lower()
    if not email or not x.password:
        raise HTTPException(422, 'Email/ID and password are required')
    c = get_connection()
    row = c.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
    if DEMO_MODE:
        if not row:
            c.execute('INSERT INTO users(email, password_hash) VALUES (?, NULL)', (email,))
            c.commit()
        c.close()
        token = create_session(email)
        return {'ok': True, 'token': token, 'user': {'email': email, 'demo': True}}
    if not row or not row['password_hash'] or not verify_password(x.password, row['password_hash']):
        c.close()
        raise HTTPException(401, 'Invalid credentials')
    c.close()
    token = create_session(row['email'])
    return {'ok': True, 'token': token, 'user': {'email': row['email'], 'demo': False}}

@app.post('/api/auth/register')
def register(x: Credentials):
    email = x.email.strip().lower()
    if not email or not x.password:
        raise HTTPException(422, 'Email/ID and password are required')
    c = get_connection()
    if c.execute('SELECT 1 FROM users WHERE email=?', (email,)).fetchone():
        c.close()
        raise HTTPException(409, 'Account already exists')
    c.execute('INSERT INTO users(email, password_hash) VALUES (?, ?)', (email, hash_password(x.password)))
    c.commit()
    c.close()
    token = create_session(email)
    return {'ok': True, 'token': token, 'user': {'email': email, 'demo': False}}

@app.get('/api/auth/me')
def me(authorization: str | None = Header(default=None)):
    s, _ = get_current_user(authorization)
    return {'authenticated': True, 'user': {'email': s['email'], 'demo': DEMO_MODE}}

@app.post('/api/auth/logout')
def logout(authorization: str | None = Header(default=None)):
    token = authorization.replace('Bearer ', '', 1).strip() if authorization else None
    delete_session(token)
    return {'ok': True}

@app.get('/api/knowledge/search')
def search(q: str = '', jurisdiction: str = 'India'):
    return {'results': retrieve(q, jurisdiction) if q.strip() else []}

@app.post('/api/chat', response_model=ChatResponse)
def chat(x: ChatRequest, authorization: str | None = Header(default=None)):
    get_current_user(authorization)
    ev = retrieve(x.message, x.jurisdiction)
    
    # Try Gemini generation
    try:
        ai = generate_chat(x.message, x.jurisdiction, x.language, ev)
        if ai:
            cited = [e for e in ev if e['id'] in set(ai.get('citation_ids', []))]
            return ChatResponse(
                answer=ai.get('answer', 'Based on available guidance, review the cited evidence.'),
                confidence=ai.get('confidence', 'medium'),
                jurisdiction=x.jurisdiction,
                language=x.language,
                citations=[{'id': e['id'], 'title': e['title'], 'url': e['source_url']} for e in cited],
                evidence=cited,
                abstained=bool(ai.get('abstained', False)),
                reason=ai.get('reason'),
                suggested_next_steps=ai.get('suggested_next_steps', [])
            )
    except Exception:
        pass
    
    # Graceful fallback: never returns an error
    fb = fallback_chat(x.message, x.jurisdiction, x.language, ev)
    return ChatResponse(**fb)

@app.post('/api/analyze', response_model=FormulationDNA)
def analyze(x: AnalyzeRequest, authorization: str | None = Header(default=None)):
    get_current_user(authorization)
    ev = retrieve(f"{x.title} {x.description}", x.jurisdiction)
    
    # Try Gemini generation
    try:
        ai_dna = generate_dna(x.title, x.description, x.jurisdiction, ev)
        if ai_dna:
            return FormulationDNA(**ai_dna)
    except Exception:
        pass
    
    # Graceful fallback
    fb = fallback_dna(x.title, x.description, x.jurisdiction, ev)
    return FormulationDNA(**fb)

@app.post('/api/two-sided', response_model=TwoSidedResponse)
def two_sided(x: TwoSidedRequest, authorization: str | None = Header(default=None)):
    get_current_user(authorization)
    ev = retrieve(f"{x.title} {x.description}", x.jurisdiction)
    
    # Try Gemini generation
    try:
        ai = generate_two_sided(x.title, x.description, x.dna, x.jurisdiction, ev)
        if ai:
            return TwoSidedResponse(**ai)
    except Exception:
        pass
    
    # Graceful fallback
    fb = fallback_two_sided(x.title, x.description, x.dna, x.jurisdiction)
    return TwoSidedResponse(**fb)

@app.post('/api/risk-radar', response_model=RiskRadarResponse)
def risk_radar(x: RiskRadarRequest, authorization: str | None = Header(default=None)):
    get_current_user(authorization)
    ev = retrieve(f"{x.title} {x.description}", x.jurisdiction)
    
    # Try Gemini generation
    try:
        ai = generate_risk_radar(x.title, x.description, x.dna, x.jurisdiction, ev)
        if ai:
            return RiskRadarResponse(**ai)
    except Exception:
        pass
    
    # Graceful fallback
    fb = fallback_risk_radar(x.title, x.description, x.dna, x.jurisdiction)
    return RiskRadarResponse(**fb)

@app.post('/api/pathway', response_model=PathwayResponse)
def pathway(x: PathwayRequest, authorization: str | None = Header(default=None)):
    get_current_user(authorization)
    ev = retrieve(f"{x.title} {x.description} {x.stage}", x.jurisdiction)

    # Try Gemini generation
    try:
        ai = generate_pathway(x.title, x.description, x.dna, x.jurisdiction, x.stage, ev)
        if ai and isinstance(ai.get('steps'), list) and len(ai['steps']) >= 1:
            return PathwayResponse(**ai)
    except Exception:
        pass

    # Graceful fallback
    fb = fallback_pathway(x.title, x.description, x.dna, x.jurisdiction, x.stage)
    return PathwayResponse(**fb)

@app.post('/api/analyses', response_model=AnalysisRecord)
def save_analysis(x: SaveAnalysisRequest, authorization: str | None = Header(default=None)):
    s, _ = get_current_user(authorization)
    uid = get_user_id(s['email'])
    c = get_connection()
    cur = c.cursor()
    cur.execute(
        'INSERT INTO analyses (user_id, title, jurisdiction, dna_json) VALUES (?, ?, ?, ?)',
        (uid, x.title, x.jurisdiction, json.dumps(x.dna))
    )
    c.commit()
    aid = cur.lastrowid
    row = c.execute('SELECT * FROM analyses WHERE id=?', (aid,)).fetchone()
    c.close()
    return AnalysisRecord(
        id=row['id'],
        title=row['title'],
        jurisdiction=row['jurisdiction'],
        dna=json.loads(row['dna_json']),
        created_at=str(row['created_at'])
    )

@app.get('/api/analyses', response_model=list[AnalysisRecord])
def list_analyses(authorization: str | None = Header(default=None)):
    s, _ = get_current_user(authorization)
    uid = get_user_id(s['email'])
    c = get_connection()
    rows = c.execute(
        'SELECT * FROM analyses WHERE user_id=? ORDER BY created_at DESC',
        (uid,)
    ).fetchall()
    c.close()
    out = []
    for r in rows:
        try:
            d = json.loads(r['dna_json'])
        except Exception:
            d = {}
        out.append(AnalysisRecord(
            id=r['id'],
            title=r['title'],
            jurisdiction=r['jurisdiction'],
            dna=d,
            created_at=str(r['created_at'])
        ))
    return out

@app.delete('/api/analyses/{analysis_id}')
def delete_analysis(analysis_id: int, authorization: str | None = Header(default=None)):
    s, _ = get_current_user(authorization)
    uid = get_user_id(s['email'])
    c = get_connection()
    row = c.execute('SELECT * FROM analyses WHERE id=?', (analysis_id,)).fetchone()
    if not row:
        c.close()
        raise HTTPException(404, 'Analysis not found')
    if row['user_id'] != uid:
        c.close()
        raise HTTPException(403, 'Permission denied')
    c.execute('DELETE FROM analyses WHERE id=?', (analysis_id,))
    c.commit()
    c.close()
    return {'ok': True}
