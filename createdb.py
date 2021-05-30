import sqlite3 as sq
import requests


r = requests.get('http://www.nuerburgring.ru/info/lap_times_records.html')
s = str(r.text)

with sq.connect("cars.db") as con:
    cur = sq.Cursor(con)

    cur.execute("""CREATE TABLE IF NOT EXISTS cars (

        car TEXT NOT NULL,
        pilot TEXT,
        wheels TEXT,
        time TEXT NOT NULL,
        date TEXT
    )""")
    con.commit()
    fl = 0
    b = 1 # чет/нечет
    car_id = 0 
    for i in range(len(s)):
        if s[i] == '<' and s[i + 1] == 't' and s[i + 18] == 't' and s[i + 17] == 's':
            i += 24
            b += 1
            if b % 2 == 0:
                print('\n\nАвтомобиль:', end='\t')
                car_id += 1
            else:
                print('\nВремя:', end = '\t')
            while s[i] != '<':
                print(s[i], end="")
                i += 1
        if s[i] == 't' and s[i + 1] == '1' and s[i + 2] == '0':
            i += 4
            k = 1
            case = 0
            print("\nПилот:", end='\t')
            while s[i + 1] != '<' and s[i] != '<':
                i += 1
                if s[i] == '&' and s[i + 5] ==';':
                    i += 5
                    continue
                if s[i] == '&' and s[i + 6] ==';':
                    i += 6
                    continue
                if s[i] == '|':
                    print("\nШины:", end='\t')
                    continue
                print(s[i], end='')
        if s[i] == '5' and s[i + 1] == '4' and s[i + 3] == '>':
            i += 3
            print("\nДата:", end='\t')
            while s[i + 1] != '<' and s[i + 1] != '&':
                i += 1
                print(s[i], end='')
        if fl != car_id:
            cur.execute(f"INSERT INTO cars VALUES (?, ?, ?, ?, ?), (car, pilot, wheels, time, date)")
            con.commit()
            car = ''
            pilot = ''
            wheels = ''
            time = ''
            date = ''
            fl = car_id

