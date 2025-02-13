import dash
from dash import dash_table, html
import pandas as pd

def DataTable(df=None):
    if df is None:
        return html.Div("No data uploaded yet.", className="text-gray-500 text-center p-4")
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'system-ui'
        },
        style_header={
            'backgroundColor': 'rgb(240, 242, 245)',
            'fontWeight': 'bold',
            'border': '1px solid rgb(209, 213, 219)'
        },
        style_data={
            'border': '1px solid rgb(209, 213, 219)'
        },
        page_size=15
    ) 