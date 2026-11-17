import os
import sys
import time
import requests
from dotenv import load_dotenv

# Load env from parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

BASE_URL = "http://localhost:8000/api"

def run_integration_test():
    print("🚀 Starting multiplayer Battle Mode integration test...")
    
    # 1. Host creates a room
    print("\n--- Step 1: Host creates a room ---")
    host_resp = requests.post(f"{BASE_URL}/battle/create", json={
        "host_username": "TestHost"
    })
    if host_resp.status_code != 200:
        print(f"❌ Failed to create room. Status: {host_resp.status_code}, Body: {host_resp.text}")
        sys.exit(1)
        
    room_info = host_resp.json()
    room_code = room_info.get("room_code")
    print(f"✅ Host created room successfully! Code: {room_code}")
    
    # 2. Guest joins the room
    print("\n--- Step 2: Guest joins the room ---")
    guest_resp = requests.post(f"{BASE_URL}/battle/join", json={
        "room_code": room_code,
        "guest_username": "TestGuest"
    })
    if guest_resp.status_code != 200:
        print(f"❌ Failed to join room. Status: {guest_resp.status_code}, Body: {guest_resp.text}")
        sys.exit(1)
        
    room_state = guest_resp.json()
    print(f"✅ Guest joined room successfully! Status: {room_state.get('status')}")
    
    if room_state.get("status") != "countdown":
        print(f"❌ Room status should be 'countdown', got: {room_state.get('status')}")
        sys.exit(1)
        
    # 3. Start first round
    print("\n--- Step 3: Triggering start_round ---")
    start_resp = requests.post(f"{BASE_URL}/battle/start_round", json={
        "room_code": room_code
    })
    if start_resp.status_code != 200:
        print(f"❌ Failed to start round. Status: {start_resp.status_code}, Body: {start_resp.text}")
        sys.exit(1)
        
    room_state = start_resp.json()
    print(f"✅ Round 1 started! Status: {room_state.get('status')}")
    
    # 4. Play all rounds (1 to 10)
    print("\n--- Step 4: Playing all rounds ---")
    total_rounds = room_state.get("total_rounds", 10)
    
    for round_num in range(1, total_rounds + 1):
        print(f"\n🎮 ROUND {round_num} / {total_rounds}")
        
        # Verify status is active
        room_resp = requests.get(f"{BASE_URL}/battle/room/{room_code}")
        room_state = room_resp.json()
        if room_state.get("status") != "active":
            print(f"❌ Room status should be 'active' for round play, got: {room_state.get('status')}")
            sys.exit(1)
            
        # Fetch current question
        q_resp = requests.get(f"{BASE_URL}/battle/question/{room_code}")
        if q_resp.status_code != 200:
            print(f"❌ Failed to fetch question for round {round_num}: {q_resp.text}")
            sys.exit(1)
        q_data = q_resp.json()
        correct_ans = q_data.get("correct_answer")
        options = q_data.get("options", [])
        incorrect_ans = [o for o in options if o != correct_ans][0] if len(options) > 1 else "NO"
        
        print(f"❓ Question: \"{q_data.get('question_text')}\"")
        print(f"Options: {options} | Correct: {correct_ans}")
        
        # Host submits correct answer
        print("👤 Host submitting answer...")
        host_ans_resp = requests.post(f"{BASE_URL}/battle/answer", json={
            "room_code": room_code,
            "player_role": "host",
            "answer": correct_ans
        })
        if host_ans_resp.status_code != 200:
            print(f"❌ Host answer failed: {host_ans_resp.text}")
            sys.exit(1)
            
        print("✅ Host answer submitted!")
        
        # Guest submits incorrect answer
        print("👤 Guest submitting answer...")
        guest_ans_resp = requests.post(f"{BASE_URL}/battle/answer", json={
            "room_code": room_code,
            "player_role": "guest",
            "answer": incorrect_ans
        })
        if guest_ans_resp.status_code != 200:
            print(f"❌ Guest answer failed: {guest_ans_resp.text}")
            sys.exit(1)
            
        print("✅ Guest answer submitted!")
        
        # Room status should now be round_result
        room_resp = requests.get(f"{BASE_URL}/battle/room/{room_code}")
        room_state = room_resp.json()
        print(f"🏁 Round {round_num} complete! Status: {room_state.get('status')}")
        if room_state.get("status") != "round_result":
            print(f"❌ Room status should be 'round_result' after both answer, got: {room_state.get('status')}")
            sys.exit(1)
            
        # Host and guest score check
        print(f"Scores - Host: {room_state.get('host_score')}, Guest: {room_state.get('guest_score')}")
        
        # Advance to next round or end game
        print("⏭️ Advancing to next round...")
        next_resp = requests.post(f"{BASE_URL}/battle/next_round", json={
            "room_code": room_code
        })
        if next_resp.status_code != 200:
            print(f"❌ Failed to advance round: {next_resp.text}")
            sys.exit(1)
            
        room_state = next_resp.json()
        print(f"✅ Advanced room status: {room_state.get('status')} | New Round: {room_state.get('current_round')}")

    # 5. Verify game finished state
    print("\n--- Step 5: Game End Verification ---")
    if room_state.get("status") != "finished":
        print(f"❌ Final room status should be 'finished', got: {room_state.get('status')}")
        sys.exit(1)
        
    print("🏆 GAME OVER! SUCCESS!")
    print(f"Final score - Host: {room_state.get('host_score')} | Guest: {room_state.get('guest_score')}")
    print(f"🥇 Winner: {room_state.get('winner_username')}")
    print("✨ ALL 10 ROUNDS COMPLETED AND TRANSITIONED PERFECTLY WITHOUT FREEZING!")

if __name__ == "__main__":
    run_integration_test()
