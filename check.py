import sqlite3
conn=sqlite3.connect('cppcodes.db')
c=conn.cursor()
c.execute('SELECT * FROM history')
row=c.fetchall()
for i in row:
    print(i)
