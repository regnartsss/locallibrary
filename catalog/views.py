from django.shortcuts import render
import json
import os
from datetime import datetime, timedelta
# Create your views here.
# from .models import Book, Author, BookInstance, Genre
global stat, dat

def open_all():
    global stat, dat

    with open(r'C:\Users\podkopaev.k\PycharmProjects\snmpvs\stat.json', 'rb') as f:
        stat = json.load(f)
    with open(r'C:\Users\podkopaev.k\PycharmProjects\snmpvs\dat.json', 'rb') as f:
        dat = json.load(f)

def data_monitor():
    return datetime.today().strftime("%H:%M:%S %d/%m/%Y")

def index(request):
    open_all()

    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
#    print(len(stat))
    column = (int(len(stat)/5))+2
    print("строчек %s" % column)
    r =0
    tab = 0
    s = {}
    #
    col = [5,10,15,20,25,30]
    for k, v in stat.items():
            if v["status_t1"] == 1:
                ch1 = "🔵"
            elif v["status_t1"] == 0:
                ch1 = "🔴"
            if v["status_t2"] == 1:
                ch2 = "🔵"
            elif v["status_t2"] == 0:
                ch2 = "🔴"
            try:
                s[tab].append([k, dat[str(k)]["name"], ch1, ch2])
            except:
                s[tab] = []
                s[tab].append([k, dat[str(k)]["name"], ch1, ch2])
            r += 1
            if r in col:
                tab += 1
            # s[k].append("kod": k,"name": dat[str(k)]["name"], "st1": ch1, "st2": ch2)
        #     r+=1
        #     print(s)
    kod = s

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'kod': kod, "time":data_monitor()},
    )
