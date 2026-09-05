import os,json
from dotenv import load_dotenv
load_dotenv()

def enabled():
    return os.getenv('GEMINI_ENABLED','true').lower()=='true' and bool(os.getenv('GEMINI_API_KEY'))

def generate(message,jurisdiction,language,evidence):
    if not enabled(): return None
    try:
        from google import genai
        from google.genai import types
        client=genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        ev='\n\n'.join(f"ID:{e['id']}\nTITLE:{e['title']}\nCONTENT:{e['content']}" for e in evidence)
        prompt=f'''You are an evidence-grounded IP decision-support assistant.
Jurisdiction: {jurisdiction}
Language: {language}
Question: {message}
Evidence:
{ev}
Rules: use only supplied evidence and user-provided facts. Never invent laws, sections, cases, deadlines, fees, patent/trademark numbers, requirements, citations or URLs. Never claim final legal advice or guaranteed patentability. If evidence is insufficient, abstain. Cite only supplied IDs.
Return JSON: answer, confidence, citation_ids, abstained, reason, suggested_next_steps.'''
        res=client.models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-2.5-flash'),contents=prompt,config=types.GenerateContentConfig(temperature=0.15,response_mime_type='application/json'))
        data=json.loads(res.text)
        valid={e['id'] for e in evidence}
        data['citation_ids']=[x for x in data.get('citation_ids',[]) if x in valid]
        return data
    except Exception:
        return None
