import sqlite3 as sq

with sq.connect("pilots.db") as con:
    cur = sq.Cursor(con)
    cur.execute("""CREATE TABLE IS NOT EXISTS""")