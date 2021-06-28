import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import seaborn as sns
from sklearn.svm import LinearSVC
from sklearn import metrics
import spacy
import re
import pickle
from spacy.lang.en.stop_words import STOP_WORDS
import matplotlib.pyplot as plt

from nltk.tokenize import TweetTokenizer
tweet_tokenizer = TweetTokenizer()

import boto3
import io




MODEL_BUCKET = 'jbs2-project-model-files'

s3_client = boto3.client("s3", region_name="us-east-1")
obj = s3_client.get_object(Bucket=MODEL_BUCKET, Key='df_build.csv')

# resp_model = s3_client.get_object(Bucket=MODEL_BUCKET, Key='model_file.pkl')
# body_model = resp_model['Body'].read()
# model_file = pickle.loads(body_model)

with open('model_file.pkl', 'wb') as f:
    s3_client.download_fileobj(MODEL_BUCKET, 'model_file.pkl', f)

model_file = 'model_file.pkl'

with open('vect_file.pkl', 'wb') as f:
    s3_client.download_fileobj(MODEL_BUCKET, 'vect_file.pkl', f)

vect_file = 'vect_file.pkl'

# resp_vect = s3_client.get_object(Bucket=MODEL_BUCKET, Key='vect_file.pkl')
# body_vect = resp_vect['Body'].read()
# vect_file = pickle.loads(body_vect)


TWITTER_TRAIN_CSV = pd.read_csv(io.BytesIO(obj['Body'].read()),encoding='utf8')




def prepare_data(csv_file):
	df = pd.read_csv(csv_file)
	# df = df.drop(columns=['id','date','flag','user'])
	df.target = df.target.replace(to_replace=4,value=1)
	X = df.loc[:,['text']]
	y = df.target
	return X, y

def setup_model():
	X, y = prepare_data(TWITTER_TRAIN_CSV)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)
	X_train_docs = [doc for doc in X_train.text]
	return X_train_docs, X_train, X_test, y_train, y_test 

# not using lemmatization because you are using tweet tokenizer
# this function will be not be used or called
def custom_tokenizer(document):
	en_nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
	pattern = re.compile('(?u)\\b\\w\\w+\\b')
	doc_spacy = en_nlp(document)
	lemmas = [token.lemma_ for token in doc_spacy]
	return [token for token in lemmas if token not in STOP_WORDS and pattern.match(token)]

def vectorize():
	X_train_docs, X_train, X_test, y_train, y_test = setup_model()
	# tweet tokenizer
	vect = TfidfVectorizer(tokenizer = tweet_tokenizer.tokenize
							, ngram_range = (1, 4)
							, max_features = None
							, strip_accents = 'unicode'
							).fit(X_train_docs)
	X_train_features = vect.transform(X_train_docs)
	feature_names = vect.get_feature_names()
	# added 3 lines to print how your features look like
	print("Number of features: {}".format(len(feature_names)))
	print("First 100 features:\n{}".format(feature_names[:100]))
	print("Every 100th feature:\n{}".format(feature_names[::100]))
	# pass vect -to validate your model using holdout set
	return vect, X_train_features, X_train, X_test, y_train, y_test


def train_model():
	s3_client = boto3.client("s3")
	# changed this line to match vectorize() return 
	vect, X_train_features, X_train, X_test, y_train, y_test = vectorize()	
	lin_svc = LinearSVC(max_iter=120000)
	scores = cross_val_score(lin_svc, X_train_features, y_train, cv=5) 
	# added 1 line to print cross validation accuracy
	print("Mean cross-validation accuracy: {:.2f}".format(np.mean(scores)))
	#print mean scores for cross-val 
	lin_svc.fit(X_train_features, y_train)

	X_test_docs = [doc for doc in X_test.text]
	X_test_features = vect.transform(X_test_docs)
	y_test_pred = lin_svc.predict(X_test_features)
	print(metrics.accuracy_score(y_test, y_test_pred))

	cf_matrix = confusion_matrix(y_test, y_test_pred)

	#labels = ['True Neg','False Pos','False Neg','True Pos']
	#labels = np.asarray(labels).reshape(2,2)
	#sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues')

	group_names = ['True Neg','False Pos','False Neg','True Pos']
	group_counts = ["{0:0.0f}".format(value) for value in cf_matrix.flatten()]
	group_percentages = ["{0:.2%}".format(value) for value in cf_matrix.flatten()/np.sum(cf_matrix)]
	labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
	labels = np.asarray(labels).reshape(2,2)
	sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues')
	#plt.show()

	plt.savefig('static/img/confusion_matrix.png')

	
	with open(model_file, 'ab') as f:
		pickle.dump(lin_svc, f)
	
	# you need to save your vectorizer in order to transform your unlabeled documents 
	
	with open(vect_file, 'ab') as f:
		pickle.dump(vect, f)


	with open(model_file, 'rb') as data:
		s3_client.upload_fileobj(data, MODEL_BUCKET, model_file) 

	with open(vect_file, 'rb') as data:
		s3_client.upload_fileobj(data, MODEL_BUCKET, vect_file)

	print("completed uploading model and vectorizer to S3")

def apply_label(test_csv):	
	X, y = prepare_data(test_csv)

	with open(model_file, 'rb') as f1:
		lin_svc = pickle.load(f1)

	with open(vect_file, 'rb') as f2:
		vect = pickle.load(f2)
		
	X_test_docs = [doc for doc in X.text]
	X_test_features = vect.transform(X_test_docs)
	y_test_pred = lin_svc.predict(X_test_features)

	X['target']= y_test_pred
	X.to_csv('predicted.csv')
	#save X csv file instead of returning X 

def apply_text(text):

	with open('model_file.pkl', 'rb') as f3:
		lin_svc = pickle.load(f3)

	with open('vect_file.pkl', 'rb') as f4:
		vect = pickle.load(f4)


	tweet = {'text':text}
	df_tweet = pd.DataFrame(tweet)

	tweet_docs = [doc for doc in df_tweet.text]
	tweet_feat = vect.transform(tweet_docs)

	tweet_pred = lin_svc.predict(tweet_feat)
	if tweet_pred[0] == 1: value = "POSITIVE"
	else: value = "NEGATIVE"
	return value




# uncomment this line when you want to train the model 
# train_model()

# uncomment this line when you want to apply the model 
# apply_label('df_new.csv')

#comment out both lines after running 

