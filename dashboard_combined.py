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

# For global initiatives table 
initiatives_file = pd.read_csv('data/esg_initiatives.csv')
# replace NaN for initiatives without acronym
initiatives_file = initiatives_file.replace({np.nan: '-'})
# dictionary: key-initiative spelled out fully, value-[acronym, description]
initiatives_dict = initiatives_file.set_index('Initiative').T.to_dict('list')
# read csv containing all initiatives
all_initiative_array = pd.read_csv('data/all_initiatives.csv', usecols=['Company', 'Type', 'Initiatives', 'Count'])

# For decarbonization percentage
ratings_file = pd.read_csv('data/all_percentile_t8.csv', usecols=['name', 'percent', 'type'])

# For sentiment 
sentiment_file = pd.read_csv('data/sentiment_dummy.csv', usecols=['Company', 'Sentiment', 'type'])

# For bigram
bigram_file = pd.read_csv('data/bigram_df.csv', usecols=['Company', 'BigramArray'])

# For wordcount
word_count_file = pd.read_csv('data/all_word_count_top10.csv', usecols=['name', 'bigram', 'count'])

# Cards --------------------------------------------------------------------------------
card_sentiment = dbc.Card([
    dbc.CardBody([
        html.H5('Overall Sentiment Level', className='text-center'),
        dcc.Graph(id='sentiment_gauge', figure={})
    ])
])

card_percentage = dbc.Card([
    dbc.CardBody([
        html.H5('Percentage of Decarbonization Disclosure', className='text-center'),
        dcc.Graph(id='percentage_barplot', figure={})
    ])
])

card_initiative_count = dbc.Card([
    dbc.CardBody([
        html.H5('Global Standards & Initiatives Count', className='text-center'),
        dcc.Graph(id='initiative_barplot', figure={})
    ])
])

card_initiative_table = dbc.Card([
    dbc.CardBody([
        html.H5('Global Standards & Initiatives', className='text-center'),
        dcc.Graph(id='initiative_table', figure={})
    ])
])

card_word_count = dbc.Card([
    dbc.CardBody([
        html.H5('Top 10 Word Count', className='text-center'),
        dcc.Graph(id='word_count', figure={})
    ])
])

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

# Tabs ------------------------------------------------------------------------------
tab1_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H6('Select Type of Financial Institution'), 
                dcc.Dropdown(id='type_of_fi_dropdown_tab1',
                            options=[
                                {'label': 'Asset Manager (AM)', 'value': 'am'}, 
                                {'label': 'Asian Bank (AB)', 'value': 'ab'}, 
                                {'label': 'Insurance Company (INS)', 'value': 'ins'}, 
                                {'label': 'Pension Fund (PF)', 'value': 'pf'}
                            ],
                            multi=False,
                            value='am',
                            searchable=False)
            ], width={'size':4, 'offset':0, 'order': 1}),
            dbc.Col([
                html.H6('Select a Company'),
                dcc.Dropdown(id='company_dropdown_tab1',
                            multi=False,
                            value='Aegon')
            ], width={'size':4, 'offset':0, 'order':1})
        ]),
        html.Br(),
        dbc.Row([ 
            dbc.Col([card_sentiment], width={'size':4, 'offset':0, 'order':1}),
            dbc.Col([card_percentage], width={'size':4, 'offset':0, 'order':2}),
            dbc.Col([card_initiative_count], width={'size':4, 'offset':0, 'order':3})
        ]),
        html.Br(),
        dbc.Row([ 
            dbc.Col([card_initiative_table], width={'size':7, 'offset':0, 'order':1}),
            dbc.Col([card_word_count], width={'size':5, 'offset':0, 'order':2})
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([html.P('* Average is the mean result of all the companies that belongs \
                            under the same type of financial institution.')
            ], width=12)
        ])
    ]),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody([
        dbc.Row([ 
            dbc.Col([
                html.H6('Select Type of Financial Institution'), 
                dcc.Dropdown(id='type_of_fi_dropdown_tab2',
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
                dcc.Dropdown(id='company_dropdown_tab2',
                            multi=False,
                            value='Aegon')
            ], width={'size':4, 'offset':0, 'order':2}),
            dbc.Col([
                html.H6('Select the Second Company'),
                dcc.Dropdown(id='company_dropdown2_tab2',
                            multi=False,
                            value='BlackRock')
            ], width={'size':4, 'offset':0, 'order':3})
        ]),
        html.Br(),
        dbc.Row([ # Third Row
            dbc.Col([card_percentage_comparison], width={'size':7, 'offset':0, 'order':1}),
            dbc.Col([card_sentiment_comparison], width={'size':5, 'offset':0, 'order':2})
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.H5('Top 10 Occurring Bigrams', className='text-center')
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bigram1', figure={})
            ], width=6),
            dbc.Col([
                dcc.Graph(id='bigram2', figure={})
            ], width=6)
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([html.P('* Average is the mean result of all the companies that belongs \
                            under the same type of financial institution.')
            ], width=12)
        ])
    ]),
    className="mt-3",
)


