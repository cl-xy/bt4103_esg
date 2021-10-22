import ast
import random
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px  
import plotly.graph_objects as go

import dash
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.dependencies import Input, Output

# Bootstrap --------------------------------------------------------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MATERIA],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Load Data --------------------------------------------------------------------------

# Load company names to display in dropdown menu
companylabels_file = pd.read_csv('data/companylabels.csv', usecols=['FullName', 'ShortForm', 'Type'])

# For global initiatives table 
initiatives_file = pd.read_csv('data/esg_initiatives.csv')
# replace NaN for initiatives without acronym
initiatives_file = initiatives_file.replace({np.nan: '-'})
# dictionary: key-initiative spelled out fully, value-[acronym, description]
initiatives_dict = initiatives_file.set_index('Initiative').T.to_dict('list')
# read csv containing all initiatives
all_initiative_array = pd.read_csv('data/all_initiatives.csv')

# For WordCloud
dfm = pd.DataFrame({'word': ['climate', 'emission', 'esg', 'investment', 'energy', 'initiative', 'management', 'sustainability'], 
                    'freq': [20, 18, 16, 14, 11, 8, 7, 4]})
def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='white', width=480, height=400)
    wc.fit_words(d)
    return wc.to_image()

# For decarbonization rating
ratings_file = pd.read_csv('data/all_percentile.csv', usecols=['name', 'percentile'])

# For sentiment 
sentiment_file = pd.read_csv('data/sentiment_dummy.csv', usecols=['Company', 'Sentiment'])

# Cards --------------------------------------------------------------------------------
card_sentiment = dbc.Card([
    dbc.CardBody([
        html.H5('Overall Sentiment Level', className='text-center'),
        dcc.Graph(id='sentiment_gauge', figure={})
    ])
])

card_percentile_rank = dbc.Card([
    dbc.CardBody([
        html.H5('Percentile Rank', className='text-center'),
        dcc.Graph(id='percentile_barplot', figure={})
    ])
])

card_initiative_count = dbc.Card([
    dbc.CardBody([
        html.H5('Global Initiatives Count', className='text-center'),
        dcc.Graph(id='initiative_barplot', figure={})
    ])
])

card_initiative_table = dbc.Card([
    dbc.CardBody([
        html.H5('Global Initiatives', className='text-center'),
        dcc.Graph(id='initiative_table', figure={})
    ])
])

card_word_count = dbc.Card([
    dbc.CardBody([
        html.H5('Top 10 Word Count', className='text-center'),
        dcc.Graph(id='word_count', figure={})
    ])
])

# Layout -----------------------------------------------------------------------------
app.layout = dbc.Container([
    dbc.Row([ # First Row: Dashboard Header
        dbc.Col(html.H1('Decarbonization Dashboard',
                        className='text-center mb-4'),
                width=12)
    ]),
    dbc.Row([ # Second Row: 2 Dropdowns for the dashboard
        dbc.Col([
            dcc.Dropdown(id='type_of_fi_dropdown',
                        options=[
                            {'label': 'Asset Manager', 'value': 'am'}, 
                            {'label': 'Asian Bank', 'value': 'ab'}, 
                            {'label': 'Insurance Company', 'value': 'ins'}, 
                            {'label': 'Pension Fund', 'value': 'pf'}
                        ],
                        multi=False,
                        placeholder='Select Type of Financial Institution',
                        searchable=False)
        ], width={'size':4, 'offset':2, 'order':1}),
        dbc.Col([
            dcc.Dropdown(id='company_dropdown',
                        #options=[{'label': x[0], 'value': x[1]} for x in companylabels],
                        multi=False,
                        placeholder='Select a Company')
        ], width={'size':4, 'offset':0, 'order':2})
    ]),
    html.Br(),
    dbc.Row([
        dbc.CardDeck([card_sentiment, card_percentile_rank, card_initiative_count])
    ])
])

# Callback ----------------------------------------------------------------------------
# To filter for comapanies according to FI chosen in dropdown 1
@app.callback(
    Output(component_id='company_dropdown', component_property='options'),
    Input(component_id='type_of_fi_dropdown', component_property='value')
)
def update_dropdown(type_of_fi):
    sub_df = companylabels_file.loc[companylabels_file['Type'] == type_of_fi]
    options = [{'label': x[0], 'value': x[1]} for x in sub_df.values.tolist()]
    return options

# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)