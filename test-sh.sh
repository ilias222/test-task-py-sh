#! bin/bash
''' Найти сервисы, изменить их дирректории и параметры 
    WorkingDirectory, ExecStart
'''


echo Ввод части или имени юнита
read unit_chunk_name                #Ввод части или имени юнита
echo Ввод директории юнита
read unit_path_dir                  #Путь к сервису
echo Новая директория юнита
read unit_path_new                  #Новый путь к сервису
echo параметры для ExecStart
read randomn_paramets               #Произвольный параметр для ExecStart


#Получаем скписок юнитов
#Ищет только сервисы

unit_list=$(systemctl list-unit-files | grep -E '^'$unit_chunk_name'[a-z|-]*[.]+service')


# Заполняем именами сервисов переменную

for elem in $unit_list ; do 
if [[ $(echo $elem | grep $unit_chunk_name) ]]; 
then 
unit_list_service+=$(echo " $elem")
fi
done


# Останавливаем сервисы

for elem in $unit_list_service ; do 
echo $elem "---GO Stop"
sudo systemctl stop $elem
echo $elem "---OK"
done


# Изменяем пути в WorkingDirectory и ExecStart

for elem in $unit_list_service ; do
sudo sed -i "s|WorkingDirectory=.*|WorkingDirectory=-$unit_path_new/$elem|g" "$unit_path_dir/$elem"
sudo sed -i "s|ExecStart=.*|ExecStart=-$unit_path_new/$elem/foobar-deamon  $randomn_paramets" "$unit_path_dir/$elem"
done


# Переносим сервисы в другую директорию

for elem in $unit_list_service ; do
sudo mv $unit_path_dir/$elem $unit_path_new
sudo more $unit_path_new/$elem
done


# Запуск сервисов

for elem in $unit_list_service ; do 
echo $elem "---GO Start"
sudo systemctl start $elem
echo $elem "---OK"
done