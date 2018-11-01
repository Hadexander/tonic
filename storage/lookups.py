import hashlib
from storage import db, settings
import MySQLdb

def hash(string: str):
    sha = hashlib.sha256()
    sha.update(string.encode())
    return sha.hexdigest()

def find_user(uid: str):
    user = db.User(sha=hash(uid))
    db.pull(user)
    return user


def find_guild(uid: str):
    guild = db.Guild(sha=hash(uid))
    db.pull(guild)
    return guild


def find_emoji(name: str):
    conf = settings.load('MySQL')
    conn = MySQLdb.connect(host=conf.get('host'), port=conf.get('port'),
                           user=conf.get('user'), passwd=conf.get('password'), db=conf.get('dbname'))

    curs = conn.cursor()
    curs.callproc("GetEmoji", [name])
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]


def save_emoji(name: str, url: str):
    conf = settings.load('MySQL')
    conn = MySQLdb.connect(host=conf.get('host'), port=conf.get('port'),
                           user=conf.get('user'), passwd=conf.get('password'), db=conf.get('dbname'))

    curs = conn.cursor()
    curs.callproc("AddEmoji", [name, url])
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]


def delete_emoji(name: str):
    conf = settings.load('MySQL')
    conn = MySQLdb.connect(host=conf.get('host'), port=conf.get('port'),
                           user=conf.get('user'), passwd=conf.get('password'), db=conf.get('dbname'))

    curs = conn.cursor()
    curs.callproc("DeleteEmoji", [name])
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]


def list_emojis():
    conf = settings.load('MySQL')
    conn = MySQLdb.connect(host=conf.get('host'), port=conf.get('port'),
                           user=conf.get('user'), passwd=conf.get('password'), db=conf.get('dbname'))

    curs = conn.cursor()
    curs.callproc("ListEmojis")
    result = curs.fetchall()
    curs.close()
    conn.close()
    emoji = result[0]
    return emoji[0]
