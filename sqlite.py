import sqlite3

connection=sqlite3.connect("student.db")

cursor=connection.cursor()

table_info="""
create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

cursor.execute('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Alice', 'Data Science', 'A', 88)''')
cursor.execute('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Bob', 'Data Science', 'B', 75)''')
cursor.execute('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Charlie', 'Data Science', 'A', 92);''')
cursor.execute('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Diana', 'DevOPS', 'C', 81);''')
cursor.execute('''INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Ethan', 'DevOPS', 'B', 89);''')

print("The inserted records are : ")
data=cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
      print(row)
      
connection.commit()
connection.close()
