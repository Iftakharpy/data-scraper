import sqlite3
import random
connection = sqlite3.connect('test.db') #if test.db exists then connect to it else create test.db and connect to it
db_cursor = connection.cursor() #creating cursor to execute sql commands


#creating TABLE 'test_table'
# db_cursor.execute("CREATE TABLE test_table (usr_id INT, usr_name TEXT, usr_age INT);")
"""
for i in range(41,61):
    #letters that can be in the random text
    letters='abcdefghijklmnopqrstuvwxyz'
    for i in range(8):
        string_interpulation = 'string_interpulation:'
        built_in_query = 'Built_In_Query:'

        lst = [x for x in string_interpulation]
        for i in range(random.randint(5,10)):
            lst.append(random.choice(letters))
    #generated random text
    random_text = ''.join(lst)
    
    #wrong way string interpulation is VAULNARABLE TO SQL INJECTION!
    '''#inserting the random record to the Python db for 20 times
    query = f"INSERT INTO test_table Values({i},'{random_text}',{random.randint(10,50)});" #with string interpulation
    db_cursor.execute(query)
    '''

    #correct way NOT VAULNARABLE TO SQL INJECTION!
    '''#inserting the random record to the Python db for 20 times
    query = "INSERT INTO test_table VALUES(?,?,?)" #without string interpulation
    db_cursor.execute(query,(i,random_text,random.randint(10,50)))
    '''
"""

#inserting lots of data at once
'''# data_set=[(100,'a',1),(101,'b',2),(102,'c',3),(103,'d',4),(104,'e',5),(105,'f',6)]
data_set = [(i+100,f'data_set tuple {i}',i) for i in range(26)]
query = "INSERT INTO test_table VALUES(?,?,?)" #without string interpulation
db_cursor.executemany(query,data_set)
'''

query = "SELECT * FROM test_table WHERE usr_name NOT LIKE 'string%'; --AND usr_name NOT LIKE 'Built%' AND usr_name NOT LIKE 'data%' ORDER BY usr_age ASC;"
db_cursor.execute(query)
db_cursor.fetchone() #returns the first record as a tuple
db_cursor.fetchall() #returns all record as list as tuples


connection.commit() #commiting changes to the database
connection.close() #closing the connection