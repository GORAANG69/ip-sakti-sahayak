import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_full_flow():
    print("=== STARTING FULL E2E API WALKTHROUGH ===")
    
    # 1. Health check
    res = requests.get(f"{BASE_URL}/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    print("1. Health check:", health_data)
    assert health_data["status"] == "ok"
    assert health_data["database"] == "ok"
    assert health_data["gemini"] in ["enabled", "fallback"]

    # 2. Login
    login_res = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"email": "judge@hackathon.com", "password": "judgepassword123"}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("2. Login successful, token received.")

    # 3. Analyze
    sample_title = "Adaptive Edge Computing & Anomaly Detection System"
    sample_desc = "A distributed edge-computing IoT sensor platform that dynamically balances real-time telemetry processing and anomaly detection using adaptive quantization algorithms. The architecture reduces wireless uplink bandwidth consumption by 65% while maintaining sub-50ms fault detection latency across variable network conditions without requiring constant cloud connectivity."
    
    analyze_res = requests.post(
        f"{BASE_URL}/api/analyze",
        headers=headers,
        json={"title": sample_title, "description": sample_desc, "jurisdiction": "India"}
    )
    assert analyze_res.status_code == 200, f"Analyze failed: {analyze_res.text}"
    dna = analyze_res.json()
    print("3. Analyze successful, 9 DNA fields returned:")
    for k in ['problem', 'limitations', 'solution', 'mechanism', 'novel', 'relationships', 'functional', 'advantages', 'differentiating']:
        assert k in dna and len(dna[k]) > 0, f"Missing or empty DNA field: {k}"
        print(f"   - {k}: {dna[k][:60]}...")

    # 4. Save analysis
    save_res = requests.post(
        f"{BASE_URL}/api/analyses",
        headers=headers,
        json={"title": sample_title, "jurisdiction": "India", "dna": dna}
    )
    assert save_res.status_code == 200, f"Save analysis failed: {save_res.text}"
    saved_record = save_res.json()
    print("4. Saved analysis record id:", saved_record.get("id"))

    # Verify list of analyses
    list_res = requests.get(f"{BASE_URL}/api/analyses", headers=headers)
    assert list_res.status_code == 200
    saved_list = list_res.json()
    assert any(a["title"] == sample_title for a in saved_list), "Saved analysis not found in list"
    print("   Verified saved analysis exists in /api/analyses list.")

    # 5. Two-Sided AI
    two_res = requests.post(
        f"{BASE_URL}/api/two-sided",
        headers=headers,
        json={"title": sample_title, "description": sample_desc, "dna": dna, "jurisdiction": "India"}
    )
    assert two_res.status_code == 200, f"Two-sided failed: {two_res.text}"
    two_data = two_res.json()
    assert "innovator_side" in two_data and len(two_data["innovator_side"]) >= 3
    assert "ip_side" in two_data and len(two_data["ip_side"]) >= 3
    print("5. Two-Sided AI perspectives returned:")
    print("   Innovator sample:", two_data["innovator_side"][0])
    print("   IP Examiner sample:", two_data["ip_side"][0])

    # 6. Risk Radar
    radar_res = requests.post(
        f"{BASE_URL}/api/risk-radar",
        headers=headers,
        json={"title": sample_title, "description": sample_desc, "dna": dna, "jurisdiction": "India"}
    )
    assert radar_res.status_code == 200, f"Risk radar failed: {radar_res.text}"
    radar_data = radar_res.json()
    assert "items" in radar_data and len(radar_data["items"]) >= 4
    print("6. IP Risk Radar items returned:")
    for item in radar_data["items"][:3]:
        print(f"   - {item['area']}: [{item['level']}] {item['note'][:60]}...")

    # 7. Pathway (all 7 stages)
    STAGES = [
        'Product Understanding',
        'Classification',
        'IP Considerations',
        'Regulatory Considerations',
        'Traditional Knowledge Check',
        'Biodiversity / ABS',
        'Recommended Next Steps'
    ]
    print("7. Testing all 7 Pathway stages:")
    for stage in STAGES:
        p_res = requests.post(
            f"{BASE_URL}/api/pathway",
            headers=headers,
            json={"title": sample_title, "description": sample_desc, "dna": dna, "jurisdiction": "India", "stage": stage}
        )
        assert p_res.status_code == 200, f"Pathway failed for stage {stage}: {p_res.text}"
        p_data = p_res.json()
        assert "steps" in p_data and len(p_data["steps"]) > 0
        step_first = p_data["steps"][0]
        assert "title" in step_first and "guidance" in step_first
        print(f"   ✓ Stage '{stage}' returned {len(p_data['steps'])} step(s)")

    # 8. Copilot Chat (asking multiple prompts)
    test_questions = [
        "What are the distinguishing elements of my innovation?",
        "What IP considerations should I investigate regarding Section 3 exclusions?",
        "Could traditional knowledge or prior art be relevant?"
    ]
    print("8. Testing Copilot chat with 3 prompts:")
    for q in test_questions:
        chat_res = requests.post(
            f"{BASE_URL}/api/chat",
            headers=headers,
            json={"message": q, "jurisdiction": "India", "language": "English"}
        )
        assert chat_res.status_code == 200, f"Chat failed for '{q}': {chat_res.text}"
        chat_data = chat_res.json()
        assert "answer" in chat_data and len(chat_data["answer"]) > 10
        print(f"   Q: {q}")
        print(f"   A: {chat_data['answer'][:100]}...")
        if chat_data.get("citations"):
            print(f"      Citations count: {len(chat_data['citations'])}")
        if chat_data.get("suggested_next_steps"):
            print(f"      Next steps count: {len(chat_data['suggested_next_steps'])}")

    print("\n>>> ALL E2E STEPS SUCCEEDED WITH ZERO FAILURES! <<<")

if __name__ == "__main__":
    test_full_flow()
