ROLE_PERMISSIONS = {
    "ADMIN": {
        "tables": ["OUTLET_MASTER"],
        "actions": ["CREATE", "READ", "UPDATE", "DELETE", "MERGE"]
    },
    "MANAGER": {
        "tables": ["OUTLET_MASTER"],
        "actions": ["READ", "UPDATE"]
    },
    "VIEWER": {
        "tables": ["OUTLET_MASTER"],
        "actions": ["READ"]
    }
}

def can_access(user, table, action):
    return (
        table in ROLE_PERMISSIONS[user["role"]]["tables"]
        and action in ROLE_PERMISSIONS[user["role"]]["actions"]
    )

