
from lib.BusinessUnit   import BusinessUnit
from lib.DocumentType   import DocumentType
from lib.Record         import Record
from pprint             import pprint

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor

#Create tables
def create_business_series_table(db_cursor: MySQLCursor):
    series_title = "title VARCHAR(255) NOT NULL UNIQUE "
    business_series_index = "business_series_index INT NOT NULL PRIMARY KEY"
    create_series_table_cmd = "CREATE TABLE business_series (" + series_title + ", "+business_series_index +  ")"

    db_cursor.execute(create_series_table_cmd)

def create_business_unit_table(db_cursor: MySQLCursor):
    title = "title VARCHAR(255) NOT NULL"
    summary = "summary VARCHAR(255)"
    business_code = "business_code INT NOT NULL PRIMARY KEY"
    business_series_index = "business_series_index INT NOT NULL"
    foreign_key_link = "FOREIGN KEY (business_series_index) REFERENCES business_series(business_series_index)"
    create_bu_table_cmd = "CREATE TABLE business_units (" + title + ", " + summary + ", "+ business_code + ", " + business_series_index + ", "+foreign_key_link+ ")"
    db_cursor.execute(create_bu_table_cmd)

def create_document_type_table(db_cursor: MySQLCursor):
    title = "title VARCHAR(255) NOT NULL UNIQUE"
    summary = "summary VARCHAR(255)"
    document_code = "document_code INT NOT NULL PRIMARY KEY"

    create_documenttype_table_cmd = "CREATE TABLE document_types (" + title + ", " + summary + ", "+ document_code + ")"
    db_cursor.execute(create_documenttype_table_cmd)

def create_records_table(db_cursor: MySQLCursor):
    business_series_index = "business_series_index INT NOT NULL"
    business_code       = "business_code INT NOT NULL"
    document_code       = "document_code INT NOT NULL"
    full_serial_number  = "full_serial_number INT NOT NULL PRIMARY KEY"
    title               = "title VARCHAR(255) NOT NULL UNIQUE"
    summary             = "summary VARCHAR(255)"

    foreign_key_business    = "FOREIGN KEY (business_code) REFERENCES business_units(business_code)"
    foreign_key_document    = "FOREIGN KEY (document_code) REFERENCES document_types(document_code)"
    foreign_key_series      = "FOREIGN KEY (business_series_index) REFERENCES business_series(business_series_index)"
    
    create_record_table_cmd = "CREATE TABLE records (" + business_series_index + ", " + business_code + ", " + document_code
    create_record_table_cmd = create_record_table_cmd + ", " + full_serial_number + ", " + title + ", " + summary
    create_record_table_cmd = create_record_table_cmd + ", " + foreign_key_business + ", " + foreign_key_document + ", " + foreign_key_series + ")"

    db_cursor.execute(create_record_table_cmd)

def create_documents_table(db_cursor: MySQLCursor):
    title = "title VARCHAR(255) NOT NULL PRIMARY KEY"
    document_path = "document_path VARCHAR(255) NOT NULL UNIQUE"
    full_serial_number  = "full_serial_number INT NOT NULL"
    business_code       = "business_code INT NOT NULL"
    document_code       = "document_code INT NOT NULL"

    foreign_key_business    = "FOREIGN KEY (business_code) REFERENCES business_units(business_code)"
    foreign_key_document    = "FOREIGN KEY (document_code) REFERENCES document_types(document_code)"
    foreign_key_serial    = "FOREIGN KEY (full_serial_number) REFERENCES records(full_serial_number)"

    create_document_table_cmd = "CREATE TABLE document_files (" + title + ", " + document_path + ", " + full_serial_number
    create_document_table_cmd = create_document_table_cmd + ", " + business_code + ", " + document_code
    create_document_table_cmd = create_document_table_cmd + ", " + foreign_key_business + ", " + foreign_key_document  + ", " + foreign_key_serial + ")"
    db_cursor.execute(create_document_table_cmd)

#general helpers
def show_all_entries(db_cursor: MySQLCursor, table_name: str ):
    print(table_name)
    db_cursor.execute("SELECT * FROM " + table_name)
    myresult = db_cursor.fetchall()

    for x in myresult:
      print(x)

def show_tables(db_cursor: MySQLCursor):
    db_cursor.execute("SHOW TABLES")
    myresult = db_cursor.fetchall()
    for x in myresult:
        print(x)

def describe_tables(db_cursor: MySQLCursor, table_name: str ):
    db_cursor.execute("DESCRIBE " + table_name)
    myresult = db_cursor.fetchall()
    for x in myresult:
        print(x)

def prepare_business_series(db_connection: MySQLConnection ):
    
    db_cursor = db_connection.cursor()
    sql = "INSERT INTO business_series (business_series_index, title) VALUES (%s, %s)"
    val = [
    ('10', 'Corporate'),
    ('20', 'Export Controls'),
    ('30', 'Project Controls'),
    ('40', 'Engineering'),
    ('50', 'Operations'),
    ('60', 'IT'),
    ('70', 'QMS'),
    ('80', 'unassigned'),
    ('90', 'Office General')
    ]

    db_cursor.executemany(sql, val)
    db_connection.commit()

