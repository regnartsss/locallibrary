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
    req = "SELECT filial.kod, region, name, status_1, status_2, ISP1, ISP2  FROM filial LEFT JOIN status ON filial.kod = status.kod ORDER BY name"
    # print(req)
    rows = sql_select(req)
    for row in rows:
        # print(row)
        st1, st2 = status(row[3], row[4], row[5], row[6])
        temp = [st1, st2, row[0], row[2]]
        if row[1] == 0:
            try:
                s[0].append(temp)
            except:
                s[0] = []
                s[0].append(temp)
        elif row[1] == 1:
            try:
                s[1].append(temp)
            except:
                s[1] = []
                s[1].append(temp)
        elif row[1] == 2:
            try:
                s[2].append(temp)
            except:
                s[2] = []
                s[2].append(temp)
        elif row[1] == 3:
            try:
                s[3].append(temp)
            except:
                s[3] = []
                s[3].append(temp)
        elif row[1] == 4:
            try:
                s[4].append(temp)
            except:
                s[4] = []
                s[4].append(temp)
        elif row[1] == 5 or row[1] == 6:
            try:
                s[5].append(temp)
            except:
                s[5] = []
                s[5].append(temp)
        elif row[1] == 7 or row[1] == 8 or row[1] == 9:
            try:
                s[7].append(temp)
            except:
                s[7] = []
                s[7].append(temp)

    # print(s)

    # kod = s
#     le = {}
#     for l in s:
#         le[l] = len(s[l])
#     sort = sorted(le.items(), key=lambda k: -k[1])
#     ll = sort[0][1]
#     print(s)
    kod = sorted(s.items(), key=lambda k: k)
    # print(kod)
    # print(kod)
#     # print(ll)
#     kod = s
#     i = 0
#     tab = {}
#     while i < ll:
#         try:
#             tab[i]
#         except KeyError:
#             tab[i] = []
#             # print(sort)
#         for ss in sort:
#             # print(ss)
#             # print(s[ss[0]])
#             # print(s[ss[0]][0])
#             try:
#                 tab[i].append(s[ss[0]][i])
# # #                 print(stat[s[ss[0]][i]])
# # #                 status(tab[i], stat[s[ss[0]][i]], s[ss[0]][i])
#             except IndexError:
#                 tab[i].append("")
#         i += 1
# # #     # print(tab)
#     kod = tab

    return render(
        request,
        'index.html',
        context={'kod': kod, "time":data_monitor()},
    )


# index()


def status(s1, s2, ISP1, ISP2):
    ch1, ch2 = '🟡','🟡'
    if s1 == 1:
        ch1 = "🔵"
    elif s1 == 0:
        ch1 = "🔴"
    if s2 == 1:
        ch2 = "🔵"
    elif s2 == 0:
        ch2 = "🔴"
    if ISP1 == "unassigned":
        ch1 = "⚪"
    if ISP2 == "unassigned":
        ch2 = "⚪"
    return ch1, ch2


        #
#         open_all()
#
#         """
#             Функция отображения для домашней страницы сайта.
#             """
#         # Генерация "количеств" некоторых главных объектов
#         #    print(len(stat))
#         column = (int(len(stat)/5))+2
#         print("строчек %s" % column)
#         r =0
#         tab = 0
#         s = {}
#         #
#         col = [5,10,15,20,25,30]
#         try:
#             for k, v in stat.items():
#                     if v["status_t1"] == 1:
#                         ch1 = "🔵"
#                     elif v["status_t1"] == 0:
#                         ch1 = "🔴"
#                     if v["status_t2"] == 1:
#                         ch2 = "🔵"
#                     elif v["status_t2"] == 0:
#                         ch2 = "🔴"
#                     if dat[str(k)]["ISP1"] == "unassigned":
#                         ch1 = "⚪"
#                     if dat[str(k)]["ISP2"] == "unassigned":
#                         ch2 = "⚪"
#                     try:
#                         s[tab].append([ch1, ch2, k, dat[str(k)]["name"]])
#                     except:
#                         s[tab] = []
#                         s[tab].append([ch1, ch2, k, dat[str(k)]["name"]])
#                     r += 1
#                     if r in col:
#                         tab += 1
#                     # s[k].append("kod": k,"name": dat[str(k)]["name"], "st1": ch1, "st2": ch2)
#             #     r+=1
#             #     print(s)
#             kod = s
#         except:
#             pass

        # Отрисовка HTML-шаблона index.html с данными внутри
        # переменной контекста context

