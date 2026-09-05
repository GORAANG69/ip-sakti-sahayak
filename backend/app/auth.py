import os, secrets
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()
DEMO_MODE=os.getenv('DEMO_MODE','true').lower()=='true'
pwd=CryptContext(schemes=['bcrypt'], deprecated='auto')
SESSIONS={}

def hash_password(value): return pwd.hash(value)
def verify_password(value, hashed): return pwd.verify(value, hashed)

def create_session(email):
    token=secrets.token_urlsafe(32)
    SESSIONS[token]={'email':email,'expires':datetime.now(timezone.utc)+timedelta(hours=12)}
    return token

def get_session(token):
    if not token: return None
    s=SESSIONS.get(token)
    if not s: return None
    if s['expires']<datetime.now(timezone.utc):
        SESSIONS.pop(token,None); return None
    return s

def delete_session(token):
    if token: SESSIONS.pop(token,None)
