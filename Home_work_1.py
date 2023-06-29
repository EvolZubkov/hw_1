import zipfile
import json
import sqlite3
import time

# открываем файл в формате zip
with zipfile.ZipFile('okved_2.json.zip', 'r') as myzip:
    # получаем список имен файлов в архиве
    filenames = myzip.namelist()
    # итерируемся по каждому файлу
    for filename in filenames:
        # читаем содержимое файла в формате JSON
        with myzip.open(filename) as myfile:
            data = json.load(myfile)
            
            # Подключаемся к базе данных
            conn = sqlite3.connect('hw1.db')

            # Создаем таблицу, если она не существует
            conn.execute('CERATE TABLE IF NOT EXISTS okved (code TEXT, parent_code TEXT, section TEXT, name TEXT, comment TEXT)')

            # итерируемся по каждому классификатору в файле
            for item in data:
                code = item['code']
                parent_code = item.get('parent_code', '')
                section = item['section']
                name = item['name']
                comment = item.get('comment', '')
    
                conn.execute(f"INSERT INTO okved (code, parent_code, section, name, comment) VALUES ('{code}', '{parent_code}', '{section}', '{name}', '{comment}')")
                #print(item)
            # Сохраняем изменения и закрываем соединение с базой данных
            conn.commit()
            conn.close()

