import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from db_config import db_con, db_cursor
from app import app

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
                                style={'marginLeft':'5%','marginRight':'5%', 'float':'left'}),
                                href='/'),

            dcc.ConfirmDialogProvider(
                children=html.Button(
                    'submit',
                    style={'marginLeft':'5%','marginRight':'5%', 'float':'left'}
                ),
                id='submit-button',
                message='Document will be added to DataCentral. Are you sure you want to submit?'
            ),

            dcc.ConfirmDialog(
                id = 'submit-state',
                message = 'Please fill in all required fields'
            ),

            dcc.ConfirmDialog(
                id = 'submit-confirm',
                message = 'Document has been successfully submitted'
            )
        ], style={'marginLeft':'5%',
                'marginRight':'5%',
                'width': '40%'})
    ], style={'overflow': 'hidden',
            'padding': '20px'})

])

########################
#Set up callbacks
########################

# Generate record number
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

# Generate correspondent business unit dropdown
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

# Generate correspondent document type dropdown
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

# Deduct next serial number according to existing documents
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

# Submit confirmation
@app.callback([Output('submit-state', 'displayed'),
              Output('submit-confirm', 'displayed')],
              [Input('submit-button', 'submit_n_clicks')],
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
def post_record_num(submit_n_clicks,
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

            CreateNewRecord(db_con,
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
        
            result = [False, True]
        else:
            result = [True, False]
    return result