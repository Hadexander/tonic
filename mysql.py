import hashlib
from sqlalchemy import create_engine
from storage import db
import MySQLdb
from extras import emoji

'''
Connection parameters shouldn't be here, change later.
'''
xhost = "tonicdb.caq0gwjk9u9y.us-east-2.rds.amazonaws.com"
xport = 3306
xuser = "tonicvps"
xpasswd = "T0n1cVp5"
xdb = "innodb"
conn = MySQLdb.connect(host = xhost, port = xport, user = xuser, passwd= xpasswd, db = xdb)
'''
Connection test
'''
'''



result = curs.fetchall()
conn.close()

for row in result:
    print(row[0])
'''
engine = create_engine('sqlite:///storage.db')
result = engine.execute('SELECT * FROM emojis')

for row in result:

    e = emoji.save_emoji(row[2],row[1])
    print(e)
