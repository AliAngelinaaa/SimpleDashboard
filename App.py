from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd
import plotly.express as px

# Import the sidebar component
from components.sidebar import SideContainer
# Import the data table component
from components.data_table import DataTable

# Initialize the Dash app with Tailwind CSS and suppress callback exceptions
app = Dash(__name__, 
    external_scripts=['https://cdn.tailwindcss.com'],
    suppress_callback_exceptions=True
)
# Layout structure
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Add URL location component
    dcc.Store(id='stored-data', storage_type='memory'),
    
    html.Div([
        html.Div([
            SideContainer()
        ], className="w-64 fixed h-screen"),
        
        html.Div([
            html.Div([
                html.Div(id='page-content', className="p-6 overflow-x-hidden"),  # Added overflow-x-hidden
                html.Div([
                    dcc.Dropdown(id='column-selector', multi=True),
                    dcc.Graph(id='line-chart')
                ], style={'display': 'none'})
            ])
        ], className="flex-grow ml-64 overflow-x-auto")  # Added overflow-x-auto
    ], className="flex")
])

# Add callback for URL routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('stored-data', 'data')]
)
def display_page(pathname, stored_data):
    if not stored_data:
        return html.Div("Upload a file to begin analysis", 
                       className="text-gray-500 text-center mt-10")
    
    df = pd.DataFrame(stored_data)
    
    if pathname == '/trends':
        return create_trends(df)
    elif pathname == '/table':  # Changed from /chart to /table
        return html.Div([
            html.H3("Data Table View", className="text-2xl font-bold mb-4"),
            DataTable(df)
        ])
    elif pathname == '/settings':
        return html.Div("Settings page - Coming soon", className="p-4")
    else:
        # Default view showing both charts and trends
        return html.Div([
            create_charts(df),
            html.Div(className="mt-8"),
            create_trends(df)
        ])

# Modify the update_output callback to only update stored data
@app.callback(
    [Output('stored-data', 'data')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is None:
        return [None]
    
    # Parse uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        # Determine file type and read accordingly
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif filename.endswith('.tsv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\t')
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise ValueError('Unsupported file format. Please upload a CSV, TSV, or Excel file.')
        
        # Store the data
        return [df.to_dict('records')]
            
    except Exception as e:
        return [None]

def create_charts(df):
    # Get numeric columns for plotting
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    if len(numeric_cols) == 0:
        return html.Div([
            "No numeric columns found in the dataset for visualization.",
        ], className="text-red-500")
    
    # Create a line chart using only numeric columns
    return html.Div([
        html.H3("Data Visualization", className="text-2xl font-bold mb-4"),
        
        # Add column selector
        html.Div([
            html.Label("Select columns to plot:", className="block mb-2"),
            dcc.Dropdown(
                id='column-selector',
                options=[{'label': col, 'value': col} for col in numeric_cols],
                value=numeric_cols[0],  # Default to first numeric column
                multi=True,
                className="mb-4"
            )
        ]),
        
        # Add the Graph component with explicit ID
        dcc.Graph(
            id='line-chart',
            figure=px.line(
                df,
                y=numeric_cols[0],  # Default to first numeric column
                title=f'Time Series Plot of {numeric_cols[0]}'
            )
        )
    ])

# Add new callback for updating the chart
@app.callback(
    Output('line-chart', 'figure'),
    [Input('column-selector', 'value'),
     Input('stored-data', 'data')]
)
def update_chart(selected_columns, stored_data):
    if not selected_columns or not stored_data:
        return px.line()  # Return empty figure if no data or columns selected
    
    df = pd.DataFrame(stored_data)
    fig = px.line(
        df,
        y=selected_columns,
        title=f'Time Series Plot of Selected Columns'
    )
    return fig

def create_trends(df):
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    # Calculate metrics
    metrics = []
    
    # Add total records metric
    metrics.append({
        'title': 'Total Records',
        'value': len(df),
        'icon': '📊',
        'color': 'blue'
    })
    
    # Add statistics for each numeric column
    for col in numeric_cols[:2]:  # Limit to first 2 numeric columns
        metrics.extend([
            {
                'title': f'Avg {col}',
                'value': f'{df[col].mean():.2f}',
                'icon': '📈',
                'color': 'green'
            },
            {
                'title': f'Max {col}',
                'value': f'{df[col].max():.2f}',
                'icon': '⬆️',
                'color': 'red'
            }
        ])

    return html.Div([
        html.H3("Trends Dashboard", className="text-2xl font-bold mb-4"),
        html.Div([
            # Generate metric cards dynamically
            *[html.Div([
                html.Div([
                    html.Span(metric['icon'], className="text-2xl mr-2"),
                    html.H4(metric['title'], className="text-lg font-semibold")
                ], className="flex items-center"),
                html.P(
                    metric['value'],
                    className=f"text-3xl font-bold text-{metric['color']}-600 mt-2"
                )
            ], className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow")
              for metric in metrics
            ]
        ], className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