tabs = dbc.Tabs([
    dbc.Tab(tab1_content, label="Individual Company"),
    dbc.Tab(tab2_content, label="Company Comparison")
])

# Layout -----------------------------------------------------------------------------
# ---------- For Tab 1 ----------
app.layout = dbc.Container([
    html.Br(),
    dbc.Row([ # First Row: Dashboard Header
        dbc.Col(html.H1('Decarbonization Dashboard', className='font-weight-bolder'), width=12)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([tabs])
    ])
], fluid=True)

# Callback ----------------------------------------------------------------------------
# To filter for comapanies according to FI chosen 
@app.callback(
    Output(component_id='company_dropdown_tab1', component_property='options'),
    Input(component_id='type_of_fi_dropdown_tab1', component_property='value')
)
def update_dropdown(type_of_fi):
    sub_df = companylabels_file.loc[companylabels_file['Type'] == type_of_fi]
    options = [{'label': x[0], 'value': x[1]} for x in sub_df.values.tolist()]
    return options

# To update sentiment gauge chart
@app.callback(
    Output(component_id='sentiment_gauge', component_property='figure'),
    Input(component_id='type_of_fi_dropdown_tab1', component_property='value'),
    Input(component_id='company_dropdown_tab1', component_property='value')
)
def update_graph(type_of_fi, company):
    # Extract out dataframe for relevant FI, used for aggregation
    sub_df = sentiment_file.loc[sentiment_file['type'] == type_of_fi]
    count_array = sub_df['Sentiment'].values.tolist()

    sentiment = sentiment_file.set_index('Company').Sentiment.loc[company]
    average = round(sum(count_array) / len(count_array), 1)
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = sentiment, # company's sentiment
        mode = "gauge+number+delta",
        delta = {'reference': average}, # average
        gauge = {'axis': {'range': [None, 5]},
                'bar': {'color': "black"},
                'steps' : [
                    {'range': [0, 1.25], 'color': "#F25757"}, 
                    {'range': [1.25, 2.5], 'color': "#FFC15E"}, 
                    {'range': [2.5, 3.75], 'color': "#F5FF90"}, 
                    {'range': [3.75, 5], 'color': "#58CC00"}], 
                'threshold' : {'line': {'color': "red", 'width': 3.7}, 'thickness': 0.75, 'value': average}}))
    fig.update_layout(height = 200, margin = {'t':10, 'b':0})
    return fig

