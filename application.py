
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import home
import navigation
import model
import team
from  sentiment_predictor import apply_text
import pickle

import boto3

dbclient = boto3.client("dynamodb", region_name="us-east-1")

resp = dbclient.scan(TableName="twitter-tweets")

id = pd.Series()
created = pd.Series()
author_id = pd.Series()
text = pd.Series()
sentiment = pd.Series()

for post in resp["Items"]:
	id = id.append(pd.Series((post['id']['S'])))
	created = created.append(pd.Series((post['created']['S'])))
	author_id = author_id.append(pd.Series((post['author_id']['S'])))
	text = text.append(pd.Series((post['text']['S'])))
	sentiment = sentiment.append(pd.Series((post['sentiment']['S'])))
	
df = pd.concat([id,created,author_id,text,sentiment], axis=1)
df.columns = ['id','created','author_id','text','sentiment']


prediction_results = df



app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[

        # The following 4 tags are for Linkdin preview

        {
            'property': 'og:title',
            'content': 'TweetyHunter.ai'
        },

        {
            'name': 'image',
            'property': 'og:image',
            'content': 'https://www.nolaanalytics.com/static/img/word_home.png'
        },

        {
            'property': 'og:description',
            'content': 'TweetyHunter is an application that scrapes twitter using the twitter api and can make sentiment predictions in real time.'
        },

        {
            'property': 'og:url',
            'content': 'https://www.nolaanalytics.com'
        },

        # A tag that tells Internet Explorer (IE)
        # to use the latest renderer version available
        # to that browser (e.g. Edge)
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
        # A tag that tells the browser not to scale
        # desktop widths to fit mobile screens.
        # Sets the width of the viewport (browser)
        # to the width of the device, and the zoom level
        # (initial scale) to 1.
        #
        # Necessary for "true" mobile support.
        {
          'name': 'viewport',
          'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)

application = app.server


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)


app.layout = html.Div([
    dcc.Location(id='url'),
    navigation.navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/model':
        return model.layout
    elif pathname == '/team':
        return team.layout
    else:
        return home.layout

@app.callback(Output("output_sent", "children"), [Input("input_tweet", "value")])
def output_text(value):
    value = apply_text(eval('["'+ value +'"]'))
    print(value)
    return value

@app.callback(Output("opos", "children"), [Input("bpos", "n_clicks")])
def output_pos(ex1):
    pos_data = prediction_results.text[prediction_results.sentiment == '1']
    ex1 = pos_data.sample(n=1)
    ex1 = ex1.reset_index().drop(columns=['index'])
    ex1 = ex1.text[0]
    return ex1

@app.callback(Output("oneg", "children"), [Input("bneg", "n_clicks")])
def output_neg(ex2):
    neg_data = prediction_results.text[prediction_results.sentiment == '0']
    ex2 = neg_data.sample(n=1)
    ex2 = ex2.reset_index().drop(columns=['index'])
    ex2 = ex2.text[0]
    return ex2



if __name__ == '__main__':
    application.run(debug=True, port=8000)




