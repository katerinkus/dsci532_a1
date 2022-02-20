import altair as alt
from dash import Dash, html, dcc, Input, Output
import pandas as pd
alt.data_transformers.enable('data_server')

tree_df = pd.read_csv("data/street-trees.csv", sep=";")
cherry_df = tree_df.loc[tree_df["GENUS_NAME"] == "PRUNUS"].dropna(subset=["DIAMETER"])

cherry_df["DIAMETER_CM"] = cherry_df["DIAMETER"] * 2.54
cherry_filt = cherry_df.loc[cherry_df["DIAMETER_CM"] < 150]
n_names = cherry_df["NEIGHBOURHOOD_NAME"].unique().tolist()
n_names.sort()

def plot_altair(nei1):
    chart = alt.Chart(
        cherry_filt.loc[(cherry_filt['NEIGHBOURHOOD_NAME'] == nei1) | (cherry_filt['NEIGHBOURHOOD_NAME'] == 'DOWNTOWN')], 
        title="Cherry tree diameter distribution").transform_density(
        'DIAMETER_CM',
        groupby=['NEIGHBOURHOOD_NAME'],
        as_=['DIAMETER', 'density']).mark_area(interpolate='monotone', opacity=0.4, line=({'color':'#a75ea8'})).encode(
        alt.X('DIAMETER', title = 'Tree diameter (cm)', scale=alt.Scale(nice=False)),
        alt.Y('density:Q', title="Density", axis=alt.Axis(labels=False)),
        alt.Color('NEIGHBOURHOOD_NAME',  scale=alt.Scale(domain=['WEST END', 'DOWNTOWN'], range=['#ae68d4', '#6993db']))
    )
    return chart.to_html()

app = Dash(__name__, external_stylesheets=[
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap'])
app.layout = html.Div([
        html.H1('Cherry tree diameter'),
        html.Div([
            'Select two Vancouver neighbourhoods to compare',
            dcc.Dropdown(n_names, 'DOWNTOWN', id='nei1'),
            dcc.Dropdown(n_names, 'WEST END', id='nei2')
            ], style={'border-width': '0', 'width': '25%', 'margin-bottom': '10px'}),
        html.Iframe(
            id='density_plot',
            srcDoc=plot_altair(nei1='WEST END'),
            style={'border-width': '0', 'width': '100%', 'height': '800px'})],
            style={'font-family': 'Montserrat'})

@app.callback(
    Output('density_plot', 'srcDoc'),
    Input('nei1', 'value'))
def update_output(nei1):
    return plot_altair(nei1)


if __name__ == '__main__':
    app.run_server(debug=True)