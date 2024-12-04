import plotly.graph_objects as go
import plotly.express as px

# Mapa de calor con incendios (Heatmap with fires)
def create_densitymap(df_grouped, years):

    fig = go.FigureWidget()

    def add_trace(year):
        df_year = df_grouped[df_grouped['anio'] == year]
        trace = go.Densitymapbox(
            lat=df_year['latitud'],
            lon=df_year['longitud'],
            z=df_year['count'],
            radius=10,
            colorscale='Hot',
            colorbar=dict(title="Wildfires"),
            hovertemplate="Latitud: %{lat}<br>Longitud: %{lon}<br>Count: %{z}")
        fig.add_trace(trace)

    for year in years:
        add_trace(year)

    for i in range(1, len(years)):
        fig.data[i].update(visible=False)

    # Slider
    steps = []
    for i, year in enumerate(years):
        step = dict(
            method="update",
            args=[{"visible": [False] * len(years)},
                  {"title": f"Incendios Forestales en {year}"}],
            label=str(year)
        )
        step["args"][0]["visible"][i] = True
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Año: "},
        steps=steps
    )]

    fig.update_layout(
        title=None,
        sliders=sliders,
        mapbox_style="carto-positron",
        mapbox_center={"lat": 40, "lon": -4},
        mapbox_zoom=4,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig
# Crear serie temporal incendios
def create_timeseries(df):
  
  df_grouped = df.groupby(['fecha', 'combustible']).size().reset_index(name='num_incendios')
  fig = px.line(df_grouped, x='fecha', y='num_incendios', color='combustible',
              labels={'fecha': 'Año', 'num_incendios': 'Número de incendios', 'combustible': 'Combustible'})

  # Menú para filtrar
  fig.update_layout(
      plot_bgcolor='white',
      xaxis_showgrid=True,
      yaxis_showgrid=True,
      updatemenus=[
          dict(
              type="dropdown",
              direction="down",
              buttons=list([
                  dict(label='Total',
                       method='update',
                       args=[{'visible': [True] * len(df['combustible'].unique())}]),
                  * [dict(label=l,
                          method='update',
                          args=[{'visible': [d['name'] == l for d in fig.data]}])
                   for l in df['combustible'].unique()]
              ]),
              active=0
          )
      ]
  )

  return fig

# Visualizar en semi-círculo índice peligrosidad incendio
def visualize_danger_level(predicted_peligro):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = predicted_peligro,
        title = {"text": "Nivel Peligro Incendio"},
        gauge = {
            'axis': {'range': [None, 5]},
            'bar': {'color': "darkgray"},
            'steps': [
                {'range': [0, 1], 'color': "green"},
                {'range': [1, 3], 'color': "orange"},
                {'range': [3, 5], 'color': "red"}
            ]
        }
    ))
    return fig





