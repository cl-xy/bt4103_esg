import ast
import random
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px  
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# To map type of FI to its abbrievation
fi_dict = {'ab': 'AB', 'am': 'AM', 'ins': 'INS', 'pf': 'PF'}

# For decarbonization rating
ratings_file = pd.read_csv('data/all_percentile.csv', usecols=['name', 'percent', 'type'])

# For sentiment 
sentiment_file = pd.read_csv('data/sentiment_dummy.csv', usecols=['Company', 'Sentiment', 'type'])

# Cards --------------------------------------------------------------------------------
card_percentage_comparison = dbc.Card([
    dbc.CardBody([
        html.H5('Percentage of Decarbonization Disclosure', className='text-center'),
        dcc.Graph(id='percentage_comparison', figure={})
    ])
])

card_sentiment_comparison = dbc.Card([
    dbc.CardBody([
        html.H5('Overall Sentiment Level', className='text-center'),
        dcc.Graph(id='sentiment_comparison', figure={})
    ])
])
# Layout -----------------------------------------------------------------------------
app.layout = dbc.Container([
    dbc.Row([ # First Row: Dashboard Header
        dbc.Col(html.H1('Decarbonization Dashboard',
                        className='mb-4'),
                width=12)
    ]),
    dbc.Row([ # Second Row: 2 Dropdowns for the dashboard
        dbc.Col([
            html.H6('Select Type of Financial Institution'), 
            dcc.Dropdown(id='type_of_fi_dropdown',
                        options=[
                            {'label': 'Asset Manager (AM)', 'value': 'am'}, 
                            {'label': 'Asian Bank (AB)', 'value': 'ab'}, 
                            {'label': 'Insurance Company (INS)', 'value': 'ins'}, 
                            {'label': 'Pension Fund (PF)', 'value': 'pf'}
                        ],
                        multi=False,
                        value='am',
                        searchable=False)
        ], width={'size':4, 'offset':0, 'order':1}),
        dbc.Col([
            html.H6('Select the First Company'),
            dcc.Dropdown(id='company_dropdown',
                        multi=False,
                        value='Aegon')
        ], width={'size':4, 'offset':0, 'order':2}),
        dbc.Col([
            html.H6('Select the Second Company'),
            dcc.Dropdown(id='company_dropdown2',
                        multi=False,
                        value='BlackRock')
        ], width={'size':4, 'offset':0, 'order':3})
    ]),
    html.Br(),
    dbc.Row([ # Third Row
        dbc.Col([card_percentage_comparison], width={'size':7, 'offset':0, 'order':1}),
        dbc.Col([card_sentiment_comparison], width={'size':5, 'offset':0, 'order':2})
    ])
], fluid=True)

# Callback ----------------------------------------------------------------------------
# To filter for comapanies according to FI chosen in dropdown 1 [Company 1]
@app.callback(
    Output(component_id='company_dropdown', component_property='options'),
    Input(component_id='type_of_fi_dropdown', component_property='value')
)
def update_dropdown(type_of_fi):
    sub_df = companylabels_file.loc[companylabels_file['Type'] == type_of_fi]
    options = [{'label': x[0], 'value': x[1]} for x in sub_df.values.tolist()]
    return options

# To filter for comapanies according to FI chosen in dropdown 1 [Company 2]   
@app.callback(
    Output(component_id='company_dropdown2', component_property='options'),
    Input(component_id='company_dropdown', component_property='value'),
    Input(component_id='type_of_fi_dropdown', component_property='value')
)
def update_dropdown(company1, type_of_fi):
    sub_df = companylabels_file.loc[companylabels_file['Type'] == type_of_fi]
    options = [{'label': x[0], 'value': x[1]} for x in sub_df.values.tolist() if x[1] != company1]
    return options

# To update comparison chart of percentage disclosure
@app.callback(
    Output(component_id='percentage_comparison', component_property='figure'),
    Input(component_id='type_of_fi_dropdown', component_property='value'),
    Input(component_id='company_dropdown', component_property='value'),
    Input(component_id='company_dropdown2', component_property='value')
)
def update_graph(type_of_fi, company1, company2):
    # Extract out dataframe for relevant FI, used for aggregation
    sub_df = ratings_file.loc[ratings_file['type'] == type_of_fi]
    percent_array = sub_df['percent'].values.tolist()
    average = round(sum(percent_array) / len(percent_array), 2)

    percent1 = round(ratings_file.set_index('name').percent.loc[company1], 2)
    percent2 = round(ratings_file.set_index('name').percent.loc[company2], 2)

    labels = ["Decarbonization Related", "Decarbonization Unrelated"]
    fig = make_subplots(rows=1, cols=3, 
        specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]], 
        subplot_titles=['Average' + ' (' + fi_dict[type_of_fi] + ')', company1, company2])
    fig.add_trace(go.Pie(labels=labels, values=[average, 100-average], name="Average", pull=[0.2, 0]), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[percent1, 100-percent1], name=company1, pull=[0.2, 0]), 1, 2)
    fig.add_trace(go.Pie(labels=labels, values=[percent2, 100-percent2], name=company2, pull=[0.2, 0]), 1, 3)

    fig.update_traces(hoverinfo="label+percent+name", marker_colors=['#88DEB0', '#4EADAF'])
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="auto"), 
        height = 350, margin = {'t':10, 'b':0})
    fig.update_annotations(font_size=13, font_color='black')
    return fig

# To update barplot for sentiment comparison
@app.callback(
    Output(component_id='sentiment_comparison', component_property='figure'),
    Input(component_id='type_of_fi_dropdown', component_property='value'),
    Input(component_id='company_dropdown', component_property='value'),
    Input(component_id='company_dropdown2', component_property='value')
)
def update_graph(type_of_fi, company1, company2):
    # Extract out dataframe for relevant FI, used for aggregation
    sub_df = sentiment_file.loc[sentiment_file['type'] == type_of_fi]
    sentiment_array = sub_df['Sentiment'].values.tolist()
    average = round(sum(sentiment_array) / len(sentiment_array), 1)

    sentiment1 = sentiment_file.set_index('Company').Sentiment.loc[company1]
    sentiment2 = sentiment_file.set_index('Company').Sentiment.loc[company2]
    
    fig = go.Figure(go.Bar(
            x=[average, sentiment1, sentiment2],
            y=['Average' + ' (' + fi_dict[type_of_fi] + ')', company1, company2],
            orientation='h',
            marker_color=['#88DEB0', '#69C6AF', '#4EADAF'],
            text=[average, sentiment1, sentiment2],
            textposition='inside'))
    fig.update_traces(width=0.6)
    fig.update_layout(height = 350 , margin = {'t':20, 'b':0})
    return fig 
# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)