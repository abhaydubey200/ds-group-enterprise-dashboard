import hashlib

USERS = {
    "admin": {"password": "admin123", "role": "ADMIN"},
    "user": {"password": "user123", "role": "USER"},
}


def authenticate(username, password):
    user = USERS.get(username)
    if not user:
        return None
    if password == user["password"]:
        return {"username": username, "role": user["role"]}
    return None
