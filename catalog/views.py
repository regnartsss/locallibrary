from django.shortcuts import render
from datetime import datetime
global stat, dat
import pymysql

# HOST = '10.0.111.158'
# PORT = 3306
# USER = 'bdused'
# PASSWORD = 'Q!W@E#R$'
# DB = 'bd_vs_monitoring'
# charset = 'utf8mb4'
# HOST = '10.0.111.158'
HOST = '10.97.172.10'
#
PORT = 3306
# USER = 'bdused'
USER = 'bduser'
# PASSWORD = 'Q!W@E#R$'
PASSWORD = 'q1W@e3R$'
DB = 'bd_vs_monitoring'
charset = 'utf8mb4'


# def bd_fetchall(request):
#     conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=charset)
#     cursor = conn.cursor()
#     cursor.execute(request)
#     rows = cursor.fetchall()
#     return rows


def bd_fetchall(request):
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB, charset=charset)
    with conn.cursor() as cursor:
        # cursor = await conn.cursor()
        cursor.execute(request)
        return cursor.fetchall()


def data_monitor():
    return datetime.today().strftime("%H:%M:%S %d/%m/%Y")


def index(request):
    r = 0
    tab = 0
    s = {}
    # stat_one = (sorted(dat.items(), key=lambda k: k[1]["region"]))
    req = "SELECT bd_devices.kod, region_mon, name, status_1, status_2, ISP1, ISP2,  sdwan, Oper1, Oper2, status_operisp2  FROM bd_devices LEFT JOIN bd_status " \
          "ON bd_devices.kod = bd_status.kod WHERE bd_status.kod is not null ORDER BY name"
    # print(req)
    rows = bd_fetchall(req)
    for row in rows:
        name = f"{row[0]} {row[2]}"
        name = ser_name(name)[:24]
        # name = row[2][:25]
        st1, st2, sd = status(row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        temp = [sd, st1, st2, name]
        try:
            # s[row[1]].append(temp)
            if len(s[row[1]]) > 26:
                try:
                    s[row[1]+0.5].append(temp)
                except KeyError:
                    s[row[1]+0.5] = []
                    s[row[1]+0.5].append(temp)
            else:
                s[row[1]].append(temp)
        except KeyError:
            s[row[1]] = []
            s[row[1]].append(temp)

    kod = sorted(s.items(), key=lambda k: k)
    r ={}
    num = int(len(rows)/6.5)
    i = 0
    s_i = 0
    req = """SELECT bd_devices.kod, name, down, disk, ip, cam, cam_down, script, bd_devices.loopback FROM bd_devices 
    LEFT JOIN bd_registrator ON bd_devices.kod = bd_registrator.kod WHERE bd_registrator.ip is not null ORDER BY name"""
    rows = bd_fetchall(req)
    # rows = sql_select(f"SELECT down FROM registrator WHERE kod = {row[0]}")
    for row in rows:
        if row[2] == 1:
            reg, d, c, s = "🟥", "🟥",  "🟥", "🟥"
        else:
            reg = registrator(row[2])
            d = disk(row[3])
            c = cam(row[5], row[6])
            s = disk(row[7])
            if reg == "⬜️":
                c = "⬜️"
        # name = f"{row[0]} {row[1]}"
        name = row[1]
        name = name.split()
        n1 = name[0]
        n2 = ' '.join(name[1:])
        if len(n1) > 5:
            n1 = n1[:5]
        name = f"{n1} {n2}"
        name = name[:15]
        temp = [name, reg, d, row[4], c, s]
        if i == num:
            i = 0
            try:
                r[s_i].append(temp)
            except KeyError:
                r[s_i] = []
                r[s_i].append(temp)
            s_i += 1
        else:
            try:
                r[s_i].append(temp)
            except KeyError:
                r[s_i] = []
                r[s_i].append(temp)
            i += 1

    reg = sorted(r.items(), key=lambda k: k)
    return render(
        request,
        'index.html',
        context={'kod': kod, 'reg':reg, "time":data_monitor()},
    )


def ser_name(name):
    name = name.split()
    n1 = name[0]
    n2 = (' '.join(name[1:]))[0:]
    n = 4 - len(n1)
    if n == 1:
        n1 = f"{n1}⠀"
    elif n == 2:
        n1 = f"{n1}⠀⠀"
    elif n == 3:
        n1 = f"{n1}⠀⠀⠀"
    else:
        n1 = f"{n1} "
    name = f"{n1}{n2}"
    return name


# def scr(s):
#     if s == 1:
#         c = "🟩"
#     else:
#         c = "🟨"
#     return c


def cam(all, up):
    if all == up:
        c = "🟩"
    else:
        c = "🟨"
    return c


def disk(row):
    st = ""
    if row == "OK":
        st += "🟩"
    elif row == "ERROR":
        st += "🟦"
    else:
        st += "⬜️"
    return st


def registrator(row):
    st = ""
    if row == 1:
        st += "🟥"
    elif row == 0:
        st += "🟩"
    else:
        st += "⬜️"
    return st


def status(s1, s2, ISP1, ISP2, sdwan, op1, op2, st_op2):
    ch1, ch2, sd = '🟡','🟡', "⚪"
    if s1 == 1:
        ch1 = "🟢"
    elif s1 == 0:
        ch1 = "🔴"
    if s2 == 1:
        ch2 = "🟢"
    elif s2 == 0:
        ch2 = "🔴"
    if op1 == 2:
        ch1 = "🔵"
    if op2 == 2:
        ch2 = "🔵"
    if op2 == 1 and st_op2 == 2:
        ch2 = "✔️"
    # if ISP1 == "unassigned":
    #     ch1 = "⚪"
    #     # chop1 = "⚪"
    # if ISP2 == "unassigned":
    #     ch2 = "⚪"
        # chop2 = "⚪"
    if sdwan == 1:
        # sd = "❌"
        sd = "⚫"
    return ch1, ch2, sd
