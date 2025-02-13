import dash
from dash import dcc, html

def SideContainer():
    return html.Div(
        className="w-64 h-screen bg-white shadow-lg p-4 fixed border-r border-gray-200",
        children=[
            html.H2("📊 Dashboard", className="text-2xl font-bold text-gray-800"),
            html.Ul(
                className="mt-6 space-y-2",
                children=[
                    html.Li(dcc.Link("📈 Trends", href="/trends", 
                                   className="block py-2 px-4 rounded-md text-gray-700 hover:bg-green-500 hover:text-white transition")),
                    html.Li(dcc.Link("⚙️ Settings", href="/settings", 
                                   className="block py-2 px-4 rounded-md text-gray-700 hover:bg-yellow-500 hover:text-white transition")),
                    html.Li(dcc.Link("📋 Data Table", href="/table", 
                                   className="block py-2 px-4 rounded-md text-gray-700 hover:bg-blue-500 hover:text-white transition")),              
                ],
            ),
            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    "📂 Drag & Drop or ",
                    html.A("Select File", className="text-blue-500 underline"),
                    html.P("(CSV or Excel only)", className="text-gray-500 text-sm")
                ]),
                className="border-2 border-dashed border-gray-300 p-4 text-center rounded-lg bg-gray-50 hover:bg-gray-100 cursor-pointer",
                multiple=False,  # Allow only one file
            ),
        ]
    )
