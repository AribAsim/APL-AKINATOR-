import json
import os
import datetime
from typing import Dict, Any

class TelemetryService:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.log_file = os.path.join(self.data_dir, 'telemetry.json')
        
    def log_session(self, session_id: str, questions_asked: list, final_guess: str, confidence: float):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "session_id": session_id,
            "questions_asked": questions_asked,
            "questions_count": len(questions_asked),
            "final_guess": final_guess,
            "confidence": confidence
        }
        
        # Simple file append (using a JSON lines format or just a list)
        try:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    json.dump([entry], f)
            else:
                with open(self.log_file, 'r') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []
                data.append(entry)
                with open(self.log_file, 'w') as f:
                    json.dump(data, f)
        except Exception as e:
            print(f"Error logging telemetry: {e}")

telemetry_service = TelemetryService()
