# Importar librerias
import dash
from src import graphics, etl
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Importar modulos
import src.etl
import src.graphics
from src.model import train_and_save_model, load_model
from src.API import get_weather_data

df, df_model = etl.load_data()
df_grouped = df.groupby(['anio', 'latitud', 'longitud']).size().reset_index(name='count')
years = df_grouped['anio'].unique()

TF_ENABLE_ONEDNN_OPTS=0

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

server = app.server

# API tiempo para datos en tiempo real
api_key = "6a2d1d6819634ac39e3222734241911"
temperature, humidity, wind_veloc, loc, city = get_weather_data(api_key)

layout_state = "dashboard"

def get_layout():
    if layout_state == "dashboard":
        return create_dashboard_layout()
    else:
        return new_page_layout()

def create_dashboard_layout():
    return html.Div([
        dbc.Container([
            dbc.Row([
                # Mapa de calor incendios
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Evolución Anual Distribución de Incendios Forestales"),
                            dbc.CardBody(
                                dcc.Graph(
                                    id="fire-map",
                                    figure=graphics.create_densitymap(df_grouped, years),
                                    style={'width': '100%', 'height': '400px'}
                                )
                            )
                        ],
                        color="#f5f8fa",
                        style={"margin": 10}
                    ),
                    width=6
                ),
                # Informacion en tiempo real y Boton prevenir incendio
                dbc.Col(
                    [
                        # Informacion en tiempo real
                        dbc.Card(
                            [
                                dbc.CardHeader("Actualidad"),
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardBody([
                                                        html.Div(className="info-container", style={"display": "flex", "flex-direction": "column", "align-items": "center"}, children=[
                                                            html.Div(style={"display": "flex", "align-items": "center"}, children=[
                                                                html.Img(src=dash.get_asset_url('temperature.png'), style={"width": 30, "height": 30, "margin-right": 5}),
                                                                html.Span(f"{temperature}ºC")
                                                            ])
                                                        ])
                                                    ])
                                                ],
                                                color="#f0f2f5",
                                                style={"margin": 5}
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardBody([
                                                        html.Div(className="info-container", style={"display": "flex", "flex-direction": "column", "align-items": "center"}, children=[
                                                            html.Div(style={"display": "flex", "align-items": "center"}, children=[
                                                                html.Img(src=dash.get_asset_url('humedad.png'), style={"width": 30, "height": 30, "margin-right": 5}),
                                                                html.Span(f"{humidity}%")
                                                            ])
                                                        ])
                                                    ])
                                                ],
                                                color="#f0f2f5",
                                                style={"margin": 5}
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardBody([
                                                        html.Div(className="info-container", style={"display": "flex", "flex-direction": "column", "align-items": "center"}, children=[
                                                            html.Div(style={"display": "flex", "align-items": "center"}, children=[
                                                                html.Img(src=dash.get_asset_url('ventoso.png'), style={"width": 30, "height": 30, "margin-right": 5}),
                                                                html.Span(f"{wind_veloc}km/h")
                                                            ])
                                                        ])
                                                    ])
                                                ],
                                                color="#f0f2f5",
                                                style={"margin": 5}
                                            ),
                                            width=4
                                        ),
                                        dbc.Col(
                                            dbc.Card(
                                                [
                                                    dbc.CardBody([
                                                        html.Div(className="info-container", style={"display": "flex", "flex-direction": "column", "align-items": "center"}, children=[
                                                            html.Div(style={"display": "flex", "align-items": "center"}, children=[
                                                                html.Img(src=dash.get_asset_url('sitio.png'), style={"width": 25, "height": 25, "margin-right": 5}),
                                                                html.Span(f"{city}\n{loc}")
                                                            ])
                                                        ])
                                                    ])
                                                ],
                                                color="#f0f2f5",
                                                style={"margin": 10,"text-align":"center"}
                                            ),
                                            width=12
                                        ),
                                    ])
                                ])
                            ],
                            color="#f5f8fa",
                            style={"margin": 10}
                        ),
                        # Boton Riesgo Incendio
                        dbc.Button(
                                    children="RIESGO INCENDIO FORESTAL",
                                    id="emergency-button",
                                    n_clicks=0,
                                    className="emergency-button",
                                    style={"margin":10,"margin-top": 50, "width":400, "height":80, 'text-align': 'center', "color":"black","background-color":"transparent","border": "2px solid black"}
                        )
                    ],
                    width=6
                )
            ]),
            dbc.Row([
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Evolución Mensual Incendios Forestales"),
                        dbc.CardBody(
                            dcc.Graph(
                                id="time-map",
                                figure=graphics.create_timeseries(df),
                                style={'width': '100%', 'height': '400px'}
                            )
                        )
                    ],
                    color="#f5f8fa",
                    style={"margin": 10}
                )
            )
        ])
    ])
    ])


