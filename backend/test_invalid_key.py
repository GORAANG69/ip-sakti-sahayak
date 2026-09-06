import os
from fastapi.testclient import TestClient

# Explicitly set invalid key to simulate broken / quota exceeded / invalid key
os.environ['GEMINI_API_KEY'] = 'invalid_key_test_xyz123'
os.environ['GEMINI_ENABLED'] = 'true'

from app.main import app

client = TestClient(app)

print("--- Testing with INVALID GEMINI_API_KEY ---")

# 1. Chat
print("1. Testing Chat with invalid key...")
res = client.post('/api/chat', json={
    "message": "What are the Section 3(p) implications for botanical formulations in India?",
    "jurisdiction": "India",
    "language": "English"
}, headers={"Authorization": "Bearer demo-token"})
assert res.status_code == 200, f"Chat returned {res.status_code}: {res.text}"
data = res.json()
assert 'error' not in data.get('answer', '').lower()
assert 'failed' not in data.get('answer', '').lower()
print("   Chat response successfully fell back cleanly! Answer preview:")
print("  ", data['answer'][:100], "...")

# 2. Analyze
print("2. Testing Analyze with invalid key...")
res = client.post('/api/analyze', json={
    "title": "Herbal Wound Healing Gel",
    "description": "Standardized Curcuma and Aloe formulation with low-temperature vacuum extraction.",
    "jurisdiction": "India"
}, headers={"Authorization": "Bearer demo-token"})
assert res.status_code == 200, f"Analyze returned {res.status_code}: {res.text}"
data = res.json()
for k in ['problem', 'limitations', 'solution', 'mechanism', 'novel', 'relationships', 'functional', 'advantages', 'differentiating']:
    assert k in data and len(data[k]) > 10
print("   Analyze successfully fell back to structured Formulation DNA!")
print("   Problem:", data['problem'][:80])

# 3. Two-Sided AI
print("3. Testing Two-Sided AI with invalid key...")
res = client.post('/api/two-sided', json={
    "title": "Herbal Wound Healing Gel",
    "description": "Standardized Curcuma and Aloe formulation with low-temperature vacuum extraction.",
    "jurisdiction": "India"
}, headers={"Authorization": "Bearer demo-token"})
assert res.status_code == 200, f"Two-sided returned {res.status_code}: {res.text}"
data = res.json()
assert len(data['innovator_side']) >= 3
assert len(data['ip_side']) >= 3
print("   Two-Sided AI successfully fell back to rich perspectives!")
print("   Innovator bullets:", len(data['innovator_side']), "IP bullets:", len(data['ip_side']))

# 4. Risk Radar
print("4. Testing Risk Radar with invalid key...")
res = client.post('/api/risk-radar', json={
    "title": "Herbal Wound Healing Gel",
    "description": "Standardized Curcuma and Aloe formulation with low-temperature vacuum extraction.",
    "jurisdiction": "India"
}, headers={"Authorization": "Bearer demo-token"})
assert res.status_code == 200, f"Risk Radar returned {res.status_code}: {res.text}"
data = res.json()
assert len(data['items']) == 6
for it in data['items']:
    assert it['level'] in ['Low', 'Medium', 'High', 'Needs Review']
    assert 'error' not in it['note'].lower()
print("   Risk Radar successfully returned clean dynamic assessments!")

print("\n>>> ALL TESTS WITH INVALID GEMINI_API_KEY PASSED WITH ZERO VISIBLE ERRORS! <<<")
