import MySQLdb

'''
Connection parameters shouldn't be here, change later.
'''
xhost = "tonicdb.caq0gwjk9u9y.us-east-2.rds.amazonaws.com"
xport = 3306
xuser = "tonicvps"
xpasswd = "T0n1cVp5"
xdb = "innodb"

'''
Connection test
'''

conn = MySQLdb.connect(host = xhost, port = xport, user = xuser, passwd= xpasswd, db = xdb)
curs = conn.cursor()
curs.execute("Select Count(ID) From emojis")

result = curs.fetchall()


for row in result:
    print(row[0])

conn.close()