import hashlib
from storage import db

async def retrieve_user(uid : str):
    sha = hashlib.sha256()
    sha.update(uid.encode())
    user = db.User(sha = sha.hexdigest())
    user.retrieve()
    return user