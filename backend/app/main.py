from fastapi import FastAPI,HTTPException,Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .database import init_db,get_connection
from .auth import DEMO_MODE,create_session,get_session,delete_session,hash_password,verify_password
from .schemas import Credentials,ChatRequest,ChatResponse
from .data import retrieve
from .services.gemini_service import enabled,generate

load_dotenv(); init_db()
app=FastAPI(title='IP-SAKTI Sahayak API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

def user(authorization):
    token=authorization.replace('Bearer ','',1) if authorization else None
    s=get_session(token)
    if not s: raise HTTPException(401,'Session expired or not authenticated')
    return s,token

@app.get('/api/health')
def health():
    try:
        c=get_connection(); c.execute('SELECT 1'); c.close(); db='ok'
    except Exception: db='error'
    return {'status':'ok' if db=='ok' else 'degraded','database':db,'gemini':'enabled' if enabled() else 'fallback','demo_mode':DEMO_MODE}

@app.post('/api/auth/login')
def login(x:Credentials):
    email=x.email.strip().lower()
    if not email or not x.password: raise HTTPException(422,'Email/ID and password are required')
    c=get_connection(); row=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
    if DEMO_MODE:
        if not row:
            c.execute('INSERT INTO users(email,password_hash) VALUES (?,NULL)',(email,)); c.commit()
        c.close(); token=create_session(email)
        return {'ok':True,'token':token,'user':{'email':email,'demo':True}}
    if not row or not row['password_hash'] or not verify_password(x.password,row['password_hash']):
        c.close(); raise HTTPException(401,'Invalid credentials')
    c.close(); token=create_session(row['email'])
    return {'ok':True,'token':token,'user':{'email':row['email'],'demo':False}}

@app.post('/api/auth/register')
def register(x:Credentials):
    email=x.email.strip().lower()
    if not email or not x.password: raise HTTPException(422,'Email/ID and password are required')
    c=get_connection()
    if c.execute('SELECT 1 FROM users WHERE email=?',(email,)).fetchone():
        c.close(); raise HTTPException(409,'Account already exists')
    c.execute('INSERT INTO users(email,password_hash) VALUES (?,?)',(email,hash_password(x.password))); c.commit(); c.close()
    token=create_session(email); return {'ok':True,'token':token,'user':{'email':email,'demo':False}}

@app.get('/api/auth/me')
def me(authorization:str|None=Header(default=None)):
    s,_=user(authorization); return {'authenticated':True,'user':{'email':s['email'],'demo':DEMO_MODE}}

@app.post('/api/auth/logout')
def logout(authorization:str|None=Header(default=None)):
    token=authorization.replace('Bearer ','',1) if authorization else None; delete_session(token); return {'ok':True}

@app.get('/api/knowledge/search')
def search(q:str='',jurisdiction:str='India'):
    return {'results':retrieve(q,jurisdiction) if q.strip() else []}

@app.post('/api/chat',response_model=ChatResponse)
def chat(x:ChatRequest,authorization:str|None=Header(default=None)):
    user(authorization)
    ev=retrieve(x.message,x.jurisdiction)
    if not ev:
        msg="I don't have sufficient evidence in the current knowledge base to provide a reliable conclusion." if x.language.lower().startswith('en') else "Vartamaan knowledge base mein reliable conclusion ke liye paryapt evidence nahi hai."
        return ChatResponse(answer=msg,confidence='low',jurisdiction=x.jurisdiction,language=x.language,abstained=True,reason='No sufficiently relevant evidence was retrieved.',suggested_next_steps=['Add or verify an authoritative source relevant to the exact question.','Provide more technical detail about the innovation.'])
    ai=generate(x.message,x.jurisdiction,x.language,ev)
    if ai:
        cited=[e for e in ev if e['id'] in set(ai.get('citation_ids',[]))]
        return ChatResponse(answer=ai.get('answer','Insufficient evidence for a reliable conclusion.'),confidence=ai.get('confidence','medium'),jurisdiction=x.jurisdiction,language=x.language,citations=[{'id':e['id'],'title':e['title'],'url':e['source_url']} for e in cited],evidence=cited,abstained=bool(ai.get('abstained',False)),reason=ai.get('reason'),suggested_next_steps=ai.get('suggested_next_steps',[]))
    lead=ev[0]
    answer=f"Based on the available demo evidence, the most relevant area is {lead['domain']}. Evidence: {lead['content']} This is preliminary decision support; verify the current official source before relying on it."
    return ChatResponse(answer=answer,confidence='medium',jurisdiction=x.jurisdiction,language=x.language,citations=[{'id':lead['id'],'title':lead['title'],'url':lead['source_url']}],evidence=ev,suggested_next_steps=['Review the evidence source.','Add more technical facts for a narrower analysis.'])
