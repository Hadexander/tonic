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
    db.pull(user)
    if(user.access == 9001):
        print('id:{} already has owner-level access'.format(id))
    else:
        user.access = 9001
        db.merge(user)
        print('Successfully granted id:{} owner-level access'.format(id))
