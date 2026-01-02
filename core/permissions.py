ROLE_PERMISSIONS = {
    "ADMIN": {"read", "insert", "update", "delete", "merge"},
    "MANAGER": {"read", "insert", "update"},
    "USER": {"read"},
}


def has_permission(role, action):
    return action in ROLE_PERMISSIONS.get(role, set())
