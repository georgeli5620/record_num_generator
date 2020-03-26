import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import lib.BusinessUnit
import lib.DocumentType
import lib.Record

from lib.BusinessUnit import BusinessUnit
from lib.DocumentType import DocumentType
from lib.Record import Record, CreateNewRecord, ReadRecord, UpdateRecord, ReadAllRecords, DeleteRecord

import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor     import MySQLCursor

import pandas as pd
import numpy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

# from SQLTesting import show_all_entries

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

################
DB_USER='root'
DB_PASS='R@ou56206161'
DB_IP='127.0.0.1'
DB_PORT = "3306"
DB_NAME="record"
DB_PLUGIN='mysql_native_password'
TABLE_NAME='records'

mydb = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_IP, database=DB_NAME, auth_plugin=DB_PLUGIN)

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

db_connection_str = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    DB_USER, DB_PASS, DB_IP, DB_PORT, DB_NAME
)
db_connection = create_engine(db_connection_str)
Session = sessionmaker(bind=db_connection)
session = Session()
db_command = "SELECT * FROM {}".format(TABLE_NAME)
df = pd.read_sql_table(TABLE_NAME, con=db_connection)
########################
#Setup the layout
########################
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Index page
index_page = html.Div([
    dcc.Link('Register a new document', href='/register_page'),
    html.Br(),
    dcc.Link('Document search', href='/search_page'),
    html.Br(),
    dcc.Link('Modify existing document', href='/modify_page'),
])

