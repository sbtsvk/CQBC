import dash
from dash import html
import psycopg2 as psy

dbname = "QCBC"
user = "User1"
password = "Choq"
host = "localhost"
port = "5432"

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

app = dash.Dash(__name__, external_stylesheets=['C:\\Users\\Lenovo\\Desktop\\Proyecto_ing_datos\\ex.css'])

app.layout = html.Div([
    html.Div(className='header', children=[
        html.H1("Calidad del Café por País")
    ]),
    html.Div(className='container', children=[
        html.Div(className='content', children=[
            html.P("Cafeina :) ."),
        ])
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
