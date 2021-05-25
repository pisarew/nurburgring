import sqlite3 as sq
import requests

r = requests.get('http://www.nuerburgring.ru/info/lap_times_records.html')
s = str(r.text)

# with sq.connect("cars.db") as con:
#     cur = sq.Cursor(con)

#     cur.execute("""CREATE TABLE IF NOT EXISTS cars(
#         brand TEXT,
#         model TEXT NOT NULL,
#         pilot TEXT,
#         time TEXT IS NIT NULL,
#         date TEXT
#     )""")
    
for i in range(len(s)):
    if s[i] == '<' and s[i + 1] == 't' and s[i + 2] == 'd' and s[i + 17] == 's':
        i += 24
        while s[i] != '<':
            print(s[i], end="")
            i += 1
        print('\n')

