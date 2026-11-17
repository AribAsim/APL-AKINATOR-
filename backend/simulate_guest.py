import os
import time
import requests
from dotenv import load_dotenv

# Load env
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

BASE_URL = "http://localhost:8000/api"

def main():
    room_code = input("Enter room code to join: ").strip().upper()
    username = "SimulatedGuest"
    
    # 1. Join room
    print(f"Joining room {room_code} as {username}...")
    resp = requests.post(f"{BASE_URL}/battle/join", json={
        "room_code": room_code,
        "guest_username": username
        
    })
    
    if resp.status_code != 200:
        print("Failed to join room:", resp.json())
        return
        
    room = resp.json()
    print("Joined successfully! Initial Room State:", room)
    
    # 2. Game Loop
    while True:
        # Fetch fresh room state
        room_resp = requests.get(f"{BASE_URL}/battle/room/{room_code}")
        if room_resp.status_code != 200:
            print("Failed to fetch room state")
            time.sleep(2)
            continue
            
        room = room_resp.json()
        status = room.get("status")
        current_round = room.get("current_round", 1)
        
        print(f"[Status: {status} | Round: {current_round}]")
        
        if status == "finished":
            print("🏆 Game Finished! Winner:", room.get("winner_username"))
            print("Scores - Host:", room.get("host_score"), "Guest:", room.get("guest_score"))
            break
            
        elif status == "active":
            # Check if simulator has already answered this round
            if not room.get("guest_last_answer"):
                # Fetch current question to know the options
                q_resp = requests.get(f"{BASE_URL}/battle/question/{room_code}")
                if q_resp.status_code == 200:
                    q = q_resp.json()
                    options = q.get("options", ["YES", "NO"])
                    dummy_answer = options[0]
                    print(f"Question: {q.get('question_text')} | Options: {options}")
                    print(f"Submitting guest answer: {dummy_answer}")
                    
                    ans_resp = requests.post(f"{BASE_URL}/battle/answer", json={
                        "room_code": room_code,
                        "player_role": "guest",
                        "answer": dummy_answer
                    })
                    if ans_resp.status_code == 200:
                        print("Answer submitted successfully!")
                    else:
                        print("Failed to submit answer:", ans_resp.json())
                else:
                    print("Failed to fetch current question")
            else:
                print("Waiting for Host to answer...")
                
        elif status == "round_result":
            print("Showing round results. Waiting for transition to next round...")
            
        elif status == "countdown":
            print("Counting down to start...")
            
        elif status == "waiting":
            print("Waiting in lobby...")
            
        time.sleep(1.5)

if __name__ == "__main__":
    main()
