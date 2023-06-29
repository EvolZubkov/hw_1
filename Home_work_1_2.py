import zipfile
import pandas as pd
import json
import sqlite3



# открываем файл в формате zip
with zipfile.ZipFile('egrul.json.zip', 'r') as myzip:
    # получаем список имен файлов в архиве
    filenames = myzip.namelist()
    # итерируемся по каждому файлу
    for filename in filenames:
        # читаем содержимое файла в формате JSON
        with myzip.open(filename) as myfile:
            data = pd.read_json(myfile)

            # Подключаемся к базе данных
            connection = sqlite3.connect('hw1.db')
            cursor = connection.cursor()

            # Создаем таблицу, если она не существует
            cursor.execute('''CREATE TABLE IF NOT EXISTS telecom_companies (name TEXT, full_name TEXT, inn TEXT, kpp TEXT, okved TEXT)''')

            # фильтруем данные из файлов
            for idx, row in data.iterrows():
                if 'СвОКВЭД' in row['data']:
                    if 'СвОКВЭДОсн' in row['data']['СвОКВЭД']:
                        okved = row['data']['СвОКВЭД']['СвОКВЭДОсн']['КодОКВЭД']
                        if okved[:2] == '61':
                            new_data = (row['name'], row['full_name'], row['inn'], row['kpp'], okved)

                            # итерируемся по каждому классификатору в файле
                            name = new_data[0]
                            full_name = new_data[1]
                            inn = new_data[2]
                            kpp = new_data[3]
                            okved = new_data[4]
        
                            cursor.execute(f"INSERT INTO telecom_companies (name, full_name, inn, kpp, okved) VALUES (?, ?, ?, ?, ?)", (name, full_name, inn, kpp, okved))   
            # Сохраняем изменения и закрываем соединение с базой данных
            connection.commit()
            connection.close()