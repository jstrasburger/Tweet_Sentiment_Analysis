import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import dash_core_components as dcc
import pandas as pd

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import os
import base64

import boto3
import io

MODEL_BUCKET = 'jbs2-project-model-files'

s3_client = boto3.client("s3", region_name='us-east-1')
obj = s3_client.get_object(Bucket=MODEL_BUCKET, Key='df_build.csv')

df_build = pd.read_csv(io.BytesIO(obj['Body'].read()),encoding='utf8')

df_build_pos = df_build[df_build.target == 1]
df_build_neg = df_build[df_build.target == 0]

text_pos = " ".join(tweet for tweet in df_build_pos.text)
text_neg = " ".join(tweet for tweet in df_build_neg.text)

#print ("There are {} words in the combination of all review.".format(len(text_pos)))
#print ("There are {} words in the combination of all review.".format(len(text_neg)))

stopwords = set(STOPWORDS)
stopwords.update(["quot","u","RT"])

wordcloud_pos = WordCloud(stopwords=stopwords, background_color="white").generate(text_pos)
wordcloud_neg = WordCloud(stopwords=stopwords, background_color="white").generate(text_neg)

# plt.imshow(wordcloud_pos, interpolation='bilinear')
# plt.axis("off")
# plt.show()

# plt.imshow(wordcloud_neg, interpolation='bilinear')
# plt.axis("off")
# plt.show()

word_pos = 'static/img/word_pos.png' # replace with your own image
pos_cloud = base64.b64encode(open(word_pos, 'rb').read())

word_neg = 'static/img/word_neg.png' # replace with your own image
neg_cloud = base64.b64encode(open(word_neg, 'rb').read())


# CM = cv2.imread('static/img/confusion_matrix.png')
# confusion_img = px.imshow(CM)

CM  = 'static/img/confusion_matrix.png' # replace with your own image
confusion_img = base64.b64encode(open(CM, 'rb').read())


colors = {
    'background': '#A9A9A9',
    #'background': '#FFFFFF',
    'text': '#3c4363'
}
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Training Dataset"),
            className="mx-1 my-1")
        ]),
        dbc.Row([
            dbc.Col(html.P("To build our training dataset our Team random sampled the 1.6 million tweets from the data we found on kaggle (https://www.kaggle.com/kazanova/sentiment140). This would greatly reduce the computational requirements and speed up model building. We ended with training data that was perfectly balanced - 5000 negatively marked tweets and corresponding information and 5000 positively marked tweets. For our initial model we dropped all of the columns that were not the target sentiment 1/0 or the actual tweet itself."),
            className="mx-1 my-1")
        ]),    
        dbc.Row([
            dbc.Col([html.Div(children=[html.H2("Positive Training Words"),html.Img(src='data:image/png;base64,{}'.format(pos_cloud.decode()),style={'width': '100%'})])]),
            dbc.Col([html.Div(children=[html.H2("Negative Training Words"),html.Img(src='data:image/png;base64,{}'.format(neg_cloud.decode()),style={'width': '100%'})])])
        ]),
        dbc.Row([
            dbc.Col(html.H2("Model Training"),
            className="mx-1 my-1")
        ]),
        dbc.Row([
            dbc.Col(html.P(" In order to train this model we had to import a variety of popular data science modules for Python. numpy, pandas, several sklearn modules, seaborn for the confusion matrix, support vector classifier, spacy, re, joblib - to save the model, matplotlib, a tweet tokenizer, and spacy-stopwords. After cutting our data into a training and testing set by random sampling for a balanced amount of tweets - we then began putting together the model. We wrote a function that prepares the data, droping columns that are not needed and then setting a target variable (sentiment 1+ or 0-). We then setup the model with sklearns' typical train,test, split arguments and chose to reserve thirty percent of the model for cross validation. We then vectorized the actual tweets which were stored as a single string. After the vectorization was complete we wrote a function to use a linear support vector machine learning algorithm to be trained on our training set of data. We then looked at model accuracy in terms of the cross validation score and its ability to detect sentiment in sample and out of sample. The model appears to be stable at around 70 percent accuracy for detecting binary sentiment.")
            	, className="mx-1 my-1")
        ]),
         dbc.Row([
            dbc.Col(html.H2("Model Improvements"),
            className="mx-1 my-1")
        ]),
        dbc.Row([
        	dbc.Col(html.P("As a part of our continuous model improvement we focused our efforts on applying the correct methodology and tuning hyperparameters to achieve the best results. We utilized the spacy stopwords list and appended to it to include commonly found irrelevant words. This was an interative process and we utilized prediction word counts and word clouds as visualizations to ensure that we were using the right stopwords. Balancing the dataset was also an important part of our data cleaning process. Our team selected the TFIDF vectorizer and passed the argument specifying a tweet tokenizer since our application was using twitter data. It is also notable that we tried increasing the size of the training data up to a certain point. 10,000 observations provides readily available results, however we are confident that with more computing power, further accuracy improvements could be made. For our final model we were able to sucessfully train a model on 100,000 labeled tweets. This further imporved accuracy by about 3%. We adjusted the ngram_range parameter from the default (1,1) to (1,4). We also set Max_features to None, since our inital value of 1000 was great for quick prototyping but dragged performance. We also set strip_accents to unicode for another marginal gain in accuracy. All of these tweaks and changes resulted in a Mean cross-validation accuracy of 79.0% and an overall accuracy of 79.44%. This represents a near 10% improvemnt over our base model."),className="mx-1 my-1")
        ]),
        html.Div(children=[
        html.Div(style={'color': colors['text']}, children=[
            html.H3('Model Confusion Levels'),
            dbc.Col([html.Div([html.Img(src='data:image/png;base64,{}'.format(confusion_img.decode()),style={'width': '60%'})])])]),
		])    
    ])
])