# To update barplot for percentile rank
@app.callback(
    Output(component_id='percentage_barplot', component_property='figure'),
    Input(component_id='type_of_fi_dropdown_tab1', component_property='value'),
    Input(component_id='company_dropdown_tab1', component_property='value')
)
def update_graph(type_of_fi, company):
    # Extract out dataframe for relevant FI, used for aggregation
    sub_df = ratings_file.loc[ratings_file['type'] == type_of_fi]
    count_array = sub_df['percent'].values.tolist()

    rating = round(ratings_file.set_index('name').percent.loc[company], 2)
    average = round(sum(count_array) / len(count_array), 2)
    fig = go.Figure(go.Bar(
            x=[average, rating],
            y=['Average' + ' (' + fi_dict[type_of_fi] + ')*', company],
            orientation='h',
            marker_color=['#4EADAF', '#88DEB0'],
            text=[average, rating],
            textposition='inside'))
    fig.update_traces(width=0.6)
    fig.update_layout(height = 200 , margin = {'t':10, 'b':0})
    return fig 

# To update barplot for initiative count
@app.callback(
    Output(component_id='initiative_barplot', component_property='figure'),
    Input(component_id='type_of_fi_dropdown_tab1', component_property='value'),
    Input(component_id='company_dropdown_tab1', component_property='value')
)
def update_graph(type_of_fi, company):
    # Extract out dataframe for relevant FI, used for aggregation
    sub_df = all_initiative_array.loc[all_initiative_array['Type'] == type_of_fi]
    count_array = sub_df['Count'].values.tolist()

    company_initiative = all_initiative_array.set_index('Company').Initiatives.loc[company]
    count = len(ast.literal_eval(company_initiative))
    average = round(sum(count_array) / len(count_array))
    fig = go.Figure(go.Bar(
            x=[average, count],
            y=['Average' + ' (' + fi_dict[type_of_fi] + ')*', company],
            orientation='h',
            marker_color=['#4EADAF', '#88DEB0'],
            text=[average, count],
            textposition='inside'))
    fig.update_traces(width=0.6)
    fig.update_layout(height = 200 , margin = {'t':10, 'b':0})
    return fig 

# To update Global Initiatives Table
@app.callback(
    Output(component_id='initiative_table', component_property='figure'),
    Input(component_id='company_dropdown_tab1', component_property='value')
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

# To update word count bar plot
@app.callback(
    Output(component_id='word_count', component_property='figure'),
    Input(component_id='company_dropdown_tab1', component_property='value')
)
def update_graph(company):
    sub_df = word_count_file.loc[word_count_file['name'] == company]
    sorted_df = sub_df.sort_values(by=['count'], ascending=False)
    words = sorted_df['bigram'].tolist()
    counts = sorted_df['count'].tolist()
    counts = [int(x) for x in counts]

    fig = go.Figure(go.Bar(
            x=counts,
            y=words,
            orientation='h',
            marker_color=px.colors.sequential.Tealgrn,
            text=counts,
            textposition='inside'))
    fig.update_layout(height = 450 , margin = {'t':10, 'b':0}, yaxis=dict(autorange="reversed"))
    return fig 

# ---------- For Tab 2 ----------
# To filter for comapanies according to FI chosen in dropdown 1 [Company 1]
@app.callback(
    Output(component_id='company_dropdown_tab2', component_property='options'),
    Input(component_id='type_of_fi_dropdown_tab2', component_property='value')
)
def update_dropdown(type_of_fi):
    sub_df = companylabels_file.loc[companylabels_file['Type'] == type_of_fi]
    options = [{'label': x[0], 'value': x[1]} for x in sub_df.values.tolist()]
    return options

# To filter for comapanies according to FI chosen in dropdown 1 [Company 2]   
@app.callback(
    Output(component_id='company_dropdown2_tab2', component_property='options'),
    Input(component_id='company_dropdown_tab2', component_property='value'),
    Input(component_id='type_of_fi_dropdown_tab2', component_property='value')
)
def update_dropdown(company1, type_of_fi):
    sub_df = companylabels_file.loc[companylabels_file['Type'] == type_of_fi]
    options = [{'label': x[0], 'value': x[1]} for x in sub_df.values.tolist() if x[1] != company1]
    return options

# To update comparison chart of percentage disclosure
@app.callback(
    Output(component_id='percentage_comparison', component_property='figure'),
    Input(component_id='type_of_fi_dropdown_tab2', component_property='value'),
    Input(component_id='company_dropdown_tab2', component_property='value'),
    Input(component_id='company_dropdown2_tab2', component_property='value')
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
        subplot_titles=['Average' + ' (' + fi_dict[type_of_fi] + ')*', company1, company2])
    fig.add_trace(go.Pie(labels=labels, values=[average, 100-average], name="Average", pull=[0.2, 0]), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[percent1, 100-percent1], name=company1, pull=[0.2, 0]), 1, 2)
    fig.add_trace(go.Pie(labels=labels, values=[percent2, 100-percent2], name=company2, pull=[0.2, 0]), 1, 3)

    fig.update_traces(hoverinfo="label+percent+name", marker_colors=['#88DEB0', '#4EADAF'])
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", xanchor="auto"), 
        height = 350, margin = {'t':50, 'b':0})
    fig.update_annotations(font_size=13, font_color='black')
    return fig

