# 1. Importar bibliotecas
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# 2. Ler os dados
df = pd.read_csv('ecommerce_estatistica.csv')

# 3. Iniciar a aplicação Dash
app = dash.Dash(__name__)
server = app.server

# 4. Layout da aplicação
app.layout = html.Div([
    html.H1('Dashboard - E-commerce Estatística', style={'textAlign': 'center'}),

    # Filtros interativos
    html.Div([
        html.Label('Filtrar Gênero:'),
        dcc.Dropdown(
            options=[{'label': genero, 'value': genero} for genero in df['Gênero'].unique()],
            value=None,
            placeholder='Selecione o gênero',
            id='filtro-genero'
        ),

        html.Br(),

        html.Label('Filtrar Nota Mínima:'),
        dcc.Slider(
            min=df['Nota'].min(),
            max=df['Nota'].max(),
            step=0.1,
            value=df['Nota'].min(),
            marks={i: str(i) for i in range(int(df['Nota'].min()), int(df['Nota'].max()) + 1)},
            id='filtro-nota'
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Br(),

    # Gráficos
    dcc.Graph(id='grafico-histograma'),
    dcc.Graph(id='grafico-dispersao')
])


# 5. Callbacks para atualizar os gráficos
@app.callback(
    [Output('grafico-histograma', 'figure'),
     Output('grafico-dispersao', 'figure')],
    [Input('filtro-genero', 'value'),
     Input('filtro-nota', 'value')]
)
def atualizar_graficos(genero_selecionado, nota_minima):
    df_filtrado = df.copy()

    # Aplicar filtro de gênero
    if genero_selecionado:
        df_filtrado = df_filtrado[df_filtrado['Gênero'] == genero_selecionado]

    # Aplicar filtro de nota mínima
    df_filtrado = df_filtrado[df_filtrado['Nota'] >= nota_minima]

    # Histograma atualizado
    fig_hist = px.histogram(df_filtrado, x='Nota', nbins=20, marginal='box',
                            title='Distribuição das Notas dos Produtos')

    # Dispersão atualizada
    fig_scatter = px.scatter(df_filtrado, x='N_Avaliações', y='Nota', color='Gênero',
                             title='Dispersão: Avaliações x Nota')

    return fig_hist, fig_scatter


# 6. Rodar a aplicação
if __name__ == '__main__':
        app.run(debug=True)

