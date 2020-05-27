import sqlite3

connection = sqlite3.connect('Products_in_shops_from_Evaly.db')
print(connection)
print(connection)
print('creating cursor on sqlite3')
db_cursor = connection.cursor()
print(db_cursor)
print(db_cursor.description)

table_name = 'table1'