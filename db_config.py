import mysql.connector
import pandas as pd
import numpy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

DB_USER='root'
DB_PASS='R@ou56206161'
DB_IP='127.0.0.1'
DB_PORT = "3306"
DB_NAME="record"
DB_PLUGIN='mysql_native_password'
TABLE_NAME='records'

db_con = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_IP, database=DB_NAME, auth_plugin=DB_PLUGIN)

db_cursor = db_con.cursor()

##############

db_connection_str = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    DB_USER, DB_PASS, DB_IP, DB_PORT, DB_NAME
)
db_connection = create_engine(db_connection_str)
Session = sessionmaker(bind=db_connection)
session = Session()
db_command = "SELECT * FROM {}".format(TABLE_NAME)
df = pd.read_sql_table(TABLE_NAME, con=db_connection)