from django.shortcuts import render
import json
import os
from datetime import datetime, timedelta
# Create your views here.
# from .models import Book, Author, BookInstance, Genre
global stat, dat
import sqlite3


def sql_select(request):
    conn = sqlite3.connect(r'C:\GitHub\snmpvs\work\sdwan.db')
    # conn = sqlite3.connect(r'C:\Users\podkopaev.k\PycharmProjects\snmpvs\work\sdwan.db')
    cursor = conn.cursor()
    cursor.execute(request)
    rows = cursor.fetchall()
    return rows


def data_monitor():
    return datetime.today().strftime("%H:%M:%S %d/%m/%Y")


def index(request):
    r = 0
    tab = 0
    s = {}
    # stat_one = (sorted(dat.items(), key=lambda k: k[1]["region"]))
    req = "SELECT filial.kod, region, name, status_1, status_2, ISP1, ISP2,sdwan  FROM filial LEFT JOIN status " \
          "ON filial.kod = status.kod ORDER BY name"
    # print(req)
    rows = sql_select(req)
    for row in rows:
        # rows = sql_select(f"SELECT down FROM registrator WHERE kod = {row[0]}")
        # reg = f"\n {registrator(rows)}"
        name = f"{row[0]} {row[2]}"
        name = f" {name[:25]}"
        st1, st2, sd = status(row[3], row[4], row[5], row[6], row[7])
        temp = [sd, st1, st2, name]
        if row[1] == 0:
            try:
                s[0].append(temp)
            except KeyError:
                s[0] = []
                s[0].append(temp)
        elif row[1] == 1:
            try:
                s[1].append(temp)
            except KeyError:
                s[1] = []
                s[1].append(temp)
        elif row[1] == 2:
            try:
                s[2].append(temp)
            except KeyError:
                s[2] = []
                s[2].append(temp)
        elif row[1] == 3:
            try:
                s[3].append(temp)
            except KeyError:
                s[3] = []
                s[3].append(temp)
        elif row[1] == 4:
            try:
                s[4].append(temp)
            except KeyError:
                s[4] = []
                s[4].append(temp)
        elif row[1] == 5 or row[1] == 6:
            try:
                s[5].append(temp)
            except KeyError:
                s[5] = []
                s[5].append(temp)
        elif row[1] == 7 or row[1] == 8 or row[1] == 9:
            try:
                s[7].append(temp)
            except KeyError:
                s[7] = []
                s[7].append(temp)
    kod = sorted(s.items(), key=lambda k: k)


    r ={}
    num = int(len(rows)/7)
    i = 0
    s_i = 0
    req = "SELECT filial.kod, name, down, disk, ip, cam, cam_down FROM filial LEFT JOIN registrator ON filial.kod = registrator.kod ORDER BY name"
    rows = sql_select(req)
    # rows = sql_select(f"SELECT down FROM registrator WHERE kod = {row[0]}")
    for row in rows:
        if row[2] == 1:
            reg, d, c = "🟥", "🟥",  "🟥"
        else:
            reg = registrator(row[2])
            d = disk(row[3])
            c = cam(row[5], row[6])
        # name = f"{row[0]} {row[1]}"
        name = row[1]
        name = name.split()
        n1 = name[0]
        n2 = ' '.join(name[1:])
        if len(n1) > 5:
            n1 = n1[:5]
        name = f"{n1} {n2}"
        name = name[:15]
        temp = [name, reg, d, row[4], c]
        if i == num:
            i = 0
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
        st += "🟥"
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


def status(s1, s2, ISP1, ISP2, sdwan):
    ch1, ch2, sd = '🟡','🟡', "⚪"
    if s1 == 1:
        ch1 = "🟢"
    elif s1 == 0:
        ch1 = "🔴"
    if s2 == 1:
        ch2 = "🟢"
    elif s2 == 0:
        ch2 = "🔴"
    if ISP1 == "unassigned":
        ch1 = "⚪"
    if ISP2 == "unassigned":
        ch2 = "⚪"
    if sdwan == 1:
        # sd = "❌"
        sd = "⚫"
    return ch1, ch2, sd
