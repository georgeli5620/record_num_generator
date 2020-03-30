import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from layout.CreateNewDoc import register_page_layout
from layout.SearchDoc import search_page_layout
from layout.ModifyDoc import modify_page_layout

from app import app
import pandas as pd
from db_config import TABLE_NAME, db_con, db_cursor, db_connection, df

########################
#Setup the layout
########################
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

########################
#Set up callbacks
########################
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
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

if __name__ == '__main__':
    app.run_server(debug=True)