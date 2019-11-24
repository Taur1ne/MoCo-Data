import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd

from app import app

url = 'https://data.montgomerycountymd.gov/resource/e54u-qx42.json'
df = pd.read_json(path_or_buf=url)

def normalize_age(petage: str) -> int:
    petage = petage.lower()
    new_petage = 0
    if 'year' in petage:
        new_petage = int(petage.split('year')[0]) * 12
    elif 'day' in petage:
        new_petage = round(int(petage.split('day')[0]) / 30)
    elif 'week' in petage:
        new_petage = round(int(petage.split('week')[0]) / 4)
    elif 'month' in petage:
        new_petage = int(petage.split('month')[0])
    else:
        new_petage = np.NaN
    return new_petage


def generate_table(dataframe, columns, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


def graph(dataframe, x_column):
    x = dataframe[x_column].unique()
    y = df.groupby(df[x_column])[x_column].count()
    return dcc.Graph(
        id='{} by count'.format(x_column),
        figure={
            'data': [
                    {'x': x, 'y': y, 'type': 'bar'}
                ]
        }
    )

df.petage = df.petage.apply(normalize_age)
pd.to_numeric(df.petage)

columns = ['animalid', 'intype', 'indate', 'petname', 'animaltype', 'petage',
           'petsize', 'color', 'breed']
    
layout = html.Div(children=[
        html.H3('Adoptable Pets!'),
        #generate_table(df, columns)
        graph(df, 'intype'),
        graph(df, 'animaltype')
])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
