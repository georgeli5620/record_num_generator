import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pprint import pprint

import lib.BusinessUnit
import lib.DocumentType
import lib.Record

from lib.BusinessUnit import BusinessUnit
from lib.DocumentType import DocumentType
from lib.Record import Record

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor
# from SQLTesting import show_all_entries

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

################
#set up the database
mydb = mysql.connector.connect(user='root', password='password',
                              host='127.0.0.1', database="mydatabase",
                              auth_plugin='mysql_native_password')

db_cursor = mydb.cursor()

app = dash.Dash(__name__)# external_stylesheets=external_stylesheets)

bs_dropdown = []
business_series = lib.BusinessUnit.ReadAllBusinessSeries(db_cursor)
for bs in business_series:
    bs_dropdown.append({'label':str(bs.specific_code)+ " - "+bs.title, 'value':bs.specific_code})

bu_dropdown = []
business_units = lib.BusinessUnit.ReadAllBusinessUnits(db_cursor)
for bu in business_units:
    bu_dropdown.append({'label':str(bu.specific_code)+ " - "+bu.title, 'value':bu.specific_code})

doc_types_dropdown =[]
doc_types = lib.DocumentType.ReadAllDocumentTypes(db_cursor)
for dt in doc_types:
    doc_types_dropdown.append({'label':str(dt.document_code).zfill(2)+ " - "+dt.title, 'value':dt.document_code})

records_dropdown = []
records = lib.Record.ReadAllRecords(db_cursor)
largest_serial = max(records, key=lambda rec: rec.full_serial_number )

for rec in records:
    records_dropdown.append({'label':str(rec.full_serial_number)+ " - "+rec.title, 'value':rec.full_serial_number})



####
#Setup the layout
app.layout = html.Div([
    html.H3("Document Number"),

    html.Div([
        html.P("Record Number"),
        dcc.Input(
            id='full-serial-num',
            type = 'number',
            max = "99999",
            disabled=True
        )
        ],
                style={'marginBottom': 25,
                       'marginTop': 195,
                       'marginLeft':'5%',
                       'marginRight':'5%',
                       'width': '40%',
                       'float':'right',
                       'background-color':'#ffffff',
                       'text-align':'center',
                       'vertical-align':'middle'
                       }),

    html.Div([
       html.P("Business Series"),
       dcc.Dropdown(
           id = 'business-series-dropdown',
           options=bs_dropdown,
           value=''
    )
    ], style={'marginBottom': 25, 'marginTop': 25, 'width': '40%'}),

    html.Div([
        html.P("Business Units"),
        dcc.Dropdown(
            id = 'business-unit-dropdown',
            options=bu_dropdown,
            value=''
    )
    ], style={'marginBottom': 25, 'marginTop': 25, 'width': '40%'}),

    html.Div([
        html.P("Document Types"),
        dcc.Dropdown(
            id = 'document-type-dropdown',
            options = doc_types_dropdown,
            value = ''
    )
    ], style={'marginBottom': 25, 'marginTop': 25, 'width': '40%'}),

    html.Div([
        html.P("Serial Numbers"),
        dcc.Input(
            id='serial-text-input',
            disabled=True
        )
    ], style={'marginBottom': 25, 'marginTop': 25, 'width': '40%'}),
])

####
#Set up callbacks
########################
@app.callback(
    Output('full-serial-num', 'value'),
    [Input('business-unit-dropdown', 'value'),
    Input('document-type-dropdown', 'value'),
    Input('serial-text-input', 'value')])
def update_output_div(input_business_unit, input_document_type, input_serial_text):
    if input_business_unit and input_document_type and input_serial_text:
        leading_zeros_document_type = str(input_document_type).zfill(2)
        leading_zeros_serial_text = str(input_serial_text).zfill(5)
        result = str(input_business_unit) + leading_zeros_document_type + leading_zeros_serial_text
        return result

@app.callback(
    Output('business-unit-dropdown', 'options'),
    [Input('business-series-dropdown', 'value')])
def update_business_unit_dropdown(input_value):
    bu_dropdown = []
    if input_value:
        business_units = lib.BusinessUnit.ReadBusinessUnitsByCode(db_cursor, str(input_value))
        for bu in business_units:
            bu_dropdown.append({'label':str(bu.specific_code)+ " - "+bu.title, 'value':bu.specific_code})
    return bu_dropdown

@app.callback(
    Output('serial-text-input', 'value'),
    [Input('business-unit-dropdown', 'value'),
    Input('document-type-dropdown', 'value')])
def update_serial_text_input(input_business_unit, input_document_type):
    records_list = []
    result = ''
    if input_business_unit and input_document_type:
        if len(str(input_document_type)) < 2:
            input_document_type_str = '0' + str(input_document_type)
        records_list = lib.Record.ReadRecordsFromType(db_cursor, input_business_unit, input_document_type)
        len_of_records = len(records_list)+1
        result = str(len_of_records).zfill(5)
    return result


# def UpdateRecords(business_code, document_code):

#     records_dropdown = []
#     records = lib.Record.ReadRecordsFromType(db_cursor, business_code, document_code)
#     #largest_serial = max(records, key=lambda rec: rec.full_serial_number )

#     for rec in records:
#         records_dropdown.append({'label':str(rec.full_serial_number)+ " - "+rec.title, 'value':rec.full_serial_number})

#     return records_dropdown

#@app.callback([Output],[Input])
#def CalculateNextSerial():
#    pass


##############################
#@app.callback([Output],[Input])
#def AddNewBU():
#    pass

#@app.callback([Output],[Input])
#def ModifyBU():
#    pass

############################
#@app.callback([Output],[Input])
#def AddNewDocType():
#    pass

#@app.callback([Output],[Input])
#def ModifyDocType():
#    pass

############################
#@app.callback([Output],[Input])
#def AddNewRecord():
#    pass

#@app.callback([Output],[Input])
#def ModifyRecord():
#    pass

if __name__ == '__main__':
    app.run_server(debug=True)