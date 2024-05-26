import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.colors import n_colors
import psycopg2 as psy

dbname = "QCBC"
user = "user1"
password = "password111"
host = "localhost"
port = "5433"

try:
    conn = psy.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connected to PostgreSQL database successfully!")
except psy.OperationalError as e:
    print(f"Unable to connect to database. Error: {e}")

app = dash.Dash(__name__)

def fetch_data_from_db(query):
    try:
        conn = psy.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        conn.close()
        print("Data fetched successfully:")
        return data
    except psy.OperationalError as e:
        print(f"Unable to connect to database. Error: {e}")
        return None

def get_countries_data():
    query = "SELECT * FROM country;"
    return fetch_data_from_db(query)

def get_continent_data():
    query = "SELECT * FROM continent;"
    return fetch_data_from_db(query)

def get_batch_data():
    query = "SELECT * FROM Coffee_batch;"
    return fetch_data_from_db(query)

def get_quality_data():
    query = "SELECT * FROM Coffee_quality;"
    return fetch_data_from_db(query)
def get_locations():
    query = "select distinct continent_fk, country_fk from coffee_batch where country_fk is not null order by continent_fk, country_fk"
    return fetch_data_from_db(query)

def create_table(data, headers):
    table_style = {
        'borderCollapse': 'collapse',
        'width': '100%',
        'border': '1px solid #ddd',
        'font-size': '14px'
    }
    th_style = {
        'padding': '8px',
        'textAlign': 'left',
        'border': '1px solid #ddd',
        'backgroundColor': '#f2f2f2',
        'color': '#333'
    }
    td_style = {
        'padding': '8px',
        'textAlign': 'left',
        'border': '1px solid #ddd'
    }

    return html.Table(
        style=table_style,
        children=[
            html.Thead(
                children=[
                    html.Tr(
                        children=[
                            html.Th(header, style=th_style) for header in headers
                        ]
                    )
                ]
            ),
            html.Tbody(
                children=[
                    html.Tr(
                        children=[
                            html.Td(cell, style=td_style) for cell in row
                        ]
                    ) for row in data
                ]
            )
        ]
    )
styles = {
    'body': {
        'font-family': 'Arial, sans-serif',
        'background-color': '#f9f9f9',
        'margin': '0',
        'padding': '0',
    },
    '.header': {
        'background-color': '#4CAF50',
        'color': 'white',
        'padding': '15px',
        'text-align': 'center',
        'font-size': '24px',
    },
    '.container': {
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'padding': '20px',
    },
    '.content': {
        'background-color': 'white',
        'padding': '20px',
        'margin': '10px',
        'border-radius': '8px',
        'box-shadow': '0 0 10px rgba(0, 0, 0, 0.1)',
        'width': '80%',
        'max-width': '800px',
    },
    'button': {
        'background-color': '#4CAF50',
        'color': 'white',
        'border': 'none',
        'padding': '10px 20px',
        'text-align': 'center',
        'text-decoration': 'none',
        'display': 'inline-block',
        'font-size': '16px',
        'margin': '4px 2px',
        'cursor': 'pointer',
        'border-radius': '4px',
    },
    'button:hover': {
        'background-color': '#45a049',
    },
    'table': {
        'width': '100%',
        'border-collapse': 'collapse',
        'margin': '20px 0',
    },
    'th, td': {
        'padding': '12px',
        'border': '1px solid #ddd',
        'text-align': 'left',
    },
    'th': {
        'background-color': '#f2f2f2',
    },
    'tr:nth-child(even)': {
        'background-color': '#f9f9f9',
    }
}

