from collections import defaultdict

raw_users = [
    {"id": 1, "username": "alice", "email": "alice@example.com", "role": "admin", "password_hash": "hash_123", "is_active": True},
    {"id": 2, "username": "bob", "email": "bob@example.com", "role": "subscriber", "password_hash": "hash_456", "is_active": False},
    {"id": 3, "username": "carol", "email": "carol@example.com", "role": "editor", "password_hash": "hash_789", "is_active": True},
    {"id": 4, "username": "dave", "email": "dave@example.com", "role": "admin", "password_hash": "hash_000", "is_active": True},
    {"id": 5, "username": "eve", "email": "eve@example.com", "role": "subscriber", "password_hash": "hash_111", "is_active": True},
]

# Write a function named transform_user_directory(users: list[dict]) 
#               -> dict[str, list[dict]] that satisfies these requirements:
#   Filter:     Include only active users ("is_active": True).
#   Sanitize:   The output dictionaries must contain only id, username, and email. 
#               Omit password_hash and all other fields.
#   Group:      Return a single dictionary where keys are the role (e.g., "admin", "editor", "subscriber") 
#               and values are lists of the sanitized user dictionaries belonging to that role.

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
    # Filter inactive users
    active = [user for user in users if user["is_active"]] # List comprehension
    # Sanitize using whitelisting and Group based on roles
    grouped: dict[str, list[dict]] = defaultdict(list)
    allowed_keys = ("id", "username", "email")
    for user in active:
        sanitized_user = {k: user[k] for k in allowed_keys if k in user} # Dictionary comprehension
        grouped[user["role"]].append(sanitized_user)
    return dict(grouped) # convert to dict for cleaner output

if __name__ == "__main__":
    print(transform_user_directory(raw_users))

       