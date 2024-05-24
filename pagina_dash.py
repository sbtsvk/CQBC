import dash
from dash import html
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
    query = "select distinct continent_fk, country_fk from coffee_batch where country_fk is not null order by country_fk"
    return fetch_data_from_db(query)
def create_table(data, headers):
    return html.Table([
        html.Tr([html.Th(header) for header in headers]),
        html.Tbody([
            html.Tr([html.Td(cell) for cell in row]) for row in data
        ])
    ])

app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1("CuppingData: Quality of Coffee By Countries (QCBC)")
    ]),
    html.Div(className='container', children=[
        html.Div(className='content', children=[
            html.P("Analizing what you are drinking... ... ..."),
            html.Button("Show Country Data", id="show-country-button", n_clicks=0),
            html.Button("Show Continent Data", id="show-continent-button", n_clicks=0),
            html.Button("Show Coffee Batch Data", id="show-batch-button", n_clicks=0),
            html.Button("Show Coffee Quality Data", id="show-quality-button", n_clicks=0),
            html.Button("Show Analized Countries", id="show-locations-button", n_clicks=0),  # New button
            html.Div(id="tables-container")
        ])
    ]),
])


@app.callback(
    Output("tables-container", "children"),
    [
        Input("show-country-button", "n_clicks"),
        Input("show-continent-button", "n_clicks"),
        Input("show-batch-button", "n_clicks"),
        Input("show-locations-button", "n_clicks"),
        Input("show-quality-button", "n_clicks")  # New input
    ]
)
def display_tables(n_clicks_country, n_clicks_continent, n_clicks_batch, n_clicks_locations, n_clicks_quality):  # Updated function signature
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
    elif button_id == "show-quality-button":  # New condition
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

if __name__ == '__main__':
    app.run_server(debug=True)
