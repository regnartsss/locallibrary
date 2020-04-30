from django.shortcuts import render
import json
import os
from datetime import datetime, timedelta
# Create your views here.
# from .models import Book, Author, BookInstance, Genre
global stat, dat

def open_all():
    global stat, dat

    # with open(r'C:\GitHub\snmpvs\stat.json', 'rb') as f:
    #     stat = json.load(f)
    # with open(r'C:\GitHub\snmpvs\dat.json', 'rb') as f:
    #     dat = json.load(f)

    with open(r'C:\Users\podkopaev.k\PycharmProjects\snmpvs\stat.json', 'rb') as f:
        stat = json.load(f)
    with open(r'C:\Users\podkopaev.k\PycharmProjects\snmpvs\dat.json', 'rb') as f:
        dat = json.load(f)

def data_monitor():
    return datetime.today().strftime("%H:%M:%S %d/%m/%Y")

def index(request):
    open_all()
    r = 0
    tab = 0
    s = {}
    stat_one = (sorted(dat.items(), key=lambda k: k[1]["region"]))
    for key in stat_one:

        if key[1]["region"] == 0:
            try:
                s[0].append(key[0])
            except:
                s[0] = []
                s[0].append(key[0])
        elif key[1]["region"] == 1:
            try:
                s[1].append(key[0])
            except:
                s[1] = []
                s[1].append(key[0])
        elif key[1]["region"] == 2:
            try:
                s[2].append(key[0])
            except:
                s[2] = []
                s[2].append(key[0])
        elif key[1]["region"] == 3:
            try:
                s[3].append(key[0])
            except:
                s[3] = []
                s[3].append(key[0])
        elif key[1]["region"] == 4:
            try:
                s[4].append(key[0])
            except:
                s[4] = []
                s[4].append(key[0])
        elif key[1]["region"] == 5 or key[1]["region"] == 6:
            try:
                s[5].append(key[0])
            except:
                s[5] = []
                s[5].append(key[0])
        # elif key[1]["region"] == 6:
        #     try:
        #         s[6].append(key[0])
        #     except:
        #         s[6]=[]
        #         s[6].append(key[0])
        elif key[1]["region"] == 7 or key[1]["region"] == 8 or key[1]["region"] == 9:
            try:
                s[7].append(key[0])
            except:
                s[7] = []
                s[7].append(key[0])

    # print(s)

    le = {}
    for l in s:
        le[l] = len(s[l])

    sort = sorted(le.items(), key=lambda k: -k[1])
    # print(sort)
    # print(sort[0][1])
    ll = sort[0][1]
    # for r in sort:
    #     print(s[r[0]])
    #
    i = 0

    tab = {}

    while i < ll:

        try:
            tab[i]
        except:
            tab[i] = []

        for ss in sort:
            try:
#                tab[i].append(s[ss[0]][i])
#                 print(stat[s[ss[0]][i]])
                status(tab[i], stat[s[ss[0]][i]], s[ss[0]][i])
            except:
                tab[i].append("")
        i += 1
    # print(tab)
    kod = tab

    return render(
        request,
        'index.html',
        context={'kod': kod, "time":data_monitor()},
    )

def status(tab, sss, k):
            if sss["status_t1"] == 1:
                ch1 = "🔵"
            elif sss["status_t1"] == 0:
                ch1 = "🔴"
            if sss["status_t2"] == 1:
                ch2 = "🔵"
            elif sss["status_t2"] == 0:
                ch2 = "🔴"
            if dat[str(k)]["ISP1"] == "unassigned":
                ch1 = "⚪"
            if dat[str(k)]["ISP2"] == "unassigned":
                ch2 = "⚪"
            try:
                tab.append([ch1, ch2, k, dat[str(k)]["name"]])
            except:
                tab = []
                tab.append([ch1, ch2, k, dat[str(k)]["name"]])


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

