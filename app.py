import dash
import json
import pandas as pd
import plotly as py
import base64

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from plotly.graph_objs import *
from dash.dependencies import Input, Output

# ------------------------------------------------------------------------------
# Import and clean data

with open('./data/IDN_adm_1_province.json') as f:
    geodata = json.load(f)
    # print(geodata)

data_penduduk = pd.read_csv("./data/jumlah_penduduk_1971-2019.csv")
df_choropleth = data_penduduk.copy()
df_choropleth = df_choropleth[df_choropleth.Provinsi != 'Indonesia']

options_list = list(df_choropleth.columns[1:])


# ------------------------------------------------------------------------------
# Load Image

path_arrow = './assets/up-arrow.png'
path_new = './assets/new.png'
path_question = './assets/question.png'
path_graph = './assets/graph.png'

encoded_up_arrow = base64.b64encode(open(path_arrow, 'rb').read())
encoded_new = base64.b64encode(open(path_new, 'rb').read())
encoded_question = base64.b64encode(open(path_question, 'rb').read())
encoded_graph = base64.b64encode(open(path_graph, 'rb').read())


# ------------------------------------------------------------------------------
# Initiate app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Pertumbuhan Penduduk RI'


def create_line_chart():
    figure = go.Figure()
    figure.update_layout(
        title={
            'text': '<b>Jumlah Penduduk Indonesia dari Tahun 1971 - 2019</b>',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(color='black'),
        xaxis=dict(
            title='Tahun',
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
        ),
        yaxis=dict(
            title='Jumlah Penduduk',
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='rgb(204, 204, 204)',
        ),
        plot_bgcolor='white',
        annotations=[(dict(xref='paper', yref='paper', x=0.5, y=-0.2,
                           xanchor='center', yanchor='top',
                           text='Sumber: Badan Pusat Statistik (https://www.bps.go.id/)',
                           font=dict(family='Arial',
                                     size=12,
                                     color='rgb(150,150,150)'),
                           showarrow=False))]
    )
    
    tahun = list(df_choropleth.columns[1:])

    for provinsi in df_choropleth.Provinsi:
        penduduk_tiap_tahun = df_choropleth.iloc[:, 1:].loc[df_choropleth['Provinsi'] == provinsi].values.flatten().tolist()

        if provinsi == 'Jawa Barat':
            figure.add_trace(go.Scatter(x=tahun, 
                                        y=penduduk_tiap_tahun,
                                        mode='lines',
                                        name=provinsi,
                                        showlegend=True,
                                        line=dict(color='#B21727', width=7)
                            )
            )

        elif provinsi == 'Jawa Timur':
            figure.add_trace(go.Scatter(x=tahun, 
                                        y=penduduk_tiap_tahun,
                                        mode='lines',
                                        name=provinsi,
                                        showlegend=True,
                                        line=dict(color='#DC626E', width=5)
                            )
            )
        elif provinsi == 'Jawa Tengah':
            figure.add_trace(go.Scatter(x=tahun, 
                                        y=penduduk_tiap_tahun,
                                        mode='lines',
                                        name=provinsi,
                                        showlegend=True,
                                        line=dict(color='#F18E97', width=3)
                            )
            )
        elif provinsi == 'Kalimantan Utara':
            figure.add_trace(go.Scatter(x=tahun, 
                                        y=penduduk_tiap_tahun,
                                        mode='lines',
                                        name=provinsi,
                                        showlegend=True,
                                        line=dict(color='#F1C511', width=7)
                            )
            )
        elif provinsi == 'Maluku':
            figure.add_trace(go.Scatter(x=tahun, 
                                        y=penduduk_tiap_tahun,
                                        mode='lines',
                                        name=provinsi,
                                        showlegend=True,
                                        line=dict(color='#67B224', width=7)
                            )
            )
        else:
            figure.add_trace(go.Scatter(x=tahun, 
                                        y=penduduk_tiap_tahun,
                                        mode='lines',
                                        name=provinsi,
                                        showlegend=False,
                                        line=dict(color='#C4C3C2')
                            )
            )

    return figure


# ------------------------------------------------------------------------------
# App layout

app.layout = html.Div([
    dbc.Container([
        html.H2('Jumlah Penduduk Indonesia per Provinsi', style={'font-weight': 'bold', 'margin-left': '10%'}),
        dbc.Row([
            dbc.Col([
                html.H1('3', style={'margin': '10px', 'font-size': '80px', 'color': '#B21727'}),
                html.P(children=[
                    html.Span('Provinsi dengan '),
                    html.B('jumlah penduduk terbanyak '),
                    html.Span('berada di '),
                    html.B('Pulau Jawa '),
                    html.Br(),
                    html.Span('(saat ini di atas 34 juta).'),
                    html.Br(),
                    html.Br(),
                    html.Span('Berdasarkan '),
                    html.A('Wikipedia, ', href='https://en.wikipedia.org/wiki/List_of_islands_by_population'),
                    html.Span('Pulau Jawa merupakan '),
                    html.B('pulau dengan jumlah penduduk terbanyak di dunia.'),
                    html.Br(),
                    html.Br(),
                ], style={'margin-left': '10%', 'margin-right': '10%'}),
            ], style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '33%',
                'text-align': 'center'}
            ),
            dbc.Col([
                html.Img(src='data:image/png;base64,{}'.format(encoded_up_arrow.decode()), height=70,
                         style={'margin-top': '30px'}),
                html.P(children=[
                    html.Span('Pertumbuhan jumlah penduduk terjadi secara '),
                    html.B('signifikan '),
                    html.Span('di provinsi '),
                    html.B('Jawa Barat.'),
                    html.Br(),
                    html.Br(),
                    html.Span('Sedangkan provinsi lainnya cenderung landai.'),
                ], style={'margin-top': '15%', 'margin-left': '10%', 'margin-right': '10%'}),
            ], style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '33%',
                'margin-left': '3%',
                'text-align': 'center'}
            ),
            dbc.Col([
                html.Img(src='data:image/png;base64,{}'.format(encoded_new.decode()), height=70,
                         style={'right': '0', 'position': 'absolute'}),
                html.P(children=[
                    html.Span('Jumlah penduduk di beberapa provinsi masih sedikit, beberapa di antaranya karena merupakan '),
                    html.B('provinsi baru'),
                    html.Span(', seperti Kalimantan Utara, Papua Barat, dan Sulawesi Barat.'),
                    html.Br(),
                    html.Br(),
                    html.Span('Terlepas dari provinsi baru atau bukan, penduduk provinsi di '),
                    html.B('luar Pulau Jawa cenderung lebih sedikit '),
                    html.Span('(berjumlah di bawah 15 juta).'),
                    html.Br(),
                    html.Br()
                ], style={'margin-top': '15%', 'margin-left': '10%', 'margin-right': '10%'}),
            ], style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '33%',
                'margin-left': '3%',
                'text-align': 'center'}
            ),
        ], style={'margin-top': '20px', 'margin-left': '10%',
                  'display': 'flex', 'justify-content': 'space-between'}
        ),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Tampilkan data tahun:',
                                dcc.Dropdown(id='dropdown_tahun',
                                             options=[{'label': i, 'value': i} for i in options_list],
                                             multi=False,
                                             clearable=False,
                                             value=options_list[-1],
                                             style={'font-weight': 'normal'})]),
                ], style={'width': '165px'}
            )], style={'display': 'flex', 'align-items': 'center', 'margin-left': '50px'}),

            dbc.Col([
                dcc.Loading([
                    dcc.Graph(id='choropleth_indonesia',
                              figure={}
                    )
                ], type='default', color="#B21727"),
            ]),
        ],
            style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '100%',
                'height': '450px',
                'margin-top': '20px',
                'margin-left': '10%',
                'margin-right': '10%',
                'display': 'flex',
                'justify-content': 'space-between'}
        ),

        dbc.Row([
            dbc.Col([
                html.H1('10', style={'margin': '10px', 'font-size': '80px', 'color': '#B21727'}),
                html.P(children=[
                    html.Span('Provinsi dengan '),
                    html.B('jumlah penduduk terbanyak: '),
                    html.Br(),
                    html.Span('(per tahun 2019)'),
                    html.Br(),
                    html.Br(),
                ], style={'margin-left': '10%', 'margin-right': '10%'}),
                html.P(children=[
                    html.Span('1. Jawa Barat (49.3 juta)'),
                    html.Br(),
                    html.Span('2. Jawa Timur (39.6 juta)'),
                    html.Br(),
                    html.Span('3. Jawa Tengah (34.7 juta)'),
                    html.Br(),
                    html.Span('4. Sumatera Utara (14.5 juta)'),
                    html.Br(),
                    html.Span('5. Banten (12.9 juta)'),
                    html.Br(),
                    html.Span('6. DKI Jakarta (10.5 juta)'),
                    html.Br(),
                    html.Span('7. Sulawesi Selatan (8.8 juta)'),
                    html.Br(),
                    html.Span('8. Sumatera Selatan (8.47 juta)'),
                    html.Br(),
                    html.Span('9. Lampung (8.44 juta)'),
                    html.Br(),
                    html.Span('10. Riau (6.9 juta)'),
                    html.Br(),
                ], style={'margin-left': '10%', 'margin-right': '10%', 'text-align': 'left'}),
            ], style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '33%',
                'text-align': 'center'}
            ),
            dbc.Col([
                html.Img(src='data:image/png;base64,{}'.format(encoded_graph.decode()), height=100,
                         style={'margin-top': '30px'}),
                html.P(children=[
                    html.Span('Semua provinsi terus mengalami peningkatan jumlah penduduk secara linear, hanya '),
                    html.B('sedikit yang pernah mengalami penurunan.'),
                    html.Br(),
                    html.Br(),
                    html.Span('Penurunan penduduk yang paling terlihat adalah di provinsi '),
                    html.B('Jawa Barat pada tahun 1995-2000*.'),
                    html.Br(),
                    html.Br()
                ], style={'margin-top': '15%', 'margin-left': '10%', 'margin-right': '10%'}),
                html.P('*Penyebab masih belum diketahui.', style={'font-size': '10px'})
            ], style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '33%',
                'margin-left': '3%',
                'text-align': 'center'}
            ),
            dbc.Col([
                html.Img(src='data:image/png;base64,{}'.format(encoded_question.decode()), height=80,
                         style={'margin-top': '30px'}),
                html.P(children=[
                    html.Span('Banyaknya penduduk di Pulau Jawa disebabkan karena '),
                    html.B('migrasi yang tinggi dan fasilitas kesehatan* yang baik. '),
                    html.Br(),
                    html.Br(),
                    html.Span('Pusat ekonomi dan pemerintahan yang dominan berada di Pulau Jawa '),
                    html.Span('menimbulkan efek domino, di mana '),
                    html.B('fasilitas pendidikan, kesehatan, dan akses internet '),
                    html.Span('di Pulau Jawa juga lebih memadai dibandingkan pulau lainnya.'),
                    html.Br(),
                    html.Br()
                ], style={'margin-top': '5%', 'margin-left': '10%', 'margin-right': '10%'}),
                html.P('*mendukung kelahiran dan mencegah kematian', style={'font-size': '10px'})
            ], style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '33%',
                'margin-left': '3%',
                'text-align': 'center'}
            )
        ], style={'margin-top': '20px', 'margin-left': '10%',
                  'display': 'flex', 'justify-content': 'space-between'}
        ),

        dbc.Row([
            dbc.Col([
                dcc.Loading([
                    dcc.Graph(id='line_chart',
                              figure=create_line_chart()
                    )
                ], type='default', color="#B21727"),
            ]),
        ],
            style={'background': 'white',
                'border-radius': '5px',
                'border': '1px solid #BEC2C4',
                'box-shadow': '3px 3px 5px #B21727',
                'width': '100%',
                'height': '450px',
                'margin-top': '20px',
                'margin-left': '10%',
                'margin-right': '10%',
                'text-align': 'center'}
        ),

    ], style={'margin': '5px 5px 5px 5px', 'text-align': 'left'}),

    html.Br(),
    dbc.Row([
        html.A('Code on Github', href='https://github.com/celineinc/DataKependudukanIndonesia'),
        html.A('Data Penduduk', href='https://www.bps.go.id/indikator/indikator/view_data_pub/0000/api_pub/50/da_03/1'),
        html.A('Data GeoJSON', href='https://github.com/superpikar/indonesia-geojson')
    ], style={'margin-left': '10%', 'margin-right': '10%',
              'display': 'flex', 'justify-content': 'space-evenly'})
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(Output('choropleth_indonesia', 'figure'),
              [Input('dropdown_tahun', 'value')])
def update_choropleth(selected_year):
    figure = go.Figure()
    figure.add_trace(
        go.Choropleth(geojson=geodata,
                      locations=df_choropleth.Provinsi,
                      z=df_choropleth[selected_year],
                      zmax=50000000,
                      zmin=0,
                      featureidkey='properties.NAME_1',
                      marker_line_color='black',
                      colorscale='Reds',
                      colorbar_title='<b>Jumlah Penduduk<b>')
    )
    figure.update_layout(
        title='<b>Peta Jumlah Penduduk Indonesia Tahun </b><b>' + selected_year + '</b>',
        geo_scope='asia',
        geo_projection_scale=3,
        geo_center_lat=0,
        geo_center_lon=118,
        font=dict(color='black'),
        margin={"r": 5, "t": 100, "l": 5, "b": 50}
    )

    return figure


# ------------------------------------------------------------------------------
# Run the app

if __name__ == '__main__':
    app.run_server(debug=True)
