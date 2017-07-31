import sys
import hashlib
from storage import db

if(len(sys.argv) < 2):
    print('Usage:\n\taddowner.py <id>\n')
    print('Registers discord user <id> as a superuser for the bot.')
else:
    id = sys.argv[1]
    sha = hashlib.sha256()
    sha.update(id.encode())
    user = db.User(sha = sha.hexdigest())
    user.retrieve()
    if(user.access == 9001):
        print('id:'+id+' already has owner-level access')
    else:
        user.access = 9001
        user.store()
        print('Successfully granted id:'+id+' owner-level access')
