import hashlib
from storage import db

def hash(string : str):
    sha = hashlib.sha256()
    sha.update(string.encode())
    return sha.hexdigest()

def global_settings():
    obj = db.Settings(sha = hash(''))
    db.pull(obj)
    return obj

def find_user(uid : str):
    user = db.User(sha = hash(uid))
    db.pull(user)
    return user

def find_guild(uid : str):
    guild = db.Guild(sha = hash(uid))
    db.pull(guild)
    return guild