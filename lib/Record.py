import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor

class Record:
    """A class for story specific record information"""

    def __init__(self,  business_code: str, document_code: str, full_serial_number: str, status: str, title: str, custodian: str, revision: str, \
                link: str, sow_no: str, issue_date: str, effective_date: str, reaffirmation_date: str, protection_lvl:str, ec_technical_data: str, \
                permit: str, ecl: str, eccn: str, usml: str, cg: str, us_exemption: str, ca_exemption: str, exp_date: str, summary: str):
        self.business_code       = business_code
        self.document_code       = document_code
        self.full_serial_number  = full_serial_number
        self.status              = status
        self.title               = title
        self.custodian           = custodian
        self.revision            = revision
        self.link                = link
        self.sow_no              = sow_no
        self.issue_date          = issue_date
        self.effective_date      = effective_date
        self.reaffirmation_date  = reaffirmation_date
        self.protection_lvl      = protection_lvl
        self.ec_technical_data   = ec_technical_data
        self.permit              = permit
        self.ecl                 = ecl
        self.eccn                = eccn
        self.usml                = usml
        self.cg                  = cg
        self.us_exemption        = us_exemption
        self.ca_exemption        = ca_exemption
        self.exp_date            = exp_date
        self.summary             = summary

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

    sql = "INSERT INTO records (business_series_index, business_code, document_code, full_serial_number, status, title, custodian, revision, \
          link, sow_no, issue_date, effective_date, reaffirmation_date, protection_lvl, ec_technical_data, permit, ecl, eccn, usml, cg, us_exemption, \
          ca_exemption, exp_date, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
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
    db_cursor.execute("SELECT business_code, document_code, full_serial_number, status, title, custodian, revision, link, sow_no, issue_date, effective_date, \
                      reaffirmation_date, protection_lvl, ec_technical_data, permit, ecl, eccn, usml, cg, us_exemption, ca_exemption, exp_date, summary  FROM \
                      records WHERE full_serial_number=" + str(serial_number))
    myresult = db_cursor.fetchone()
    
    my_record = Record(business_code = myresult[0], document_code = myresult[1], full_serial_number = myresult[2], status = myresult[3], title = myresult[4], custodian = myresult[5], \
                       revision = myresult[6], link = myresult[7], sow_no = myresult[8], issue_date = myresult[9], effective_date = myresult[10], reaffirmation_date = myresult[11], \
                       protection_lvl = myresult[12], ec_technical_data = myresult[13], permit = myresult[14], ecl = myresult[15], eccn = myresult[16], usml = myresult[17], \
                       cg = myresult[18], us_exemption = myresult[19], ca_exemption = myresult[20], exp_date = myresult[21], summary = myresult[22])
    return my_record

def ReadAllRecords(db_cursor: MySQLCursor):
    records_list = []
    db_cursor.execute("SELECT business_code, document_code, full_serial_number, status, title, custodian, revision, link, sow_no, issue_date, effective_date, \
                      reaffirmation_date, protection_lvl, ec_technical_data, permit, ecl, eccn, usml, cg, us_exemption, ca_exemption, exp_date, summary FROM records")
    myresult = db_cursor.fetchall()
    
    for result in myresult:
        record = Record(business_code = result[0], document_code = result[1], full_serial_number = result[2], status = result[3], title = result[4], \
                        custodian = result[5], revision = result[6], link = result[7], sow_no = result[8], issue_date = result[9], effective_date = result[10], \
                        reaffirmation_date = result[11], protection_lvl = result[12], ec_technical_data = result[13], permit = result[14], \
                        ecl = result[15], eccn = result[16], usml = result[17], cg = result[18], us_exemption = result[19], ca_exemption = result[20], \
                        exp_date = result[21], summary = result[22])
        
        records_list.append(record)

    return records_list

def ReadRecordsFromType(db_cursor: MySQLCursor, business_code: int, document_code: int):
    records_list = []
    sql = "SELECT business_code, document_code, full_serial_number, status, title, custodian, revision, link, sow_no, issue_date, effective_date, \
          reaffirmation_date, protection_lvl, ec_technical_data, permit, ecl, eccn, usml, cg, us_exemption, ca_exemption, exp_date, summary FROM \
          records WHERE business_code=%s AND document_code=%s"
    values = (str(business_code), str(document_code))
    db_cursor.execute(sql, values)
    records_tuple = db_cursor.fetchall()

    for result in records_tuple:
        record = Record(business_code = result[0], document_code = result[1], full_serial_number = result[2], status = result[3], title = result[4], \
                        custodian = result[5], revision = result[6], link = result[7], sow_no = result[8], issue_date = result[9], effective_date = result[10], \
                        reaffirmation_date = result[11], protection_lvl = result[12], ec_technical_data = result[13], permit = result[14], \
                        ecl = result[15], eccn = result[16], usml = result[17], cg = result[18], us_exemption = result[19], ca_exemption = result[20], \
                        exp_date = result[21], summary = result[22])
        
        records_list.append(record)

    return records_list

def UpdateRecord(db_connection: MySQLConnection, record: Record):

    db_cursor = db_connection.cursor()
    sql = "UPDATE records SET status=%s, title=%s, custodian=%s, revision=%s, link=%s, sow_no=%s, \
          issue_date=%s, effective_date=%s, reaffirmation_date=%s, protection_lvl=%s, ec_technical_data=%s, permit=%s, ecl=%s, eccn=%s, usml=%s, cg=%s, \
          us_exemption=%s, ca_exemption=%s, exp_date=%s, summary=%s WHERE full_serial_number = %s"
    values = (record.status, record.title, record.custodian, record.revision, record.link, record.sow_no, record.issue_date, record.effective_date,\
              record.reaffirmation_date, record.protection_lvl, record.ec_technical_data, record.permit, record.ecl, record.eccn, record.usml, record.cg, \
              record.us_exemption, record.ca_exemption, record.exp_date, record.summary, record.full_serial_number)
    db_cursor.execute(sql,values)
    db_connection.commit()

def DeleteRecord(db_connection: MySQLConnection, document_code:int):
    db_cursor = db_connection.cursor()
    sql = "DELETE FROM records WHERE full_serial_number="+str(document_code)
    db_cursor.execute(sql)
    db_connection.commit()