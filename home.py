import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import numpy as np
import itertools
import collections
import nltk
import spacy
import re

from spacy.lang.en.stop_words import STOP_WORDS

# from application import app

import os
import base64

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



# df = df.rename(columns={"target": "sentiment"})
df.sentiment = df.sentiment.apply(lambda x:'negative' if x == '0' else 'positive')

fig1 = px.histogram(df, x='sentiment',
                    color='sentiment',
                    title='Count of Predicted Tweets',
                    color_discrete_map={'positive':'#95d4e6',
                                        'negative':'#d16d6d'})


### Word Cloud Creation
text = " ".join(review for review in df.text)

#print ("There are {} words in the combination of all review.".format(len(text)))

stopwords = set(STOPWORDS)
stopwords.update(["quot","u","rt","https","one","politics","amp","will"])
wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

twitter_mask = np.array(Image.open("static/img/twit_mask.png"))

wc = WordCloud(background_color="white", max_words=2000, mask=twitter_mask,
               stopwords=stopwords)

# generate word cloud
# wc.generate(text)

# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# # plt.figure()
# plt.show()

# plt.imshow(twitter_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
# plt.show()


#### GRAPH and WORD ANALYSIS

all_tweets = list(df.text)


# Function to remove urls
def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

all_tweets_no_urls = [remove_url(tweet) for tweet in all_tweets]

# all_tweets_no_urls[:2]

# lists containing lowercase words for each tweet
words_in_tweet = [tweet.lower().split() for tweet in all_tweets_no_urls]
# words_in_tweet[:1]

# List of all words across tweets
all_words_no_urls = list(itertools.chain(*words_in_tweet))
# all_words_no_urls[:5]


# Create counter
counts_no_urls = collections.Counter(all_words_no_urls)

tweets_clean = [[word for word in tweet_words if not word in stopwords]
              for tweet_words in words_in_tweet]

all_words_clean = list(itertools.chain(*tweets_clean))
master_counts = collections.Counter(all_words_clean)
# counts_no_urls.most_common(10)

top_words = pd.DataFrame(master_counts.most_common(10), columns=['words', 'count'])
top_words = top_words.sort_values(by='count', ascending=True)


count_bar = px.bar(top_words, x="count", y="words", orientation='h',
             height=400,
             title='Top 10 Word Counts',
             color = 'count',
             color_continuous_scale='Teal')
# count_bar.show()


df2 = df.groupby(by = 'sentiment', as_index = False).size().rename(columns={"size": "count"})

count_pie = px.pie(df2, values='count', names = 'sentiment', title='Count of Each Sentiment as a Percent of All Tweets',
            color='sentiment', height=400,
            color_discrete_map={'positive':'#95d4e6',
                                 'negative':'#d16d6d'})


### Load images

word_home = 'static/img/word_home.png' # replace with your own image
home_img = base64.b64encode(open(word_home, 'rb').read())


layout = html.Div(children=[
    dbc.Container([
        dbc.Row(children=[
            dbc.Col(html.H1("Twitter Sentiment Prediction Dashboard", className="text-center"),
            className="mx-1 my-1")
        ]),
        dbc.Row([
            dbc.Col(html.H5('This application predicts sentiment of tweets', className="text-center"),className="mx-1 my-1") 
        ]),
        dbc.Row([
            dbc.Col(html.P('The dataset represents tweets being pulled directly off Twitter using a Twitter Developer API. All the tweets are in the politics category. The dataset contained two columns of interest: sentiment (denoted by 0 for negative and 1 for positive) and text (containing the content of each tweet).', className="text-justify")) 
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                    id="chr-1",
                    figure=fig1),className="col-6"),
            dbc.Col(children=[dcc.Input(
                    id="input_tweet",
                    placeholder="Input to test your tweet here",
                    type='text',
                    style={'width': '100%'
                            ,'height': '10%'   
                            , 'textAlign': 'center'}),
                    html.Br(),
                    html.P(id="output_sent",style={'color':'navy', 'fontSize': 21}),
            dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(home_img.decode()),style={'width': '100%'})])]),
                        ]
                    )
        ]),  
        dbc.Row([
            dbc.Col(html.H3('Sample Tweets', className="text-center"),
            className="mx-1 my-1")
        ]),
        dbc.Row([
            dbc.Col(children = [
                html.H5('Predicted Positive', className='card-title'),
                html.P(id="opos"),
                dbc.Button("Randomize", id ="bpos", color="secondary", className="mr-1")
                ],
            className="col-6"),
            dbc.Col(children = [
                html.H5('Predicted Negative', className='card-title'),
                html.P(id="oneg"),
                dbc.Button("Randomize", id ="bneg", color="secondary", className="mr-1")
                ],
            className="col-6")
         ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id="chr-2",
                figure=count_bar),className="col-6"),
            dbc.Col(dcc.Graph(
                id="chr-3",
                figure=count_pie),className="col-6")
        ])
    ])
])
