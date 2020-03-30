import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from db_config import DB_USER, DB_PASS, DB_IP, DB_PORT, DB_NAME, TABLE_NAME, db_connection
import pandas as pd
from app import app

df = pd.DataFrame()

########################
#Setup the layout
########################

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
                        href='/'),

    html.Button(id='refresh-button',
                children='Refresh',
                style={'margin':'5px'}),

    html.Div(id='trigger-div', style={'display': 'none'})
])

########################
#Set up callbacks
########################
@app.callback([Output('table', 'data'),
             Output('table', 'columns')],
             [Input('refresh-button', 'n_clicks'),
             Input('trigger-div', 'children')])
def update_df(n_clicks, trigger):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.read_sql_table(TABLE_NAME, con=db_connection)
        columns=[{"name": i, "id": i} for i in df.columns]
        data=df.to_dict('records')
    
    return data, columns