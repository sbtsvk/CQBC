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
        print("Data fetched successfully:", data)
        return data
    except psy.OperationalError as e:
        print(f"Unable to connect to database. Error: {e}")
        return None

def get_countries_data():
    query = "SELECT country_origin, avg_aroma FROM country;"
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
app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1("Calidad del Café por País")
    ]),
    html.Div(className='container', children=[
        html.Div(className='content', children=[
            html.P("Todos los paises y continentes para el análisis de los datos:) ."),
            html.Table([
                html.Tr([html.Th("Continent"), html.Th("Country")]),
                html.Tbody([
                    html.Tr([html.Td(continent), html.Td(country)]) for continent, country in get_locations()
                ])
            ])
        ])
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
