from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_full_flow():
    # 1. Start session
    response = client.post("/api/start")
    assert response.status_code == 200
    data = response.json()
    print("START:", data)
    session_id = data["session_id"]
    
    # 2. Answer a few questions
    for _ in range(8):
        response = client.post("/api/answer", json={"session_id": session_id, "answer": "no"})
        data = response.json()
        print("ANSWER:", data)
        if "guess" in data:
            print("FINISHED with guess:", data["guess"])
            return
            
    print("Reached 8 questions. Disambiguation triggered:", data.get("is_disambiguation"))

if __name__ == "__main__":
    test_full_flow()
