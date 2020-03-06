import operator
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor

class BusinessSeries:

    def __init__(self, specific_code: str, title: str , records : list = []):
        self.title           = title
        self.specific_code   = specific_code

class BusinessUnit:

    def __init__(self, specific_code: str , summary: str, title:str, records : list = []):
        self.specific_code  = specific_code
        self.records        = records
        self.summary        = summary
        self.title          = title    

def CreateNewBusinessUnit(db_connection: MySQLConnection, title:str, code:int, summary: str = "NA"):
 
    db_cursor = db_connection.cursor()
    str_code = str(code)
    business_series = str_code[0]+"0"

    sql = "INSERT INTO business_units (title, summary, business_code, business_series_index) VALUES (%s, %s, %s, %s) "
    value = (title, summary, str_code, business_series)
    db_cursor.execute(sql, value)
    db_connection.commit()

def ReadBusinessUnit(db_cursor: MySQLCursor, business_code:int):
    db_cursor.execute("SELECT title, business_code, summary  FROM business_units WHERE business_code=" + str(business_code))
    myresult = db_cursor.fetchone()
    my_bu = BusinessUnit(title = myresult[0], specific_code = myresult[1], summary = myresult[2])
    return my_bu

def ReadAllBusinessUnits(db_cursor: MySQLCursor):
    bu_list = []
    db_cursor.execute("SELECT title, business_code, summary FROM business_units")
    bu_tuple = db_cursor.fetchall()

    for business_unit in bu_tuple:
        title = business_unit[0]
        code = business_unit[1]
        summary = business_unit[2]
        bu = BusinessUnit(specific_code = code, title = title, summary = summary )
        bu_list.append(bu)

    return bu_list

def ReadBusinessUnitsByCode(db_cursor: MySQLCursor, business_series_index:int):
    bu_list = []
    db_cursor.execute("SELECT title, business_code, summary FROM business_units WHERE business_series_index=" + str(business_series_index))
    bu_tuple = db_cursor.fetchall()

    for business_unit in bu_tuple:
        title = business_unit[0]
        code = business_unit[1]
        summary = business_unit[2]
        bu = BusinessUnit(specific_code = code, title = title, summary = summary )
        bu_list.append(bu)

    return bu_list

def ReadAllBusinessSeries(db_cursor: MySQLCursor):
    bs_list = []   
    db_cursor.execute("SELECT business_series_index, title FROM business_series")
    bs_tuple = db_cursor.fetchall()
    sorted_bs_tuple = sorted(bs_tuple, key=lambda tup:tup[0])

    for business_series in sorted_bs_tuple:
        business_series_index = business_series[0]
        title = business_series[1]
        bs = BusinessSeries(specific_code = business_series_index, title = title)
        bs_list.append(bs)

    return bs_list

def UpdateBusinessUnit(db_connection: MySQLConnection, business_unit:int):

    db_cursor = db_connection.cursor()
    sql = "UPDATE business_units SET title=%s,summary=%s WHERE business_code = %s"
    values = (business_unit.title, business_unit.summary, business_unit.specific_code)
    db_cursor.execute(sql,values)
    db_connection.commit()

def DeleteBusinessUnit(db_connection: MySQLConnection, business_code: int):
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM business_units WHERE business_code="+str(business_code)
    db_cursor.execute(sql)
    db_connection.commit()