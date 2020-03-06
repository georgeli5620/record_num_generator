import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor

class DocumentType:
    """A class for storing the DocumentType data"""

    def __init__(self, title: str, document_code: str, summary: str, record_list: list = []):
        self.title              = title
        self.document_code      = document_code
        self.summary            = summary
        self.record_list        = record_list

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

def UpdateDocumentType(db_connection: MySQLConnection, document_type: DocumentType):

    db_cursor = db_connection.cursor()
    sql = "UPDATE document_types SET title=%s, summary=%s WHERE document_code = %s"
    values = (document_type.title, document_type.summary, document_type.document_code)
    db_cursor.execute(sql,values)
    db_connection.commit()

def DeleteDocumentType(db_connection: MySQLConnection, document_code:int):
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM document_types WHERE document_code="+str(document_code)
    db_cursor.execute(sql)
    db_connection.commit()