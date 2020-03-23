import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor

class Record:
    """A class for story specific record information"""

    def __init__(self,  business_code: str, document_code: str, full_serial_number: str, title: str, summary: str, 
                        document_path_list: list = []):
        self.business_code       = business_code
        self.document_code       = document_code
        self.full_serial_number  = full_serial_number
        self.title               = title
        self.summary             = summary
        self.document_path_list  = document_path_list

#CRUD for records
#business_series_index = "business_series_index INT NOT NULL"
#    business_code       = "business_code INT NOT NULL"
#    document_code       = "document_code INT NOT NULL"
#    full_serial_number  = "full_serial_number int NOT NULL PRIMARY KEY"
#    title               = "title VARCHAR(255) NOT NULL UNIQUE"
#    summary             = "summary VARCHAR(255)"
def CreateNewRecord(db_connection: MySQLConnection,
                    serial_number:int,
                    status:str,
                    title:str,
                    record_custodian_state:str,
                    record_revision_state:str,
                    record_link_state:str,
                    record_sow_state:str,
                    record_issue_date_state:str,
                    record_effective_date_state:str,
                    record_reaffirmation_date_state:str,
                    record_protection_lvl_state:str,
                    record_ec_state:bool,
                    record_permit_state:str,
                    record_ecl_state:str,
                    record_eccn_state:str,
                    record_usml_state:str,
                    record_cg_state:str,
                    record_us_exemption_state:str,
                    record_ca_exemption_state:str,
                    record_exp_date_state:str,
                    summary:str ="NA" ):
 
    db_cursor = db_connection.cursor()
    str_code = str(serial_number)
    business_series = str_code[0]+"0"
    business_code = str_code[0:2]
    document_code = str_code[2:4]

    sql = "INSERT INTO records (business_series_index, business_code, document_code, full_serial_number, status, title, custodian, revision, link, sow_no, issue_date, effective_date, reaffirmation_date, protection_lvl, ec_technical_data, permit, ecl, eccn, usml, cg, us_exemption, ca_exemption, exp_date, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
    value = (business_series,
             business_code,
             document_code,
             str_code,
             status,
             title,
             record_custodian_state,
             record_revision_state,
             record_link_state,
             record_sow_state,
             record_issue_date_state,
             record_effective_date_state,
             record_reaffirmation_date_state,
             record_protection_lvl_state,
             record_ec_state,
             record_permit_state,
             record_ecl_state,
             record_eccn_state,
             record_usml_state,
             record_cg_state,
             record_us_exemption_state,
             record_ca_exemption_state,
             record_exp_date_state, 
             summary)
    db_cursor.execute(sql, value)
    db_connection.commit()

def ReadRecord(db_cursor: MySQLCursor, serial_number:int):
    db_cursor.execute("SELECT full_serial_number, title, business_code, document_code, summary  FROM records WHERE full_serial_number=" + str(serial_number))
    myresult = db_cursor.fetchone()
    
    my_record = Record(full_serial_number = myresult[0], title = myresult[1], business_code = myresult[2], document_code = myresult[3], summary = myresult[4])
    return my_record

def ReadAllRecords(db_cursor: MySQLCursor):
    records_list = []
    db_cursor.execute("SELECT full_serial_number, title, business_code, document_code, summary  FROM records")
    records_tuple = db_cursor.fetchall()

    for result in records_tuple:
        record = Record(full_serial_number = result[0], title = result[1], business_code = result[2], document_code = result[3], summary = result[4])
        
        records_list.append(record)

    return records_list

def ReadRecordsFromType(db_cursor: MySQLCursor, business_code: int, document_code: int):
    records_list = []
    sql = "SELECT full_serial_number, title, business_code, document_code, summary  FROM records WHERE business_code=%s AND document_code=%s"
    values = (str(business_code), str(document_code))
    db_cursor.execute(sql, values)
    records_tuple = db_cursor.fetchall()

    for result in records_tuple:
        record = Record(full_serial_number = result[0], title = result[1], business_code = result[2], document_code = result[3], summary = result[4])
        
        records_list.append(record)

    return records_list

def UpdateRecord(db_connection: MySQLConnection, record: Record):

    db_cursor = db_connection.cursor()
    sql = "UPDATE records SET title=%s, summary=%s WHERE full_serial_number = %s"
    values = (record.title, record.summary, record.full_serial_number)
    db_cursor.execute(sql,values)
    db_connection.commit()

def DeleteRecord(db_connection: MySQLConnection, document_code:int):
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM records WHERE full_serial_number="+str(document_code)
    db_cursor.execute(sql)
    db_connection.commit()