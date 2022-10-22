# цикл, в котором мы генерируем Dilaogs()
# в цикле получаем данные из монги
# получаем все объекты коллекции
from mongo import MongoFieldsDB

cursor = MongoFieldsDB()
all_fields = cursor.find_all()
print(all_fields)

# python forms/dialog.py
