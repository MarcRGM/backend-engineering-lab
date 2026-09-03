# You are building the session management engine for an authentication backend.

# You must create two distinct classes:

# UserSession:
# - A domain entity representing an active session token for a user.
# SessionRepository: 
# - An in-memory data store providing safe CRUD (Create, Read, Update/Revoke, Count) operations.

# Raw Test Sequence
"""
    repo = SessionRepository()

    # 1. Create sessions
    s1 = repo.create_session("sess-001", user_id=10, scope="READ")
    s2 = repo.create_session("sess-002", user_id=10, scope="ADMIN")
    s3 = repo.create_session("sess-003", user_id=20, scope="READ")

    # 2. Inspect representations and queries
    print("Total stored:", repo.count())
    print("All active:", repo.list_active_sessions())
    print("Active for user 10:", repo.list_active_sessions(user_id=10))

    # 3. Revoke one session
    revoked = repo.revoke_session("sess-002")
    print("Revoke sess-002 succeeded:", revoked)

    # 4. Check active for user 10 again
    print("Active for user 10 after revoke:", repo.list_active_sessions(user_id=10))

    # 5. Revoke a non-existent session
    print("Revoke non-existent:", repo.revoke_session("sess-999"))
"""

# Expected Output
"""
Total stored: 3
All active: [UserSession(id='sess-001', user_id=10, active=True), UserSession(id='sess-002', user_id=10, active=True), UserSession(id='sess-003', user_id=20, active=True)]
Active for user 10: [UserSession(id='sess-001', user_id=10, active=True), UserSession(id='sess-002', user_id=10, active=True)]
Revoke sess-002 succeeded: True
Active for user 10 after revoke: [UserSession(id='sess-001', user_id=10, active=True)]
Revoke non-existent: False
"""

class UserSession:
    VALID_SCOPE = {"READ", "ADMIN"}
    def __init__(self, session_id: str, user_id: int, scope: str):
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("Invalid session_id")
        self.session_id = session_id.strip()
        if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id <= 0:
            raise ValueError("Invalid user_id")
        self.user_id = user_id
        if scope not in self.VALID_SCOPE:
            raise ValueError("Invalid scope")
        self.scope = scope
        self._is_active = True 

    @property
    def session_id(self) -> str:
        return self.session_id

    @property
    def user_id(self) -> int:
        return self.user_id

    @property
    def scope(self) -> str:
        return self.scope

    def revoke(self) -> None:
        self._is_active = False

    def __repr__(self) -> str:
        return f"UserSession(id={self.session_id!r}, user_id={self.user_id}, active={self._is_active})"

class SessionRepository:
    def __init__(self):
        self._sessions: dict[str, UserSession] = {}

    def create_session(self, session_id: str, user_id: int, scope: str) -> UserSession:
        if session_id in self._sessions:
            raise ValueError(f"Session {session_id} already exists")
        self._sessions[session_id] = UserSession(session_id, user_id, scope)
        return self._sessions[session_id]

    def get_session(self, session_id: str) -> UserSession | None:
        return self._sessions.get(session_id, None)

    def revoke_session(self, session_id: str) -> bool:
        if session_id not in self._sessions: return False
        self._sessions[session_id].revoke()

    def list_active_sessions(self, user_id: int | None = None) -> list[UserSession]: 
        if user_id is not None: # Compare the user id in each session.user_id and return the session
            return [self._session[session] for session in self._sessions if user_id == self._sessions[session].user_id]
        # if user id is None, return list of all sessions active
        return [self._sessions[session] for session in self._sessions if self._sessions[session]._is_active == True]