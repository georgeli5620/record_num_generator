import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from db_config import DB_USER, DB_PASS, DB_IP, DB_PORT, DB_NAME, TABLE_NAME, db_con, db_cursor, db_connection, df
from app import app
import pandas as pd
import numpy as np

import lib.BusinessUnit
import lib.DocumentType
import lib.Record

from lib.BusinessUnit import BusinessUnit
from lib.DocumentType import DocumentType
from lib.Record import Record, CreateNewRecord, ReadRecord, UpdateRecord, ReadAllRecords, DeleteRecord

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

########################
#Setup the layout
########################

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
                                style={'marginLeft':'5%','marginRight':'5%', 'float':'left'}),
                                href='/'),
                            
            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'Delete',
                    style={'marginLeft':'5%','marginRight':'5%', 'float':'left'}
                ),
                id='delete-button',
                message='Document will be deleted from DataCentral. Are you sure you want to do that?'
            ),

            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'Submit',
                    style={'marginLeft':'5%','marginRight':'5%', 'float':'left'}
                ),
                id='submit-button',
                message='Document will be modified in DataCentral. Are you sure you want to do that?'
            ),

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

            dcc.ConfirmDialog(
                id = 'delete-confirm',
                message = 'Document has been successfully deleted'
            ),

            dcc.ConfirmDialog(
                id = 'modify-confirm',
                message = 'Document has been successfully modified'
            ),

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

# Read document from correspondent record number
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
        selected_row = df[df['full_serial_number']==np.int64(input_serial_num)]
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

# Generate record number from business unit, document types and serial numbers
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

# Filter Business Units options based on Business Series
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

# Modify document
@app.callback([Output('submit-state-mod', 'displayed'),
    Output('modify-confirm', 'displayed')],
    [Input('submit-button', 'submit_n_clicks')],
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
def put_record_num(submit_n_clicks,
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
    if submit_n_clicks is None:
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
            UpdateRecord(db_con, record)
            result = [False, True]
        else:
            result = [True, False]
    return result

# Delete document
@app.callback([Output('delete-state', 'displayed'),
    Output('delete-confirm', 'displayed')],
    [Input('delete-button', 'submit_n_clicks')],
    [State('full-serial-num-mod', 'value')])
def delete_record_num(submit_n_clicks, full_serial_number):
    if submit_n_clicks is None:
        raise PreventUpdate
    else:
        if (full_serial_number):
            DeleteRecord(db_con, full_serial_number)
            result = [False, True]
        else:
            result = [True, False]
    return result