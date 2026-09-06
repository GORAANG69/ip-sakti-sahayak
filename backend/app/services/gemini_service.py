import os, json
from dotenv import load_dotenv

load_dotenv()

def enabled():
    return os.getenv('GEMINI_ENABLED', 'true').lower() == 'true' and bool(os.getenv('GEMINI_API_KEY'))

def _get_client():
    from google import genai
    return genai.Client(api_key=os.environ['GEMINI_API_KEY'])

def generate_chat(message, jurisdiction, language, evidence):
    if not enabled():
        return None
    try:
        from google.genai import types
        client = _get_client()
        ev = '\n\n'.join(f"ID: {e['id']}\nTITLE: {e['title']}\nDOMAIN: {e.get('domain','')}\nCONTENT: {e['content']}" for e in evidence)
        prompt = f'''You are an evidence-grounded IP decision-support assistant for IP-SAKTI Sahayak.
Jurisdiction: {jurisdiction}
Language: {language}
Question: {message}

Retrieved Authoritative Evidence:
{ev}

Rules:
1. Provide an objective, insightful, and evidence-grounded response.
2. Use only supplied evidence and user-provided facts. Do not fabricate case citations or section numbers.
3. Cite only supplied IDs in citation_ids.
4. Return valid JSON only.

JSON Format:
{{
  "answer": "Clear, direct guidance string",
  "confidence": "high" or "medium" or "low",
  "citation_ids": ["id1", "id2"],
  "abstained": false,
  "reason": null or explanation if abstaining,
  "suggested_next_steps": ["step 1", "step 2", "step 3"]
}}'''
        res = client.models.generate_content(
            model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, response_mime_type='application/json')
        )
        data = json.loads(res.text)
        valid = {e['id'] for e in evidence}
        data['citation_ids'] = [x for x in data.get('citation_ids', []) if x in valid]
        return data
    except Exception:
        return None

# Backward compatibility alias
generate = generate_chat

def generate_dna(title, description, jurisdiction, evidence):
    if not enabled():
        return None
    try:
        from google.genai import types
        client = _get_client()
        ev_summary = '\n'.join(f"- {e['title']} ({e.get('domain','')})" for e in (evidence or [])[:4])
        prompt = f'''You are a senior patent attorney and innovation scientist specializing in Formulation DNA analysis.
Analyze the user's specific innovation description and decompose it into 9 structured Formulation DNA fields.

Innovation Title: {title}
Jurisdiction: {jurisdiction}
Innovation Description:
{description}

Context Evidence:
{ev_summary}

Rules:
1. Generate specific, grounded, and technically detailed statements derived from the user's actual text. Do NOT return generic placeholders.
2. Return a single JSON object containing EXACTLY these 9 string keys:
   - "problem": Specific technical problem or bottleneck being addressed.
   - "limitations": Shortcomings, instability, or failures of existing methods/formulations.
   - "solution": The core proposed solution, composite, or methodology.
   - "mechanism": Scientific, physical, or chemical mechanism of action.
   - "novel": Specific novel process parameters, ingredient ratios, or structural features.
   - "relationships": Key interdependent parameters (e.g. Parameter A <-> Parameter B <-> Effect).
   - "functional": Measurable performance characteristics, stability metrics, or functional yield.
   - "advantages": Tangible technical, operational, and commercial advantages.
   - "differentiating": The critical combination of factors distinguishing it from known prior art.
3. Output valid JSON only.
'''
        res = client.models.generate_content(
            model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, response_mime_type='application/json')
        )
        data = json.loads(res.text)
        req_keys = ['problem', 'limitations', 'solution', 'mechanism', 'novel', 'relationships', 'functional', 'advantages', 'differentiating']
        if all(k in data for k in req_keys):
            return data
        return None
    except Exception:
        return None

