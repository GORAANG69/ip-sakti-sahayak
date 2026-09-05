from pathlib import Path
import json,re
DATA=Path(__file__).resolve().parent.parent/'data'/'knowledge.json'

def load_knowledge():
    return json.loads(DATA.read_text(encoding='utf-8'))

def retrieve(query,jurisdiction='India',limit=5):
    terms=set(re.findall(r'[a-zA-Z0-9]+',query.lower()))
    out=[]
    for r in load_knowledge():
        if jurisdiction.lower()=='india' and r['jurisdiction'] not in ('India','Both'): continue
        if jurisdiction.lower()=='international' and r['jurisdiction'] not in ('International','Both'): continue
        hay=' '.join([r['title'],r['domain'],r['content']]).lower()
        score=sum(1 for t in terms if len(t)>2 and t in hay)
        if score: out.append((score,r))
    out.sort(key=lambda x:x[0],reverse=True)
    return [r for _,r in out[:limit]]
