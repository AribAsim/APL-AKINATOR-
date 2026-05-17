import uuid
from typing import Dict, Optional
from api.models import SessionState

class SessionService:
    def __init__(self):
        # In-memory session store
        self.sessions: Dict[str, SessionState] = {}

    def create_session(self) -> SessionState:
        session_id = str(uuid.uuid4())
        session = SessionState(
            session_id=session_id,
            probabilities={}, # Will be populated by engine
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[SessionState]:
        return self.sessions.get(session_id)

    def save_session(self, session: SessionState):
        self.sessions[session.session_id] = session

    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

# Singleton instance
session_service = SessionService()
