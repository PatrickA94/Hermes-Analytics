import psycopg2


con = psycopg2.connect(database='hermes', user='flask', host='localhost', password='root')

file = open('proj.sql','r')
file = " ".join(file.readlines())

cur =con.cursor()
cur.execute(file)
