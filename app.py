import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from reader import open_serial_connection, read_sensor_data

app = dash.Dash(__name__)

serial_connection = open_serial_connection()

app.layout = html.Div([
    html.H1('Dashboard de Monitoramento da Qualidade do Ar'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,
        n_intervals=0
    )
])

@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    data = read_sensor_data(serial_connection)
    if data is not None:
        df = pd.DataFrame([data])
        df['Timestamp'] = pd.Timestamp('now')
    else:
        df = pd.DataFrame(columns=['Timestamp', 'K', 'Na', 'Cl'])

    fig = px.line(df, x='Timestamp', y=['K', 'Na', 'Cl'],
                  title='Concentrações de K, Na e Cl ao longo do tempo')
    return fig

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)