# To update barplot for sentiment comparison
@app.callback(
    Output(component_id='sentiment_comparison', component_property='figure'),
    Input(component_id='type_of_fi_dropdown_tab2', component_property='value'),
    Input(component_id='company_dropdown_tab2', component_property='value'),
    Input(component_id='company_dropdown2_tab2', component_property='value')
)
def update_graph(type_of_fi, company1, company2):
    # Extract out dataframe for relevant FI, used for aggregation
    sub_df = sentiment_file.loc[sentiment_file['type'] == type_of_fi]
    sentiment_array = sub_df['Sentiment'].values.tolist()
    average = round(sum(sentiment_array) / len(sentiment_array), 1)

    sentiment1 = sentiment_file.set_index('Company').Sentiment.loc[company1]
    sentiment2 = sentiment_file.set_index('Company').Sentiment.loc[company2]
    
    fig = go.Figure(go.Bar(
            x=[average, sentiment2, sentiment1],
            y=['Average' + ' (' + fi_dict[type_of_fi] + ')*', company2, company1],
            orientation='h',
            marker_color=['#4EADAF', '#69C6AF','#88DEB0'],
            text=[average, sentiment2, sentiment1],
            textposition='inside'))
    fig.update_traces(width=0.6)
    fig.update_layout(height = 350 , margin = {'t':20, 'b':0})
    return fig 

# To update bigram chart 1
@app.callback(
    Output(component_id='bigram1', component_property='figure'),
    Input(component_id='company_dropdown_tab2', component_property='value')
)
def update_graph(company1):
    bigram_dict = bigram_file.set_index('Company').BigramArray.loc[company1]
    bigram_dict = ast.literal_eval(bigram_dict)
    words = [w[0] for w in bigram_dict]
    counts = [w[1] for w in bigram_dict]
    
    fig = go.Figure(go.Bar(
            x=counts,
            y=words,
            orientation='h',
            marker_color=px.colors.sequential.Tealgrn))
    fig.update_layout(height = 450 , margin = {'t':60, 'b':0}, yaxis=dict(autorange="reversed"), 
                    title_text=company1, title_font_size=13, title_x=0.5)
    return fig

# To update bigram chart 2
@app.callback(
    Output(component_id='bigram2', component_property='figure'),
    Input(component_id='company_dropdown2_tab2', component_property='value')
)
def update_graph(company2):
    bigram_dict = bigram_file.set_index('Company').BigramArray.loc[company2]
    bigram_dict = ast.literal_eval(bigram_dict)
    words = [w[0] for w in bigram_dict]
    counts = [w[1] for w in bigram_dict]
    
    fig = go.Figure(go.Bar(
            x=counts,
            y=words,
            orientation='h',
            marker_color=px.colors.sequential.Tealgrn))
    fig.update_layout(height = 450 , margin = {'t':60, 'b':0}, yaxis=dict(autorange="reversed"), 
                    title_text=company2, title_font_size=13, title_x=0.5)
    return fig

# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)