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
    def __init__(self, session_id: str, user_id: int, scope: str):
        pass


class SessionRepository:
    def __init__(self):
        pass