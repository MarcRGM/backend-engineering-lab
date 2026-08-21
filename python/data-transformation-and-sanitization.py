raw_users = [
    {"id": 1, "username": "alice", "email": "alice@example.com", "role": "admin", "password_hash": "hash_123", "is_active": True},
    {"id": 2, "username": "bob", "email": "bob@example.com", "role": "subscriber", "password_hash": "hash_456", "is_active": False},
    {"id": 3, "username": "carol", "email": "carol@example.com", "role": "editor", "password_hash": "hash_789", "is_active": True},
    {"id": 4, "username": "dave", "email": "dave@example.com", "role": "admin", "password_hash": "hash_000", "is_active": True},
    {"id": 5, "username": "eve", "email": "eve@example.com", "role": "subscriber", "password_hash": "hash_111", "is_active": True},
]

# Expected Output
{
    "admin": [
        {"id": 1, "username": "alice", "email": "alice@example.com"},
        {"id": 4, "username": "dave", "email": "dave@example.com"}
    ],
    "editor": [
        {"id": 3, "username": "carol", "email": "carol@example.com"}
    ],
    "subscriber": [
        {"id": 5, "username": "eve", "email": "eve@example.com"}
    ]
}

def transform_user_directory(users: list[dict]) -> dict[str, list[dict]]:
    # Filter
    active = [user for user in users if users["is_active"]]
    # Sanitize
    