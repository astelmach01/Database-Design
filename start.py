from main import run
import pymysql

host = 'localhost'
user = 'root'
password = 'Mamaitato345'
db = 'esleague'

conn = pymysql.connect(host=host, user=user, password=password, db=db)

run(conn)