def generate_two_sided(title, description, dna, jurisdiction, evidence):
    if not enabled():
        return None
    try:
        from google.genai import types
        client = _get_client()
        prompt = f'''You are the IP-SAKTI Two-Sided AI analysis engine.
Provide two complementary perspectives for the given innovation:
1. Innovator side: Practical steps the inventor must take to refine, document, and validate their invention.
2. IP analysis side: Critical scrutiny, novelty examination, Section 3 statutory hurdles, prior-art boundaries, and claim drafting considerations.

Innovation Title: {title}
Jurisdiction: {jurisdiction}
Description: {description}
Formulation DNA Context: {json.dumps(dna) if dna else "None"}

Return JSON format:
{{
  "innovator_side": [
    "5 specific actionable bullet points for the innovator..."
  ],
  "ip_side": [
    "5 specific legal/patentability analysis bullet points under {jurisdiction} patent practice..."
  ]
}}
Output valid JSON only.'''
        res = client.models.generate_content(
            model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, response_mime_type='application/json')
        )
        data = json.loads(res.text)
        if isinstance(data.get('innovator_side'), list) and isinstance(data.get('ip_side'), list):
            return data
        return None
    except Exception:
        return None

def generate_risk_radar(title, description, dna, jurisdiction, evidence):
    if not enabled():
        return None
    try:
        from google.genai import types
        client = _get_client()
        prompt = f'''You are the IP-SAKTI IP Risk Radar evaluation engine.
Evaluate early-warning risks for the following innovation across 6 essential areas:
1. "Novelty / Prior Art"
2. "Traditional Knowledge"
3. "Regulatory"
4. "Biodiversity / ABS"
5. "Jurisdiction"
6. "Missing Evidence"

Innovation Title: {title}
Jurisdiction: {jurisdiction}
Description: {description}
Formulation DNA: {json.dumps(dna) if dna else "None"}

For each area, assess:
- "level": One of "Low", "Medium", "High", or "Needs Review".
- "note": 1-2 sentences of specific, actionable risk assessment based on the technology and {jurisdiction} statutory framework (e.g. mention Section 3(d)/3(e)/3(p), NBA Form 3, TKDL, FSSAI/AYUSH where relevant).

Return JSON format:
{{
  "items": [
    {{"area": "Novelty / Prior Art", "level": "...", "note": "..."}},
    {{"area": "Traditional Knowledge", "level": "...", "note": "..."}},
    {{"area": "Regulatory", "level": "...", "note": "..."}},
    {{"area": "Biodiversity / ABS", "level": "...", "note": "..."}},
    {{"area": "Jurisdiction", "level": "...", "note": "..."}},
    {{"area": "Missing Evidence", "level": "...", "note": "..."}}
  ]
}}
Output valid JSON only.'''
        res = client.models.generate_content(
            model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, response_mime_type='application/json')
        )
        data = json.loads(res.text)
        if isinstance(data.get('items'), list) and len(data['items']) == 6:
            return data
        return None
    except Exception:
        return None

def generate_pathway(title, description, dna, jurisdiction, stage, evidence):
    if not enabled():
        return None
    try:
        from google.genai import types
        client = _get_client()
        dna_ctx = json.dumps(dna) if dna else 'None'
        ev_summary = '\n'.join(f"- {e['title']} ({e.get('domain','')}): {e['content'][:120]}" for e in (evidence or [])[:4])
        prompt = f'''You are the IP-SAKTI Pathway guidance engine.
Generate practical, specific guidance for the "{stage}" stage of an IP journey for the following innovation.

Innovation Title: {title}
Jurisdiction: {jurisdiction}
Description: {description}
Formulation DNA: {dna_ctx}

Context Evidence:
{ev_summary}

Pathway Stage: {stage}

Instructions:
1. Return 3-4 focused guidance steps for this specific stage.
2. Each step must be directly relevant to the innovation's technology type (botanical/tech/general).
3. For {jurisdiction}, cite specific statutory sections, regulatory bodies, or official processes where relevant.
4. Return valid JSON only.

JSON Format:
{{
  "stage": "{stage}",
  "steps": [
    {{
      "title": "Step title (concise, action-oriented)",
      "guidance": "2-3 sentence specific guidance grounded in {jurisdiction} practice.",
      "checklist": ["Actionable item 1", "Actionable item 2", "Actionable item 3"],
      "references": ["Authority / Source 1", "Authority / Source 2"]
    }}
  ]
}}'''
        res = client.models.generate_content(
            model=os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.2, response_mime_type='application/json')
        )
        data = json.loads(res.text)
        if isinstance(data.get('steps'), list) and len(data['steps']) >= 1:
            return data
        return None
    except Exception:
        return None
