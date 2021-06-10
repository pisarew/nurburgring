import sqlite3 as sq
import requests


r = requests.get('http://www.nuerburgring.ru/info/lap_times_records.html')
s = str(r.text)

def add(car, pilot, front, back, time, date, carid):
    if carid > 0:
        cur.execute(f"INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?)", (car, pilot, front, back, time, date))
        con.commit()
        print(carid, " complite!")

def addPilots(pilot, pilotid):
    if pilot == '':
        return 0
    cur.execute(f"SELECT * FROM pilots WHERE pilot = '{pilot}'") #f"SELECT cash FROM users WHERE login = '{user_login}'"
    # records = cur.fetchone()
    if cur.fetchone() is None:
        cur.execute("INSERT INTO pilots VALUES (?, ?, ?)", (pilot, 1, pilotid))
        con.commit()
        return 1
    else:
        cur.execute(f"SELECT records FROM pilots WHERE pilot = '{pilot}'")
        records = cur.fetchone()[0]
        cur.execute(f"UPDATE pilots SET records = {records + 1} WHERE pilot = '{pilot}'")
        con.commit()
        return 0

def strcleaner(s_inp):
    s_out = ''
    s_inp = s_inp.lstrip()
    s_inp = s_inp.rstrip()
    for i in range(len(s_inp)):
        if s_inp[i].isalnum() or s_inp[i] == ' ':
            s_out += s_inp[i]
    if s_out == 'mdash':
        return ''
    else:
        return s_out

with sq.connect("cars.db") as con:
    cur = sq.Cursor(con)

    cur.execute("""CREATE TABLE IF NOT EXISTS cars (
        car TEXT,
        pilot TEXT,
        front TEXT,
        back TEXT,
        time TEXT,
        date TEXT
    )""")
    con.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS pilots (
        pilot TEXT,
        records INTEGER,
        id INTEGER
        )""")
    
    con.commit()
    fl = 0
    b = 1 # чет/нечет
    car_id = 0 
    car = ''
    pilot = ''
    front = ''
    back = ''
    time = ''
    date = ''
    carortime = 0
    pilotid = 0
    for i in range(len(s)):
        if s[i] == '<' and s[i + 1] == 't' and s[i + 18] == 't' and s[i + 17] == 's':   ## Тут вытягиваются машины и время 
            i += 24
            b += 1
            if b % 2 == 0: ##  тут мы понимаем с чем имеем дело (машина или резуцльтат круга). Если машина то это начало новой строки в таблице.
                print('\n\nАвтомобиль:', end='\t')
                carortime = 0
                if back == '':
                    back = front
                #add(strcleaner(car), strcleaner(pilot), strcleaner(front), strcleaner(back), time, strcleaner(date), car_id)
                x = addPilots(strcleaner(pilot), pilotid)
                pilotid += x
                car_id += 1
                car = ''
                pilot = ''
                front = ''
                back = ''
                time = ''
                date = ''
            else:
                carortime = 1
                print('\nВремя:', end = '\t')
            while s[i] != '<':
                if carortime == 0:
                    car += s[i]
                else:
                    time += s[i]
                print(s[i], end="")
                i += 1
        if s[i] == 't' and s[i + 1] == '1' and s[i + 2] == '0': # Здесь парсим пилота и шины.
            i += 4
            k = 1
            case = 0
            print("\nПилот:", end='\t')
            pilotorwheel = 0
            while s[i + 1] != '<' and s[i] != '<':
                i += 1
                if s[i] == '&' and s[i + 5] ==';':
                    i += 5
                    continue
                # if s[i] == '&' and s[i + 6] ==';':
                #     i += 6
                #     continue
                if s[i] == '|':
                    pilotorwheel += 1
                    print("\nШины:", end='\t') #Lars Kern |&nbsp;﻿Michelin Pilot Sport CUP2&nbsp;|&nbsp;Weissach Package
                    continue
                if pilotorwheel == 0:
                    pilot += s[i]
                elif pilotorwheel == 1:
                    front += s[i]
                else:
                    back += s[i]
                print(s[i], end='')
        if s[i] == '5' and s[i + 1] == '4' and s[i + 3] == '>': # Парсим дату
            i += 3
            print("\nДата:", end='\t')
            while s[i + 1] != '<' and s[i + 1] != '&':
                i += 1
                date += s[i]
                print(s[i], end='')