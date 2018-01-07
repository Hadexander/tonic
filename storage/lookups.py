import hashlib
from storage import db

def hash(string : str):
    sha = hashlib.sha256()
    sha.update(string.encode())
    return sha.hexdigest()

def get_setting(name : str):
    setting = db.Setting(sha = hash(name))
    db.pull(setting)
    return setting

def store_setting(name, value):
    setting = db.Setting(sha = hash(name))
    setting.name = name
    setting.value = value
    setting.save()

def find_user(uid : str):
    user = db.User(sha = hash(uid))
    db.pull(user)
    return user

def find_guild(uid : str):
    guild = db.Guild(sha = hash(uid))
    db.pull(guild)
    return guild