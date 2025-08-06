from django.shortcuts import render
from datetime import datetime
global stat, dat
import psycopg2


HOST = 'localhost'
USER = 'user_bot'
PASSWORD = 'z15X3vdy%'
DB = 'db_vs_bot'
charset = 'utf8mb4'


# def bd_fetchall(request):
#     conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWORD, db=DB, charset=charset)
#     cursor = conn.cursor()
#     cursor.execute(request)
#     rows = cursor.fetchall()
#     return rows


def bd_fetchall(request):
    conn = psycopg2.connect(database=DB, user=USER, password=PASSWORD, host=HOST, port=5432)
    # conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB, charset=charset)
    with conn.cursor() as cursor:
        cursor.execute(request)
        return cursor.fetchall()


def data_monitor():
    return datetime.today().strftime("%H:%M:%S %d/%m/%Y")


def index(request):
    r = 0
    tab = 0
    s = {}
    # stat_one = (sorted(dat.items(), key=lambda k: k[1]["region"]))
    req = """SELECT db_devices.kod, region_mon, name, sdwan, status_tu0, status_tu1, "link_Gi0/0/0", "link_Gi0/0/1", "link_tu1", "lte", region_text, "ssh_protocol_0/0/1", ssh_protocol_tu1, "ssh_status_0/0/1", "ssh_protocol_0/0/0", ssh_protocol_tu0, "ssh_status_0/0/0"  FROM db_devices LEFT JOIN db_status ON db_devices.kod = db_status.kod WHERE db_status.kod is not null and hostname is not null ORDER BY name"""
    rows = bd_fetchall(req)

    for row in rows:
        ssh_protocol_001 = row[11]
        ssh_protocol_tu1 = row[12]
        ssh_status_001 = row[13]
        ssh_protocol_000 = row[14]
        ssh_protocol_tu0 = row[15]
        ssh_status_000 = row[16]
        name = f"{row[0]} {row[2]}"
        name = ser_name(name)[:24]
        name = row[2][:19]
        # print(name)
        st1, st2, sd = status(row[4], row[5], row[3], row[6], row[7], row[8], row[9], ssh_protocol_001, ssh_protocol_tu1, ssh_status_001, ssh_protocol_000, ssh_protocol_tu0, ssh_status_000)
        temp = ['   ', st1, st2, name]
        temp_reg = ['⚪️', '⚪️', row[10]]
        try:
            # s[row[1]].append(temp)
            if len(s[row[1]]) > 25:
                try:
                    s[row[1]+0.5].append(temp)
                except KeyError:
                    s[row[1]+0.5] = []
                    s[row[1]+0.5].append(temp)
            else:
                s[row[1]].append(temp)
        except KeyError:
            s[row[1]] = []
            s[row[1]].append(temp_reg)
            s[row[1]].append(temp)

    kod = sorted(s.items(), key=lambda k: k)
    r ={}
    num = int(len(rows)/6.3)
    i = 0
    s_i = 0
    req = """SELECT db_devices.kod, name, down, disk, ip, cam, cam_down, script, db_devices.loopback0 FROM db_devices
    LEFT JOIN db_registrator ON db_devices.kod = db_registrator.kod WHERE db_registrator.ip is not null ORDER BY name, db_registrator.hostname"""
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
            n1 = n1[:4]
        name = f"{n1} {n2}"
        name = name[:12]
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


def status(s1, s2, sdwan, linkgi0, linkgi1, linktu1, lte, ssh_protocol_001, ssh_protocol_tu1,ssh_status_001, ssh_protocol_000, ssh_protocol_tu0, ssh_status_000):
    # print(s1, s2, sdwan, linkgi0, linkgi1, linktu0, linktu1, linktu20)
    ch1, ch2, sd = '🟡','🟡', "⚪"
    if s1 == 1:
        ch1 = "🟢"
    elif s1 == 0:
        ch1 = "🔴"
    if s2 == 1:
        ch2 = "🟢"
    elif s2 == 0:
        ch2 = "🔴"

    if linkgi0 == 2 and ssh_protocol_000 == 0 and ssh_protocol_tu0 == 0 and ssh_status_000 == 0:
        ch1 = "🔵"
    if ssh_protocol_000 == 0 and ssh_protocol_tu0 == 0 and ssh_status_000 == 1:
        ch1 = "✔️"

    if linkgi1 == 2 and ssh_protocol_001 == 0 and ssh_protocol_tu1 == 0 and ssh_status_001 == 0:
        ch2 = "🔵"
    if ssh_protocol_001 == 0 and ssh_protocol_tu1 == 0 and ssh_status_001 == 1:
        ch2 = "✔️"



    if linktu1 == 1 and linkgi1 == 2 and lte == 1:
        ch2 = "📶"
    # if linktu20 == 1 and linkgi1 == 2:
    #     ch2 = "🟤"
    # if linktu20 == 1 and s2 == 0 and linkgi1 == 2:
    #     ch2 = "🟠"
    # if linkgi1 == 2 and linktu20 == 1 and s1 == 0:
    #     ch2 = "🟣"
    if s1 == 0 and s2 == 0:
        ch1 = "🔴"
        ch2 = "🔴"
    # if s1 == 1 and s2 == 1 and linktu20 == 1:
    #     ch1 = "🟢"
    #     ch2 = "🟢"


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