def new_page_layout():
  return html.Div([
    html.Div(
      children=[
        html.H1("Estimación Peligro Incendio", style={'text-align': 'center', 'color': 'black', 'font-weight': 'bold'}),
        html.Div(style={"width": "900px", "margin": "0 auto"}, children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Detalles Zona"),
                        dbc.CardBody([
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.Div(className="input-container",children=[
                                            html.Label("Comunidad:"),
                                            dcc.Input(id="comunidad-input", type="number",style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Provincia:"),
                                            dcc.Input(id="provincia-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Latitud:"),
                                            dcc.Input(id="lat-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Longitud:"),
                                            dcc.Input(id="long-input", type="number",style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Altitud:"),
                                            dcc.Input(id="altitud-input", type="number", style={"width":"70px"}),
                                        ]),
                                    ], width=4),
                                    dbc.Col([
                                        html.Div(className="input-container",children=[
                                            html.Label("Lugar detección:"),
                                            dcc.Input(id="lugar-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Combustible:"),
                                            dcc.Input(id="combustible-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Momento del dia:"),
                                            dcc.Input(id="hora-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Clase de dia:"),
                                            dcc.Input(id="dia-input", type="number",style={"width":"70px"}),
                                        ]),
                                    ], width=4),
                                    dbc.Col([
                                        html.Div(className="input-container",children=[
                                            html.Label("Humedad:"),
                                            dcc.Input(id="humedad-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Velocidad Viento:"),
                                            dcc.Input(id="viento-input", type="number", style={"width":"70px"}),
                                        ]),
                                        html.Div(className="input-container",children=[
                                            html.Label("Temperatura:"),
                                            dcc.Input(id="temperatura-input", type="number", style={"width":"70px"}),
                                        ]),
                                    ], width=4)
                                ])
                            ])
                        ])
                        ],
                        color="#f5f8fa",
                        style={"margin": 10, "width":"450px", "height":"500px"}
                    ),
                    dbc.Button(
                        children="Predecir Peligro",
                        id="predict-button",
                        n_clicks=0,
                        className="predict-button",
                        style={"margin": 10},
                    )
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                    dbc.Card(
                        [
                        dbc.CardHeader("Nivel Peligro"),
                        dbc.CardBody(
                            html.Div(id="prediction-output")
                        )
                        ],
                        color="#f5f8fa",
                        style={"margin": 10}
                    )
                    ],
                    width=6
                )
            ]),
            # Botón regreso a página principal
            dbc.Row([
            dbc.Col([
                dbc.Button(
                    "Atrás",
                    href="/",
                    style={
                        "background-color": "transparent",
                        "border": "2px solid black",
                        "border-radius": "5px",
                        "padding": "10px 20px",
                        "cursor": "pointer",
                        "color": "black"
                    } 
                )
            ], width=12)
            ])
        ])
      ]
    )
  ])


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    global layout_state
    if pathname == '/emergency-page':
        layout_state = "emergency"
    else:
        layout_state = "dashboard"
    return get_layout()

@app.callback(
    Output('url', 'pathname'),
    [Input('emergency-button', 'n_clicks')]
)
def navigate_to_emergency_page(n_clicks):
    if n_clicks > 0:
        return '/emergency-page'
    return dash.no_update

@app.callback(
    Output("prediction-output", "children"),
    [
        Input("predict-button", "n_clicks"),
        Input("comunidad-input", "value"),
        Input("provincia-input", "value"),
        Input("lat-input", "value"),
        Input("long-input", "value"),
        Input("altitud-input", "value"),
        Input("lugar-input", "value"),
        Input("combustible-input", "value"),
        Input("hora-input", "value"),
        Input("dia-input", "value"),
        Input("humedad-input", "value"),
        Input("viento-input", "value"),
        Input("temperatura-input", "value")
    ],
)
def predict(n_clicks, comunidad_id, provincia_id, lat_id, long_id, altitud_id, lugar_id,combustible_id, hora_id, dia_id, humedad_id, viento_id, temperatura_id):
    
    if n_clicks > 0:
        if any([x is None or x == "" for x in [comunidad_id, provincia_id, lat_id, long_id, altitud_id, lugar_id, combustible_id, hora_id, dia_id, humedad_id, viento_id, temperatura_id]]):
            return html.Div("Por favor rellene todos los campos para poder realizar una predicción precisa.", style={'color': 'red'})
        model_peligro = src.model.load_model('idpeligro')

        X = np.array([[comunidad_id, provincia_id, lat_id, long_id, altitud_id, lugar_id,combustible_id, hora_id, dia_id, humedad_id, viento_id, temperatura_id]])

        # Make prediction using the model
        predicted_peligro = np.ceil(model_peligro.predict(X)[0])

        gauge_chart = dcc.Graph(
            id='danger-gauge',
            figure=graphics.visualize_danger_level(predicted_peligro),
            style={'width': '100%', 'height': '300px'}
        )

        niveles_peligro = {
            0: "Prealerta: Indica un nivel de riesgo bajo. El riesgo de incendio es mínimo.",
            1: "Alerta: Existe riesgo de incendio moderado. Se recomienda estar atentos a cambios en las condiciones meteorológicas.",
            2: "Alarma: El riesgo de incendio es alto. Se deben tomar medidas preventivas y estar preparados para una posible emergencia.",
            3: "Alarma extrema: El riesgo de incendio es extremadamente alto. Se deben seguir estrictamente las recomendaciones de las autoridades y estar listos para evacuar si es necesario."
        }

        descripcion_peligro = niveles_peligro.get(predicted_peligro, "Nivel de peligro desconocido")

        return html.Div([
            gauge_chart,
            html.P(descripcion_peligro)
        ])
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)