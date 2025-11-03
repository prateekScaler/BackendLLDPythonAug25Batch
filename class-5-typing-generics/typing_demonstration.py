def find_user(name: str) -> dict | None:
    if name in database:
        return database[name]
    return None

user = find_user("Alice")
print(user.email)