app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1("CuppingData: Quality of Coffee By Country (QCBC)")
    ], style=styles['.header']),
    html.Div(className='container', children=[
        html.Div(className='content', children=[
            html.P("Cupping Data..."),
            html.Button("Show Country Data", id="show-country-button", n_clicks=0, style=styles['button']),
            html.Button("Show Continent Data", id="show-continent-button", n_clicks=0, style=styles['button']),
        ], style=styles['.content']),
        html.Div(className='content', children=[
            html.Button("Show Coffee Batch Data", id="show-batch-button", n_clicks=0, style=styles['button']),
            html.Button("Show Coffee Quality Data", id="show-quality-button", n_clicks=0, style=styles['button'])
        ], style=styles['.content']),
        html.Div(className='content', children=[
            html.Button("Show Analyzed Countries", id="show-locations-button", n_clicks=0, style=styles['button'])
        ], style=styles['.content']),
        html.Div(className='content', children=[
            html.Button("Show Continent Pie Chart", id="show-continent-quality-pie-button", n_clicks=0, style=styles['button']),
            html.Button("Show Country Quality Bar Charts", id="show-country-quality-bar-button", n_clicks=0, style=styles['button'])
        ], style=styles['.content'])
    ], style=styles['.container']),
    html.Div(id="tables-container"),
    html.Div(id="pie-charts-container"),
    html.Div(id="bar-charts-container")
], style=styles['body'])
def display_tables(n_clicks_country, n_clicks_continent, n_clicks_batch, n_clicks_locations, n_clicks_quality):
    ctx = dash.callback_context

    if not ctx.triggered:
        return []

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "show-country-button":
        country_data = get_countries_data()
        headers = [
            "Origin", "Avg Aroma", "Avg Flavor", "Avg Aftertaste", "Avg Acidity", "Avg Body", 
            "Avg Balance", "Avg Uniformity", "Avg Clean Cup", "Avg Sweetness", "Avg Moisture", 
            "Avg Quakers", "Avg Defects One", "Avg Defects Two", "Record Count"
        ]
        country_table = create_table(country_data, headers)
        return [
            html.H2("Country Data"),
            country_table
        ]
    elif button_id == "show-continent-button":
        continent_data = get_continent_data()
        headers = [
            "Origin", "Avg Aroma", "Avg Flavor", "Avg Aftertaste", "Avg Acidity", "Avg Body", 
            "Avg Balance", "Avg Uniformity", "Avg Clean Cup", "Avg Sweetness", "Avg Moisture", 
            "Avg Quakers", "Avg Defects One", "Avg Defects Two", "Record Count"
        ]
        continent_table = create_table(continent_data, headers)
        return [
            html.H2("Continent Data"),
            continent_table
        ]
    elif button_id == "show-batch-button":
        batch_data = get_batch_data()
        headers = [
            "Rec ID", "Continent FK", "Country FK", "Processing Method", "Harvest Year", "Expiration Date"
        ]
        batch_table = create_table(batch_data, headers)
        return [
            html.H2("Coffee Batch Data"),
            batch_table
        ]
    elif button_id == "show-locations-button":
        locations_data = get_locations()
        headers = [
            "Continent FK", "Country FK"
        ]
        locations_table = create_table(locations_data, headers)
        return [
            html.H2("Locations Data"),
            locations_table
        ]
    elif button_id == "show-quality-button":
        quality_data = get_quality_data()
        headers = [
            "Rec ID FK", "Species", "Variety", "Color", "Aroma", "Flavor", "Aftertaste", "Acidity", 
            "Body", "Balance", "Uniformity", "Clean Cup", "Sweetness", "Moisture", "Quakers", 
            "Defect One", "Defect Two"
        ]
        quality_table = create_table(quality_data, headers)
        return [
            html.H2("Coffee Quality Data"),
            quality_table
        ]

    return []
@app.callback(
    Output("pie-charts-container", "children"),
    [Input("show-continent-quality-pie-button", "n_clicks")]
)
def display_continent_pie_charts(n_clicks_quality_pie):
    if not n_clicks_quality_pie:
        return []
    continent_data = get_continent_data()
    if not continent_data:
        return []
    continent_names = [row[0] for row in continent_data]
    column_names = continent_data[0][1:]
    column_values = [row[1:] for row in continent_data]
    pie_charts = []
    attribute_names = [
        "AVG_Aroma", "AVG_Flavor", "AVG_Aftertaste", "AVG_Acidity", "AVG_Body", 
        "AVG_Balance", "AVG_Uniformity", "AVG_Clean.Cup", "AVG_Sweetness", "AVG_Moisture", 
        "AVG_Quakers", "AVG_Category.One.Defects", "AVG_Category.Two.Defects", "Record Count"
    ]
    for i, column in enumerate(column_names):
        values = [row[i] for row in column_values]
        total_value = sum(values)
        percentages = [value / total_value * 100 for value in values]
        percentages = [round(percentage, 2) for percentage in percentages]

        pie_chart_data = go.Figure(
            data=[go.Pie(labels=continent_names, values=percentages, hole=0.3)],
            layout=go.Layout(title=f"Pie Chart for {attribute_names[i]}")
        )
        pie_charts.append(dcc.Graph(figure=pie_chart_data))
    return pie_charts

@app.callback(
    Output("bar-charts-container", "children"),
    [Input("show-country-quality-bar-button", "n_clicks")]
)
def display_country_bar_charts(n_clicks_quality_bar):
    if not n_clicks_quality_bar:
        return []
    country_data = get_countries_data()
    if not country_data:
        return []
    country_names = [row[0] for row in country_data]

    attribute_names = [
        "AVG_Aroma", "AVG_Flavor", "AVG_Aftertaste", "AVG_Acidity", "AVG_Body", 
        "AVG_Balance", "AVG_Uniformity", "AVG_Clean.Cup", "AVG_Sweetness", "AVG_Moisture", 
        "AVG_Quakers", "AVG_Category.One.Defects", "AVG_Category.Two.Defects", "Record Count"
    ]

    attribute_data = {name: [row[i+1] for row in country_data] for i, name in enumerate(attribute_names)}
    bar_charts = []
    for name in attribute_names:
        values = attribute_data[name]
        bar_chart_data = go.Figure(
            data=[go.Bar(x=country_names, y=values)],
            layout=go.Layout(title=f"Bar Chart for {name}")
        )
        bar_charts.append(dcc.Graph(figure=bar_chart_data))
    return bar_charts


if __name__ == '__main__':
    app.run_server(debug=True)
