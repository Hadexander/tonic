import hashlib
from storage import db
import MySQLdb


'''
==============================================================================================
Connection parameters shouldn't be here, change later.
==============================================================================================
'''
xhost = "tonicdb.caq0gwjk9u9y.us-east-2.rds.amazonaws.com"
xport = 3306
xuser = "tonicvps"
xpasswd = "T0n1cVp5"
xdb = "innodb"

# conn = MySQLdb.connect(host=xhost, port=xport,
#                       user=xuser, passwd=xpasswd, db=xdb)

'''
==============================================================================================
==============================================================================================
'''


def hash(string: str):
    sha = hashlib.sha256()
    sha.update(string.encode())
    return sha.hexdigest()


def global_settings():
    obj = db.Settings(sha=hash(''))
    db.pull(obj)
    return obj


def find_user(uid: str):
    user = db.User(sha=hash(uid))
    db.pull(user)
    return user


def find_guild(uid: str):
    guild = db.Guild(sha=hash(uid))
    db.pull(guild)
    return guild


def find_emoji(name: str):

    conn = MySQLdb.connect(host=xhost, port=xport,
                           user=xuser, passwd=xpasswd, db=xdb)

    curs = conn.cursor()
    curs.callproc("GetEmoji", [name])
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]


def save_emoji(name: str, url: str):

    conn = MySQLdb.connect(host=xhost, port=xport,
                           user=xuser, passwd=xpasswd, db=xdb)

    curs = conn.cursor()
    curs.callproc("AddEmoji", [name, url])
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]


def delete_emoji(name: str):

    conn = MySQLdb.connect(host=xhost, port=xport,
                           user=xuser, passwd=xpasswd, db=xdb)

    curs = conn.cursor()
    curs.callproc("DeleteEmoji", [name])
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]


def list_emojis():

    conn = MySQLdb.connect(host=xhost, port=xport,
                           user=xuser, passwd=xpasswd, db=xdb)

    curs = conn.cursor()
    curs.callproc("ListEmojis")
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]