# Register new document page
register_page_layout = html.Div([

    html.Div([

        html.H3(["Document Number"
            ], style={'marginLeft':'5%',
                    'marginRight':'5%',}),

        html.Div([
            html.Div([
                html.P("Record Number"),
                dcc.Input(
                    id='full-serial-num',
                    type = 'number',
                    max = "99999",
                    disabled = True,
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 195,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%',
                        'float':'right',
                        'textAlign':'center',
                        'verticalAlign':'middle'}
            ),

            html.Div([
            html.P("Business Series"),
            dcc.Dropdown(
                id = 'business-series-dropdown',
                options=bs_dropdown,
                value=''
            )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            ),

            html.Div([
                html.P("Business Units"),
                dcc.Dropdown(
                    id = 'business-unit-dropdown',
                    options=bu_dropdown,
                    value=''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            ),

            html.Div([
                html.P("Document Types"),
                dcc.Dropdown(
                    id = 'document-type-dropdown',
                    options = doc_types_dropdown,
                    value=''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
                ),

            html.Div([
                html.P("Serial Numbers"),
                dcc.Input(
                    id='serial-text-input',
                    disabled=True,
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            ),

            html.Div([
                html.P("Status"),
                dcc.Dropdown(
                    id = 'status',
                    options=[
                        {'label': 'Release', 'value': 'Release'},
                        {'label': 'WIP', 'value': 'WIP'},
                        {'label': 'Obsolete', 'value': 'Obsolete'},
                        {'label': 'Record', 'value': 'Record'}
                    ],
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            )
        ]),

        html.Div([
            html.Div([
                html.P("Title"),
                dcc.Input(
                    id='record-title',
                    placeholder='Enter document title',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 55}
            ),

            html.Div([
                html.P("Custodian"),
                dcc.Input(
                    id='custodian',
                    placeholder='Enter Custodian',
                    value = ''
                )], style={'marginBottom': 25}
            ),

            html.Div([
                html.P("Revision"),
                dcc.Input(
                    id='revision',
                    placeholder='Enter Revision',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("Link"),
                dcc.Input(
                    id='link',
                    placeholder='Enter Link',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float':'left'}),

        html.Div([
            html.Div([
                html.P("SOW No"),
                dcc.Input(
                    id='sow-no',
                    type = 'number',
                    placeholder='Enter SOW Number',
                    value = ''
                )], style={'marginBottom': 25,
                            'marginTop': 55,
                            'textAlign':'left',
                            'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Issue Date"),
                dcc.DatePickerSingle(
                    id='issue-date',
                    with_portal = True
                )], style={'marginBottom': 25,
                            'marginTop': 25,
                            'textAlign':'left',
                            'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Effective Date"),
                dcc.DatePickerSingle(
                    id='effective-date',
                    with_portal = True
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Reaffirmation Date"),
                dcc.DatePickerSingle(
                    id='reaffirmation-date',
                    with_portal = True
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float': 'right'})
    ], style={'overflow': 'hidden',
            'padding': '20px'}),

    html.Div([
        html.H3(["Export Controls Info"
            ], style={'marginLeft':'5%',
                    'marginRight':'5%'}),

        html.Div([
            html.Div([
                html.P("Protection Level"),
                dcc.Dropdown(
                    id = 'protection-level',
                    options=[
                        {'label': 'Public', 'value': 'Public: Public'},
                        {'label': 'Confidential', 'value': 'Confidential: Non-Tech Private'},
                        {'label': 'Classified', 'value': 'Classified: Technical Private'}
                    ],
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("EC Techical Data"),
                dcc.RadioItems(
                    id='ec-technical-data',
                    options=[
                        {'label': 'Yes', 'value': '1'},
                        {'label': 'No', 'value': '0'},
                    ],
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("Permit"),
                dcc.Input(
                    id='permit',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("ECL"),
                dcc.Input(
                    id='ecl',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("ECCN"),
                dcc.Input(
                    id='eccn',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("USML"),
                dcc.Input(
                    id='usml',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("CG"),
                dcc.Input(
                    id='cg',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float': 'left'}),

        html.Div([
            html.Div([
                html.P("US Exemption"),
                dcc.Input(
                    id='us-exemption',
                    placeholder='Enter US Exemption',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Canada Exemptior"),
                dcc.Input(
                    id='canada-exemptior',
                    placeholder='Enter Canada Exemptior',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Expiration Date"),
                dcc.DatePickerSingle(
                    id='expiration-date',
                    with_portal = True
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float': 'right'})
    ], style={'overflow': 'hidden',
            'padding': '20px'}),

    html.Div([
        html.Div([
            dcc.Link(html.Button(id='back-button',
                                children='Back',
                                style={'marginLeft':'5%','marginRight':'5%'}),
                                href='/'),

            html.Button(id='submit-button',
                        children='Submit',
                        style={'marginLeft':'5%','marginRight':'5%'}),

            dcc.ConfirmDialog(
                id = 'submit-state',
                message = 'Please fill in all required fields'
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%'})
    ], style={'overflow': 'hidden',
            'padding': '20px'})

])

# Document search page
search_page_layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    ),

    dcc.Link(html.Button(id='back-button',
                        children='Back',
                        style={'margin':'5px'}),
                        href='/')
])

# Modify existing document page
modify_page_layout = html.Div([

    html.Div([

        html.H3(["Document Number"
            ], style={'marginLeft':'5%',
                    'marginRight':'5%',}),

        html.Div([
            html.Div([
                html.P("Record Number"),
                dcc.Input(
                    id='full-serial-num-mod',
                    type = 'number',
                    max = "99999",
                    disabled = True,
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 195,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%',
                        'float':'right',
                        'textAlign':'center',
                        'verticalAlign':'middle'}
            ),

            html.Div([
            html.P("Business Series"),
            dcc.Dropdown(
                id = 'business-series-dropdown-mod',
                options=bs_dropdown,
                value=''
            )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            ),

            html.Div([
                html.P("Business Units"),
                dcc.Dropdown(
                    id = 'business-unit-dropdown-mod',
                    options=bu_dropdown,
                    value=''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            ),

            html.Div([
                html.P("Document Types"),
                dcc.Dropdown(
                    id = 'document-type-dropdown-mod',
                    options = doc_types_dropdown,
                    value=''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
                ),

            html.Div([
                html.P("Serial Numbers"),
                dcc.Input(
                    id='serial-text-input-mod',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            ),

            html.Button(id='modify-button',
                        children='Modify',
                        style={'marginLeft':'5%','marginRight':'5%'}),

            html.Div([
                html.P("Status"),
                dcc.Dropdown(
                    id = 'status-mod',
                    options=[
                        {'label': 'Release', 'value': 'Release'},
                        {'label': 'WIP', 'value': 'WIP'},
                        {'label': 'Obsolete', 'value': 'Obsolete'},
                        {'label': 'Record', 'value': 'Record'}
                    ],
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'marginLeft':'5%',
                        'marginRight':'5%',
                        'width': '40%'}
            )
        ]),

        html.Div([
            html.Div([
                html.P("Title"),
                dcc.Input(
                    id='record-title-mod',
                    placeholder='Enter document title',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 55}
            ),

            html.Div([
                html.P("Custodian"),
                dcc.Input(
                    id='custodian-mod',
                    placeholder='Enter Custodian',
                    value = ''
                )], style={'marginBottom': 25}
            ),

            html.Div([
                html.P("Revision"),
                dcc.Input(
                    id='revision-mod',
                    placeholder='Enter Revision',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("Link"),
                dcc.Input(
                    id='link-mod',
                    placeholder='Enter Link',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float':'left'}),

        html.Div([
            html.Div([
                html.P("SOW No"),
                dcc.Input(
                    id='sow-no-mod',
                    type = 'number',
                    placeholder='Enter SOW Number',
                    value = ''
                )], style={'marginBottom': 25,
                            'marginTop': 55,
                            'textAlign':'left',
                            'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Issue Date"),
                dcc.DatePickerSingle(
                    id='issue-date-mod',
                    with_portal = True
                )], style={'marginBottom': 25,
                            'marginTop': 25,
                            'textAlign':'left',
                            'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Effective Date"),
                dcc.DatePickerSingle(
                    id='effective-date-mod',
                    with_portal = True
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Reaffirmation Date"),
                dcc.DatePickerSingle(
                    id='reaffirmation-date-mod',
                    with_portal = True
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float': 'right'})
    ], style={'overflow': 'hidden',
            'padding': '20px'}),

    html.Div([
        html.H3(["Export Controls Info"
            ], style={'marginLeft':'5%',
                    'marginRight':'5%'}),

        html.Div([
            html.Div([
                html.P("Protection Level"),
                dcc.Dropdown(
                    id = 'protection-level-mod',
                    options=[
                        {'label': 'Public', 'value': 'Public: Public'},
                        {'label': 'Confidential', 'value': 'Confidential: Non-Tech Private'},
                        {'label': 'Classified', 'value': 'Classified: Technical Private'}
                    ],
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("EC Techical Data"),
                dcc.RadioItems(
                    id='ec-technical-data-mod',
                    options=[
                        {'label': 'Yes', 'value': '1'},
                        {'label': 'No', 'value': '0'},
                    ],
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("Permit"),
                dcc.Input(
                    id='permit-mod',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("ECL"),
                dcc.Input(
                    id='ecl-mod',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("ECCN"),
                dcc.Input(
                    id='eccn-mod',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("USML"),
                dcc.Input(
                    id='usml-mod',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            ),

            html.Div([
                html.P("CG"),
                dcc.Input(
                    id='cg-mod',
                    placeholder='N/A',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float': 'left'}),

        html.Div([
            html.Div([
                html.P("US Exemption"),
                dcc.Input(
                    id='us-exemption-mod',
                    placeholder='Enter US Exemption',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Canada Exemptior"),
                dcc.Input(
                    id='canada-exemptior-mod',
                    placeholder='Enter Canada Exemptior',
                    value = ''
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            ),

            html.Div([
                html.P("Expiration Date"),
                dcc.DatePickerSingle(
                    id='expiration-date-mod',
                    with_portal = True
                )], style={'marginBottom': 25,
                        'marginTop': 25,
                        'textAlign':'left',
                        'verticalAlign':'middle'}
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%',
                'float': 'right'})
    ], style={'overflow': 'hidden',
            'padding': '20px'}),

    html.Div([
        html.Div([
            dcc.Link(html.Button(id='back-button',
                                children='Back',
                                style={'marginLeft':'5%','marginRight':'5%'}),
                                href='/'),

            html.Button(id='delete-button',
                        children='Delete',
                        style={'marginLeft':'5%','marginRight':'5%'}),

            html.Button(id='submit-button',
                        children='Submit',
                        style={'marginLeft':'5%','marginRight':'5%'}),

            dcc.ConfirmDialog(
                id = 'record-search-state-mod',
                message = 'Cannot find entered record number in DataBase'
            ),

            dcc.ConfirmDialog(
                id = 'submit-state-mod',
                message = 'Please fill in all required fields'
            ),

            dcc.ConfirmDialog(
                id = 'delete-state',
                message = 'Cannot delete this record'
            ),

            # Dummy div
            html.Div(id='test-div', style={'display': 'none'})
        
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%'})
    ], style={'overflow': 'hidden',
            'padding': '20px'})

])


########################
#Set up callbacks
########################


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/register_page':
        return register_page_layout
    elif pathname == '/search_page':
        df = pd.read_sql_table(TABLE_NAME, con=db_connection)
        return search_page_layout
    elif pathname == '/modify_page':
        return modify_page_layout
    else:
        return index_page

@app.callback(
    Output('full-serial-num', 'value'),
    [Input('business-unit-dropdown', 'value'),
    Input('document-type-dropdown', 'value'),
    Input('serial-text-input', 'value')])
def update_output_div(input_business_unit, input_document_type, input_serial_text):
    result = ''
    if input_business_unit and input_document_type and input_serial_text:
        leading_zeros_document_type = str(input_document_type).zfill(2)
        leading_zeros_serial_text = str(input_serial_text).zfill(5)
        result = str(input_business_unit) + leading_zeros_document_type + leading_zeros_serial_text
    return result

@app.callback(
    [Output('business-unit-dropdown', 'options'),
    Output('business-unit-dropdown', 'value')],
    [Input('business-series-dropdown', 'value')])
def update_business_unit_dropdown(input_value):
    bu_dropdown = []
    bu_value =''
    if input_value:
        business_units = lib.BusinessUnit.ReadBusinessUnitsByCode(db_cursor, str(input_value))
        for bu in business_units:
            bu_dropdown.append({'label':str(bu.specific_code)+ " - "+bu.title, 'value':bu.specific_code})
    return bu_dropdown, bu_value

@app.callback(
    Output('document-type-dropdown', 'value'),
    [Input('business-unit-dropdown', 'value'),
    Input('business-series-dropdown', 'value')],
    [State('document-type-dropdown', 'value')])
def update_business_unit_dropdown(input_business_unit, input_business_series, document_type_state):
    if not (input_business_unit and input_business_series):
        return ''
    else:
        return document_type_state

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

@app.callback(Output('submit-state', 'displayed'),
    [Input('submit-button', 'n_clicks')],
    [State('full-serial-num', 'value'),
    State('status', 'value'),
    State('record-title', 'value'),
    State('custodian', 'value'),
    State('revision', 'value'),
    State('link', 'value'),
    State('sow-no', 'value'),
    State('issue-date', 'date'),
    State('effective-date', 'date'),
    State('reaffirmation-date', 'date'),
    State('protection-level', 'value'),
    State('ec-technical-data', 'value'),
    State('permit', 'value'),
    State('ecl', 'value'),
    State('eccn', 'value'),
    State('usml', 'value'),
    State('cg', 'value'),
    State('us-exemption', 'value'),
    State('canada-exemptior', 'value'),
    State('expiration-date', 'date')])
def post_record_num(n_clicks,
                    record_num_state,
                    record_status_state,
                    record_title_state,
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
                    record_exp_date_state
                    ):
    result = ''

    if n_clicks is None:
        raise PreventUpdate
    else:
        if (record_num_state and
            record_status_state and
            record_title_state and
            record_custodian_state and
            record_revision_state and
            record_link_state and
            record_sow_state and
            record_issue_date_state and
            record_effective_date_state and
            record_reaffirmation_date_state and
            record_protection_lvl_state and
            record_ec_state and
            record_permit_state and
            record_ecl_state and
            record_eccn_state and
            record_usml_state and
            record_cg_state and
            record_us_exemption_state and
            record_ca_exemption_state and
            record_exp_date_state):

            CreateNewRecord(mydb,
                    record_num_state,
                    record_status_state,
                    record_title_state,
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
                    record_exp_date_state)
            result = False
        else:
            result = True
    return result

@app.callback(
    [Output('record-search-state-mod', 'displayed'),
    Output('status-mod', 'value'),
    Output('record-title-mod', 'value'),
    Output('custodian-mod', 'value'),
    Output('revision-mod', 'value'),
    Output('link-mod', 'value'),
    Output('sow-no-mod', 'value'),
    Output('issue-date-mod', 'date'),
    Output('effective-date-mod', 'date'),
    Output('reaffirmation-date-mod', 'date'),
    Output('protection-level-mod', 'value'),
    Output('ec-technical-data-mod', 'value'),
    Output('permit-mod', 'value'),
    Output('ecl-mod', 'value'),
    Output('eccn-mod', 'value'),
    Output('usml-mod', 'value'),
    Output('cg-mod', 'value'),
    Output('us-exemption-mod', 'value'),
    Output('canada-exemptior-mod', 'value'),
    Output('expiration-date-mod', 'date')],
    [Input('modify-button', 'n_clicks')],
    [State('full-serial-num-mod', 'value')])
def display_all_fields(n_clicks, input_serial_num):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_sql_table(TABLE_NAME, con=db_connection)
        selected_row = df[df['full_serial_number']==numpy.int64(input_serial_num)]
        if (not selected_row.empty):
            alert = False
            status = selected_row.status.item()
            title = selected_row.title.item()
            custodian = selected_row.custodian.item()
            revision = selected_row.revision.item()
            link = selected_row.link.item()
            sow_no = selected_row.sow_no.item()
            issue_date = selected_row.issue_date.item()
            effective_date = selected_row.effective_date.item()
            reaffirmation_date = selected_row.reaffirmation_date.item()
            protection_lvl = selected_row.protection_lvl.item()
            ec_technical_data = str(int(selected_row.ec_technical_data.item()))
            permit = selected_row.permit.item()
            ecl = selected_row.ecl.item()
            eccn = selected_row.eccn.item()
            usml = selected_row.usml.item()
            cg = selected_row.cg.item()
            us_exemption = selected_row.us_exemption.item()
            ca_exemption = selected_row.ca_exemption.item()
            exp_date = selected_row.exp_date.item()
        else:
            alert = True
            status = ''
            title = ''
            custodian = ''
            revision = ''
            link = ''
            sow_no = ''
            issue_date = ''
            effective_date = ''
            reaffirmation_date = ''
            protection_lvl = ''
            ec_technical_data = ''
            permit = ''
            ecl = ''
            eccn = ''
            usml = ''
            cg = ''
            us_exemption = ''
            ca_exemption = ''
            exp_date = ''
    
    return [alert, status, title, custodian, revision, link, \
           sow_no, issue_date, effective_date, reaffirmation_date, \
           protection_lvl, ec_technical_data, permit, ecl, \
           eccn, usml, cg, us_exemption,ca_exemption, \
           exp_date]

@app.callback([Output('test-input', 'value')],
              [Input('status-mod', 'value'),
              Input('record-title-mod', 'value'),
              Input('custodian-mod', 'value'),
              Input('revision-mod', 'value'),
              Input('link-mod', 'value'),
              Input('sow-no-mod', 'value'),
              Input('issue-date-mod', 'date'),
              Input('effective-date-mod', 'date'),
              Input('reaffirmation-date-mod', 'date'),
              Input('protection-level-mod', 'value'),
              Input('ec-technical-data-mod', 'value'),
              Input('permit-mod', 'value'),
              Input('ecl-mod', 'value'),
              Input('eccn-mod', 'value'),
              Input('usml-mod', 'value'),
              Input('cg-mod', 'value'),
              Input('us-exemption-mod', 'value'),
              Input('canada-exemptior-mod', 'value'),
              Input('expiration-date-mod', 'date')])
def update_div(input_value):
    print('Input value: {}'.format(input_value))
    return input_value

@app.callback(
    Output('full-serial-num-mod', 'value'),
    [Input('business-unit-dropdown-mod', 'value'),
    Input('document-type-dropdown-mod', 'value'),
    Input('serial-text-input-mod', 'value')])
def update_output_div(input_business_unit, input_document_type, input_serial_text):
    result = ''
    if input_business_unit and input_document_type and input_serial_text:
        leading_zeros_document_type = str(input_document_type).zfill(2)
        leading_zeros_serial_text = str(input_serial_text).zfill(5)
        result = str(input_business_unit) + leading_zeros_document_type + leading_zeros_serial_text
    return result

@app.callback(
    [Output('business-unit-dropdown-mod', 'options'),
    Output('business-unit-dropdown-mod', 'value')],
    [Input('business-series-dropdown-mod', 'value')])
def update_business_unit_dropdown(input_value):
    bu_dropdown = []
    bu_value =''
    if input_value:
        business_units = lib.BusinessUnit.ReadBusinessUnitsByCode(db_cursor, str(input_value))
        for bu in business_units:
            bu_dropdown.append({'label':str(bu.specific_code)+ " - "+bu.title, 'value':bu.specific_code})
    return bu_dropdown, bu_value

@app.callback(
    Output('document-type-dropdown-mod', 'value'),
    [Input('business-unit-dropdown-mod', 'value'),
    Input('business-series-dropdown-mod', 'value')],
    [State('document-type-dropdown-mod', 'value')])
def update_business_unit_dropdown(input_business_unit, input_business_series, document_type_state):
    if not (input_business_unit and input_business_series):
        return ''
    else:
        return document_type_state

@app.callback(Output('submit-state-mod', 'displayed'),
    [Input('submit-button', 'n_clicks')],
    [State('full-serial-num-mod', 'value'),
    State('status-mod', 'value'),
    State('record-title-mod', 'value'),
    State('custodian-mod', 'value'),
    State('revision-mod', 'value'),
    State('link-mod', 'value'),
    State('sow-no-mod', 'value'),
    State('issue-date-mod', 'date'),
    State('effective-date-mod', 'date'),
    State('reaffirmation-date-mod', 'date'),
    State('protection-level-mod', 'value'),
    State('ec-technical-data-mod', 'value'),
    State('permit-mod', 'value'),
    State('ecl-mod', 'value'),
    State('eccn-mod', 'value'),
    State('usml-mod', 'value'),
    State('cg-mod', 'value'),
    State('us-exemption-mod', 'value'),
    State('canada-exemptior-mod', 'value'),
    State('expiration-date-mod', 'date')])
def put_record_num(n_clicks,
                    record_num_state,
                    record_status_state,
                    record_title_state,
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
                    record_exp_date_state
                    ):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if (record_num_state and
            record_status_state and
            record_title_state and
            record_custodian_state and
            record_revision_state and
            record_link_state and
            record_sow_state and
            record_issue_date_state and
            record_effective_date_state and
            record_reaffirmation_date_state and
            record_protection_lvl_state and
            record_ec_state and
            record_permit_state and
            record_ecl_state and
            record_eccn_state and
            record_usml_state and
            record_cg_state and
            record_us_exemption_state and
            record_ca_exemption_state and
            record_exp_date_state):

            record = Record(business_code = '', document_code = '', full_serial_number = record_num_state, status = record_status_state, title = record_title_state, \
                       custodian = record_custodian_state, revision = record_revision_state, link = record_link_state, sow_no = record_sow_state, \
                       issue_date = record_issue_date_state, effective_date = record_effective_date_state, reaffirmation_date = record_reaffirmation_date_state, \
                       protection_lvl = record_protection_lvl_state, ec_technical_data = record_ec_state, permit = record_permit_state, ecl = record_ecl_state, \
                       eccn = record_eccn_state, usml = record_usml_state, cg = record_cg_state, us_exemption = record_us_exemption_state, ca_exemption = record_ca_exemption_state, \
                       exp_date = record_exp_date_state, summary = 'NA')
            UpdateRecord(mydb, record)
            result = False
        else:
            result = True
    return result

@app.callback(Output('delete-state', 'displayed'),
    [Input('delete-button', 'n_clicks')],
    [State('full-serial-num-mod', 'value')])
def delete_record_num(n_clicks, full_serial_number):
    if n_clicks is None:
        raise PreventUpdate
    else:
        if (full_serial_number):
            DeleteRecord(mydb, full_serial_number)
            result = False
        else:
            result = True
    return result

if __name__ == '__main__':
    app.run_server(debug=True)