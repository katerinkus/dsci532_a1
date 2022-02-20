import altair as alt
from dash import Dash, html, dcc
import pandas as pd
alt.data_transformers.enable('data_server')

tree_df = pd.read_csv("data/street-trees.csv", sep=";")
cherry_df = tree_df.loc[tree_df["GENUS_NAME"] == "PRUNUS"].dropna(subset=["DIAMETER"])

cherry_df["DIAMETER_CM"] = cherry_df["DIAMETER"] * 2.54
cherry_filt = cherry_df.loc[cherry_df["DIAMETER_CM"] < 150]
n_names = cherry_df["NEIGHBOURHOOD_NAME"].unique().tolist()
n_names.sort()

cherry_plot = alt.Chart(cherry_df).mark_bar().encode(y="count()", x="NEIGHBOURHOOD_NAME")

chart = alt.Chart(
    cherry_filt.query("NEIGHBOURHOOD_NAME == 'WEST END' | NEIGHBOURHOOD_NAME == 'DOWNTOWN'"), 
    title="Cherry tree diameter distribution").transform_density(
    'DIAMETER_CM',
    groupby=['NEIGHBOURHOOD_NAME'],
    as_=['DIAMETER', 'density']).mark_area(interpolate='monotone', opacity=0.4, line=({'color':'#a75ea8'})).encode(
    alt.X('DIAMETER', title = 'Tree diameter (cm)', scale=alt.Scale(nice=False)),
    alt.Y('density:Q', title="Density", axis=alt.Axis(labels=False)),
    alt.Color('NEIGHBOURHOOD_NAME',  scale=alt.Scale(domain=['WEST END', 'DOWNTOWN'], range=['#ae68d4', '#6993db']))
)

app = Dash(__name__, external_stylesheets=[
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap'])
app.layout = html.Div([
        html.H1('Cherry blossom diameter (cm)'),
        html.Div([
        'Select two neighbourhoods to compare',
        dcc.Dropdown(n_names, 'DOWNTOWN'),
        dcc.Dropdown(n_names, 'WEST END')
        ], style={'border-width': '0', 'width': '25%', 'margin-bottom': '10px'}),
        html.Iframe(srcDoc=chart.to_html(),
        style={'border-width': '0', 'width': '100%', 'height': '800px'})
        ], style={'font-family': 'Montserrat'})


if __name__ == '__main__':
    app.run_server(debug=True)