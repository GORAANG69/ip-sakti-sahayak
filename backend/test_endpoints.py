import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("1. Testing /api/health...")
res = client.get('/api/health')
assert res.status_code == 200, f"Health check failed: {res.text}"
print("   Health response:", res.json())

print("2. Testing /api/analyze...")
res = client.post('/api/analyze', json={
    "title": "Herbal Wound Healing Gel",
    "description": "A novel synergistic formulation of Curcuma longa and Aloe vera with enhanced stability and dissolution rate.",
    "jurisdiction": "India"
})
assert res.status_code == 200, f"Analyze failed: {res.text}"
data = res.json()
for k in ['problem', 'limitations', 'solution', 'mechanism', 'novel', 'relationships', 'functional', 'advantages', 'differentiating']:
    assert k in data, f"Missing key {k} in DNA"
print("   Analyze response keys:", list(data.keys()))
print("   Problem preview:", data['problem'][:60])

print("3. Testing /api/two-sided...")
res = client.post('/api/two-sided', json={
    "title": "Herbal Wound Healing Gel",
    "description": "A novel synergistic formulation of Curcuma longa and Aloe vera.",
    "jurisdiction": "India"
})
assert res.status_code == 200, f"Two-sided failed: {res.text}"
ts_data = res.json()
assert 'innovator_side' in ts_data and 'ip_side' in ts_data
assert len(ts_data['innovator_side']) >= 3
assert len(ts_data['ip_side']) >= 3
print("   Innovator bullets:", len(ts_data['innovator_side']), "IP bullets:", len(ts_data['ip_side']))

print("4. Testing /api/risk-radar...")
res = client.post('/api/risk-radar', json={
    "title": "Herbal Wound Healing Gel",
    "description": "A novel synergistic formulation of Curcuma longa and Aloe vera.",
    "jurisdiction": "India"
})
assert res.status_code == 200, f"Risk radar failed: {res.text}"
rr_data = res.json()
assert 'items' in rr_data and len(rr_data['items']) == 6
print("   Risk radar areas:", [x['area'] for x in rr_data['items']])

print("5. Testing /api/analyses (Save and List)...")
save_res = client.post('/api/analyses', json={
    "title": "Herbal Wound Healing Gel",
    "jurisdiction": "India",
    "dna": data
}, headers={"Authorization": "Bearer demo-token"})
assert save_res.status_code == 200, f"Save analysis failed: {save_res.text}"
saved_item = save_res.json()
assert saved_item['id'] > 0
print("   Saved analysis id:", saved_item['id'])

list_res = client.get('/api/analyses', headers={"Authorization": "Bearer demo-token"})
assert list_res.status_code == 200, f"List analyses failed: {list_res.text}"
analyses_list = list_res.json()
assert len(analyses_list) >= 1
print("   Found saved analyses:", len(analyses_list))

print("6. Testing /api/chat...")
chat_res = client.post('/api/chat', json={
    "message": "What are Section 3(p) implications for turmeric formulations in India?",
    "jurisdiction": "India",
    "language": "English"
}, headers={"Authorization": "Bearer demo-token"})
assert chat_res.status_code == 200, f"Chat failed: {chat_res.text}"
chat_data = chat_res.json()
assert 'answer' in chat_data and len(chat_data['answer']) > 20
print("   Chat response answer preview:", chat_data['answer'][:80])

print("ALL ENDPOINT TESTS PASSED SUCCESSFULLY!")
