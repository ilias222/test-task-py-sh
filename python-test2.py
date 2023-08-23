#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Есть нюанс записи в архив
# записываются вложенные папки 
# по формату полного пути к импортируемой

import requests
import zipfile
import os
import shutil
import datetime
import time
import re

#Загружаем репозиторий
try:
    def download_file(url):
        local_filename = url.split('/')[-1]

        print('Начинаем загрузку репозитория ', str(datetime.datetime.now().time()))

        with requests.get(url, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)

        print('Успешно загружен! ', str(datetime.datetime.now().time()))

        return local_filename
except ConnectionError as e:
    print('Что то пошло не так, при загрузке репозитория ', str(datetime.datetime.now().time()))
    print(e)

filename = download_file(input('Адрес репозитория :') + '/archive/refs/heads/main.zip')


# #Разбираем архив

extract_dir = 'main'
chank_path = '/' + extract_dir

try:
    print('Начало распаковки архива ', str(datetime.datetime.now().time()))
    with zipfile.ZipFile('main.zip') as zf:
        zf.extractall(extract_dir)
    print('Архив распакован ', str(datetime.datetime.now().time()))
except zipfile.BadZipFile as e: 
    print('Ошибка при распаковки архива :' + str(e))


# #Удаляем папки и файлы, оставляем только папку или файл заданный пользователем

try:
    arr_names = os.listdir(path = os.getcwd() + chank_path)
    dir_family = os.listdir(path = os.getcwd() + chank_path)
    patsh_dir = os.getcwd() + chank_path

    # Если архив содержит корневую папку, уточнаем путь и получаем содержание 
    if os.path.isdir(os.getcwd() + chank_path + '/' + arr_names[0]) and len(arr_names) == 1:
        print("Переход в корневую папку " + str(arr_names), str(datetime.datetime.now().time()))
        patsh_dir = os.getcwd() + chank_path + '/' + str(arr_names[0])
        arr_names = os.listdir(path = os.getcwd() + chank_path + '/' + arr_names[0])

    print('Содержание каталога :' + str(arr_names), str(datetime.datetime.now().time()))

# Указываем папку или относительный путь который следует оставить, далее удаляем все
    name_child = input('Введи папку или относительный путь, для импорта : ')

    # Если ввели относительный путь, то раскидываем 
    # по родительской папке и меняем имя папки в переменной
    if name_child.find('/') > 0:
        arr_names = os.listdir(patsh_dir + '/' + name_child)
        srt = name_child.split('/')
        patsh_dir = patsh_dir + '/' + srt[0]
        name_child = srt[1]

    for item in arr_names:
        if os.path.isfile(patsh_dir + item) and item != name_child:
            print('Это файл на удаление : ' + item, str(datetime.datetime.now().time()))
            os.remove(patsh_dir + item)
            print('Файл удален ', str(datetime.datetime.now().time()))
        

        if os.path.isdir(patsh_dir + item) and item != name_child:
            try:
                print('Это каталог на удаление: ' + item, str(datetime.datetime.now().time()))
                os.rmdir(patsh_dir + item)
                print('Каталог удален ', str(datetime.datetime.now().time()))
            except OSError as e:
                shutil.rmtree(patsh_dir + item)
                print('Каталог не пуст, каталог удален ', str(datetime.datetime.now().time()))

    
except FileNotFoundError as e:
    print('Заданный путь файла или каталога не существует :' + str(e), str(datetime.datetime.now().time()))

# Создаем файл версии или перезаписываем имеющийся

versionBild = input('Версия сборки : ')

def extract_filenames(list):
    filenames = []
    pattern = r"\b\w+\.(js|py)\b"
    for elem in list:    
        if re.findall(pattern, elem) :
            filenames.append(elem)

    return filenames

nim = extract_filenames(os.listdir(path=patsh_dir + '/' + name_child))
service_file = open(patsh_dir + '/' + name_child + '/version.json', 'w')
service_file.write(
'{ \n' 
+ '"name": "hello world", \n \
"version": "' + versionBild +'", \n \
"files": ' 
+ str(nim).replace("'", '"') 
+ ' \n }'
                   )
service_file.close()
print('Запись файла версии ' + str(datetime.datetime.now().time()))


# Записываем архив. Удаляем загруженный репозиторий и папку

dat = datetime.datetime.now().date()
form_dat = datetime.datetime.strftime(dat, '%d-%m-%Y')
print(form_dat)
with zipfile.ZipFile(name_child + str(form_dat).replace('-', '') + '.zip', "w") as myzip:
    arr_names = os.listdir(patsh_dir + '/' + name_child)
    for item in arr_names:
        path = os.path.join(patsh_dir + '/' + name_child, item)
        print("Запись в архив :" + path + " :" + str(datetime.datetime.now().time()))
        if os.path.isdir(path):
            print('Это папка')
            child_dir = os.listdir(path)
            for it in child_dir:
                print('Запись вложенной папки. Файл :' + it + ' :' + str(datetime.datetime.now().time()))
                myzip.write(path + '/' + it)
        
        myzip.write(path)

print('Удаление созданных каталогов через 5 секунд' + str(datetime.datetime.now().time()))
time.sleep(5)
shutil.rmtree(os.getcwd() + chank_path)
os.remove(os.getcwd() + '/' + 'main.zip')
print('Удалено ' + str(datetime.datetime.now().time()))
