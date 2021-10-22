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
all_initiative_array = pd.read_csv('data/all_initiatives.csv', usecols=['Company', 'Type', 'Initiatives'])

# For WordCloud
dfm = pd.DataFrame({'word': ['climate', 'emission', 'esg', 'investment', 'energy', 'initiative', 'management', 'sustainability'], 
                    'freq': [20, 18, 16, 14, 11, 8, 7, 4]})
def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='white', width=480, height=400)
    wc.fit_words(d)
    return wc.to_image()

# For decarbonization rating
ratings_file = pd.read_csv('data/all_percentile.csv', usecols=['name', 'percentile', 'type'])

# For sentiment 
sentiment_file = pd.read_csv('data/sentiment_dummy.csv', usecols=['Company', 'Sentiment', 'type'])

# Cards --------------------------------------------------------------------------------
card_sentiment = dbc.Card([
    dbc.CardBody([
        html.H5('Overall Sentiment Level', className='text-center'),
        dcc.Graph(id='sentiment_gauge', figure={})
    ])
])

card_percentile_rank = dbc.Card([
    dbc.CardBody([
        html.H5('Decarbonization Rating', className='text-center'),
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
            html.H6('Select Type of Financial Institution'), 
            dcc.Dropdown(id='type_of_fi_dropdown',
                        options=[
                            {'label': 'Asset Manager', 'value': 'am'}, 
                            {'label': 'Asian Bank', 'value': 'ab'}, 
                            {'label': 'Insurance Company', 'value': 'ins'}, 
                            {'label': 'Pension Fund', 'value': 'pf'}
                        ],
                        multi=False,
                        value='am',
                        searchable=False)
        ], width={'size':4, 'offset':2, 'order':1}),
        dbc.Col([
            html.H6('Select a Company'),
            dcc.Dropdown(id='company_dropdown',
                        multi=False,
                        value='Aegon')
        ], width={'size':4, 'offset':0, 'order':2})
    ]),
    html.Br(),
    dbc.Row([ # Third Row
        dbc.Col([card_sentiment], width={'size':4, 'offset':0, 'order':1}),
        dbc.Col([card_percentile_rank], width={'size':4, 'offset':0, 'order':2}),
        dbc.Col([card_initiative_count], width={'size':4, 'offset':0, 'order':3})
    ]),
    html.Br(),
    dbc.Row([ # Fourth Row
        dbc.Col([card_initiative_table], width={'size':7, 'offset':0, 'order':1}),
        dbc.Col([card_word_count], width={'size':5, 'offset':0, 'order':2})
    ])
], fluid=True)

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

# To update sentiment gauge chart
@app.callback(
    Output(component_id='sentiment_gauge', component_property='figure'),
    Input(component_id='company_dropdown', component_property='value')
)
def update_graph(company):
    sentiment = sentiment_file.set_index('Company').Sentiment.loc[company]

    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = sentiment, # company's sentiment
        mode = "gauge+number+delta",
        delta = {'reference': 3.7}, # average
        gauge = {'axis': {'range': [None, 5]},
                'bar': {'color': "black"},
                'steps' : [
                    {'range': [0, 1.25], 'color': "#F25757"}, 
                    {'range': [1.25, 2.5], 'color': "#FFC15E"}, 
                    {'range': [2.5, 3.75], 'color': "#F5FF90"}, 
                    {'range': [3.75, 5], 'color': "#58CC00"}], 
                'threshold' : {'line': {'color': "red", 'width': 3.7}, 'thickness': 0.75, 'value': 3.7}}))
    fig.update_layout(height = 200, margin = {'t':10, 'b':0})
    return fig

# To update barplot for percentile rank
@app.callback(
    Output(component_id='percentile_barplot', component_property='figure'),
    Input(component_id='company_dropdown', component_property='value')
)
def update_graph(company):
    rating = round(ratings_file.set_index('name').percentile.loc[company])
    average = 50
    fig = go.Figure(go.Bar(
            x=[rating, average],
            y=['Company', 'Average'],
            orientation='h',
            marker_color=['#4EADAF', '#88DEB0']))
    fig.update_traces(width=0.6)
    fig.update_layout(height = 200 , margin = {'t':10, 'b':0})
    return fig 

# To update barplot for initiative count
@app.callback(
    Output(component_id='initiative_barplot', component_property='figure'),
    Input(component_id='company_dropdown', component_property='value')
)
def update_graph(company):
    company_initiative = all_initiative_array.set_index('Company').Initiatives.loc[company]
    count = len(ast.literal_eval(company_initiative))
    average = 6
    fig = go.Figure(go.Bar(
            x=[count, average],
            y=['Company', 'Average'],
            orientation='h',
            marker_color=['#4EADAF', '#88DEB0']))
    fig.update_traces(width=0.6)
    fig.update_layout(height = 200 , margin = {'t':10, 'b':0})
    return fig 

# Global Initiatives Table
@app.callback(
    Output(component_id='initiative_table', component_property='figure'),
    Input(component_id='company_dropdown', component_property='value')
)
def update_graph(option_slctd):
    company_initiative = all_initiative_array.set_index('Company').Initiatives.loc[option_slctd]
    company_initiative = ast.literal_eval(company_initiative)
    company_initiative = sorted(company_initiative)
    
    data = []
    for full_name in company_initiative:
        acronym = initiatives_dict[full_name][0]
        details = initiatives_dict[full_name][1]  
        data.append([full_name, acronym, details])
    
    df = pd.DataFrame(data, columns = ['Initiatives', 'Acronym', 'Details'])

    fig = go.Figure(data=[go.Table(
        columnwidth = [100, 50, 400],
        header = dict(
            values=list(df.columns),
            font_color='rgb(100,100,100)',
            fill_color='aquamarine',
            align='left'),
        cells = dict(
            values=[df.Initiatives, df.Acronym, df.Details],
            fill_color='white', 
            font_color='rgb(100,100,100)',
            font_size=10,
            align='left',
            height=20)),
    ], layout=go.Layout(margin={'l':0, 'r':0, 't':10, 'b':10}))

    return fig
# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)