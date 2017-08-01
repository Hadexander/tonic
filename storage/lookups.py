import hashlib
from storage import db

def find_user(uid : str):
    sha = hashlib.sha256()
    sha.update(uid.encode())
    user = db.User(sha = sha.hexdigest())
    db.pull(user)
    return user

def find_guild(uid : str):
    sha = hashlib.sha256()
    sha.update(uid.encode())
    guild = db.Guild(sha = sha.hexdigest())
    db.pull(guild)
    return guild