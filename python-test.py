#! /usr/bin/env python
# -*- coding: utf-8 -*-

import requests  
import datetime

startRequest = datetime.datetime.now()

def reqAPI():
    try:
        return requests.get("http://worldtimeapi.org/api/timezone/Europe/Moscow")
    except ConnectionError as e:
        print("\n Что то пошло не так, при обращении к АПИ! \n")
        print(e)


raw = reqAPI().json()
timezone = raw['timezone']
timeReqest = str(raw['datetime'])
timeReqest2 = datetime.datetime.strptime(timeReqest[:22], "%Y-%m-%dT%H:%M:%S.%f")

print("\n Вывод в сыром виде : \n", str(raw))
print("\n Вывод название временной зоны : \n", timezone)
print("\n Дельта времени вызова API \n", str(timeReqest2 - startRequest))

i = 0
l = []
while i < 5:
    startRequest = datetime.datetime.now()
    distTime = reqAPI().json()
    timezone = distTime['timezone']
    timeReqest = str(distTime['datetime'])
    timeReqest2 = datetime.datetime.strptime(timeReqest[:22], "%Y-%m-%dT%H:%M:%S.%f")
    l.append(float(timeReqest2.timestamp() - startRequest.timestamp()))
    i = i+1

print("\n Среднее значение ответа API : \n", str(sum(l) / 5))