def prepare_document_types(db_connection: MySQLConnection):

    db_cursor = db_connection.cursor()
    sql = "INSERT INTO document_types (document_code, title, summary) VALUES (%s, %s, %s)"
    val = [
    ('0', 'Template', 'NA'),
    ('01', 'Manuals/Policies', 'NA'),
    ('02', 'Workflow', 'NA'),
    ('03', 'Process/Procedure', 'NA'),
    ('04', 'Work Instruction', 'NA'),
    ('05', 'Form/Checklist', 'NA'),
    ('06', 'Presentation', 'NA'),
    ('07', 'Specification', 'NA'),
    ('08', 'Report', 'NA'),
    ('09', 'Drawing', 'NA'),
    ('10', 'Cover Sheet', 'NA'),
    ('97', 'Logs', 'NA'),
    ('98', 'Emails and Communication Records', 'NA'),
    ('99', 'Non-Communication Records', 'NA')
    ]

    db_cursor.executemany(sql, val)
    db_connection.commit()

##########################################
#CRUD for Business Unit
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
    print(myresult)
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

def UpdateBusinessUnit(db_connection: MySQLCursor, business_unit:int):

    db_cursor = db_connection.cursor()
    sql = "UPDATE business_units SET title=%s,summary=%s WHERE business_code = %s",
    values = (business_unit.title, business_unit.summary, business_unit.specific_code)
    db_cursor.execute(sql,values)
    db_connection.commit()

def DeleteBusinessUnit(db_connection: MySQLConnection, business_code: int):
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM business_units WHERE business_code="+str(business_code)
    db_cursor.execute(sql)
    db_connection.commit()

#####################################################################################
#CRUD for Document types
#title = "title VARCHAR(255) NOT NULL, "
#    summary = "summary VARCHAR(255), "
#    document_code = "document_code INT NOT NULL UNIQUE, "
def CreateNewDocumentType(db_connection: MySQLConnection, document_code:int, title:str, summary:str ="NA" ):
 
    db_cursor = db_connection.cursor()

    sql = "INSERT INTO document_types (document_code, title, summary) VALUES (%s, %s, %s) "
    value = (str(document_code), title, summary)
    db_cursor.execute(sql, value)
    db_connection.commit()

def ReadDocumentType(db_cursor: MySQLCursor, document_code:int):
    db_cursor.execute("SELECT document_code, title, summary  FROM document_types WHERE document_code=" + str(document_code))
    myresult = db_cursor.fetchone()
    
    my_document = DocumentType(document_code = myresult[0], title = myresult[1], summary = myresult[2])
    return my_document

def ReadAllDocumentTypes(db_cursor: MySQLCursor):
    document_type_list = []
    db_cursor.execute("SELECT document_code, title, summary FROM document_types")
    documents_tuple = db_cursor.fetchall()

    for document_type_entry in documents_tuple:
        document_code = document_type_entry[0]
        title = document_type_entry[1]
        summary = document_type_entry[2]
        doctype = DocumentType(document_code = document_code, title = title, summary = summary)
        
        document_type_list.append(doctype)

    return document_type_list

def UpdateDocumentType(db_connection: MySQLConnection, db_cursor: MySQLCursor, document_type: DocumentType):

    sql = "UPDATE business_units SET title=%s, summary=%s WHERE document_code = %s"
    values = (document_type.title, document_type.summary, document_type.document_code)
    db_cursor.execute(sql,values)
    db_connection.commit()

def DeleteDocumentType(db_connection: MySQLConnection, document_code:int):
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM document_types WHERE document_code="+str(document_code)
    db_cursor.execute(sql)
    db_connection.commit()


#####################################################################################
#CRUD for records
#business_series_index = "business_series_index INT NOT NULL"
#    business_code       = "business_code INT NOT NULL"
#    document_code       = "document_code INT NOT NULL"
#    full_serial_number  = "full_serial_number int NOT NULL PRIMARY KEY"
#    title               = "title VARCHAR(255) NOT NULL UNIQUE"
#    summary             = "summary VARCHAR(255)"
def CreateNewRecord(db_connection: MySQLConnection, serial_number:int, title:str, summary:str ="NA" ):
 
    db_cursor = db_connection.cursor()
    str_code = str(serial_number)
    business_series = str_code[0]+"0"
    business_code = str_code[0:2]
    document_code = str_code[2:4]

    sql = "INSERT INTO records (business_series_index, business_code, document_code, full_serial_number, title, summary) VALUES (%s, %s, %s, %s, %s, %s) "
    value = (business_series, business_code, document_code, str_code, title, summary)
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


####
#EXECUTE area for testing
#db_cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=N'records'")
mydb = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1', database="mydatabase",
                              auth_plugin='mysql_native_password')

db_cursor = mydb.cursor()
#CreateNewDocument(mydb, "Test Document Path", 21081111, "A test title")
#prepare_business_series(mydb)

# describe_tables(db_cursor, "business_units")

class BusinessType:
    def __init__(self, title, summary, business_code):
        self.title = title
        self.summary = summary
        self.business_code = business_code

class DocumentType:
    def __init__(self, title, summary, document_code):
        self.title = title
        self.summary = summary
        self.document_code = document_code

# document_type = DocumentType('Export Controls', 'NA', '21')
# UpdateDocumentType(mydb, db_cursor, document_type)
# print("----------------------------")
# describe_tables(db_cursor, 'business_units')
# print("----------------------------")

# show_all_entries(db_cursor,"documents_units")

# show_tables(db_cursor)

# CreateNewBusinessUnit(mydb, 'Training', '21')

show_all_entries(db_cursor,"business_units")