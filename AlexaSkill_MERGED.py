" "'''
Created on 06.05.2017

@author: phil
'''

from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import operator
from afinn import Afinn
#import unidecode

app = Flask(__name__)
ask = Ask(app, "/worldnews")

# Sentiment Analysis with AFINN
afinn = Afinn()

# NYT functions
def get_headlinesHome():
    sess = requests.Session()
    url = "http://api.nytimes.com/svc/topstories/v2/home.json?api-key=3b9ad549cdbe4d2b9e8d14a03d67ef3e"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['results']
    
    for listing in result:
        titles.append( listing['title'] )
        titles.append( "next headline" )
        
    return titles[:9]


def get_headlinesSports():
    sess = requests.Session()
    url = "http://api.nytimes.com/svc/topstories/v2/sports.json?api-key=3b9ad549cdbe4d2b9e8d14a03d67ef3e"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['results']
    
    for listing in result:
        titles.append( listing['title'] )     
        titles.append( "next headline" )
    return titles[:9]


def get_headlinesPolitics():
    sess = requests.Session()
    url = "http://api.nytimes.com/svc/topstories/v2/politics.json?api-key=3b9ad549cdbe4d2b9e8d14a03d67ef3e"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['results']
    
    for listing in result:
        titles.append( listing['title'] )
        titles.append( "next headline" )
    return titles[:9]


def get_headlinesTechnology():
    sess = requests.Session()
    url = "http://api.nytimes.com/svc/topstories/v2/technology.json?api-key=3b9ad549cdbe4d2b9e8d14a03d67ef3e"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['results']
    
    for listing in result:
        titles.append( listing['title'] )
        titles.append( "next headline" )
    return titles[:9]


# TOI functions
def get_headlinesTop():
    sess = requests.Session()
    url = "https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=3534992ea6b64a28866c01fcc2cfba24"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['articles']
    
#    for listing in result:
    for listing in result:
        titles.append( listing['title'] )
        titles = [w.replace(' - Times of India', '') for w in titles]
        titles.append( "  ... next headline ... " )   
    return titles[:9]

def get_headlinesLatest():
    sess = requests.Session()
    url = "https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=latest&apiKey=3534992ea6b64a28866c01fcc2cfba24"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['articles']
    
    for listing in result:
        titles.append( listing['title'] )
        titles = [w.replace(' - Times of India', '') for w in titles]
        titles.append( " next headline  ... " )   
    #return titles  
    return titles[:9]  


# Sentiment NYT
def get_negativeSentimentNYT():
    sess = requests.Session()
    url = "http://api.nytimes.com/svc/topstories/v2/home.json?api-key=3b9ad549cdbe4d2b9e8d14a03d67ef3e"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['results']
    
    for listing in result:
        titles.append( listing['title'] )
    
    afinn_scores = [afinn.score(text) for text in titles]
    headline_sentiment = dict(zip(titles, afinn_scores))
    sorted_x = sorted(headline_sentiment.items(), key=operator.itemgetter(1))

    return sorted_x[:3]

def get_positiveSentimentNYT():
    sess = requests.Session()
    url = "http://api.nytimes.com/svc/topstories/v2/home.json?api-key=3b9ad549cdbe4d2b9e8d14a03d67ef3e"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['results']
    
    for listing in result:
        titles.append( listing['title'] )
    
    afinn_scores = [afinn.score(text) for text in titles]
    headline_sentiment = dict(zip(titles, afinn_scores))
    sorted_x = sorted(headline_sentiment.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_x[:3]

# Sentiment TOI
def get_negativeSentimentTOI():
    sess = requests.Session()
    url = "https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=latest&apiKey=3534992ea6b64a28866c01fcc2cfba24"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['articles']
    
    for listing in result:
        titles.append( listing['title'] )
        titles = [w.replace(' - Times of India', '') for w in titles]
    
    afinn_scores = [afinn.score(text) for text in titles]
    headline_sentiment = dict(zip(titles, afinn_scores))
    sorted_x = sorted(headline_sentiment.items(), key=operator.itemgetter(1))

    return sorted_x[:3]

def get_positiveSentimentTOI():
    sess = requests.Session()
    url = "https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=latest&apiKey=3534992ea6b64a28866c01fcc2cfba24"
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    result = data['articles']
    
    for listing in result:
        titles.append( listing['title'] )
        titles = [w.replace(' - Times of India', '') for w in titles]
    
    afinn_scores = [afinn.score(text) for text in titles]
    headline_sentiment = dict(zip(titles, afinn_scores))
    sorted_x = sorted(headline_sentiment.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_x[:3]


## Welcome message.
@app.route('/')
def homepage():
    return "Welcome Sir!"


## Launch the skill in Alexa.
@ask.launch
def start_skill():
    welcome_message = "Which news source would you like to hear? We've got the New York Times or the Times of India?"
    return question(welcome_message)


## Initiate source.
@ask.intent("YesIntentNYT")
def start_NYT():
    welcome_NYT = "New York ... concrete jungle where dreams are made of. Would you like to hear the happiest articles... the most awful ones... or news from the following categories... Top News...Sports...Technology...and Politics."
    return question(welcome_NYT)

@ask.intent("YesIntentTOI")
def start_TOI():
    welcome_TOI = "India ... homeland of gracious Pranav. Would you like to hear the happiest articles... the most awful ones... or news from the following categories... Top News...Latest News?"    
    return question(welcome_TOI)


## NYT source
@ask.intent("YesIntentHome")
def share_headlines():
    headlines = get_headlinesHome()
    headline_msg = 'Alright Sir, I am so glad to announce you the following top headlines {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("YesIntentSports")
def share_headlines():
    headlines = get_headlinesSports()
    headline_msg = 'Alright Sir, I am so glad to announce you the following top headlines for sports {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("YesIntentPolitics")
def share_headlines():
    headlines = get_headlinesPolitics()
    headline_msg = 'Alright Sir, I am so glad to announce you the following top headlines for politics {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("YesIntentTechnology")
def share_headlines():
    headlines = get_headlinesTechnology()
    headline_msg = 'Alright Sir, I am so glad to announce you the following top headlines for technology{}'.format(headlines)
    return statement(headline_msg)


## TOI source.
@ask.intent("YesIntentTop")
def share_headlines():
    headlines = get_headlinesTop()
    headline_msg = 'Alright Sir, I am so glad to announce you the following top headlines {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("YesIntentLatest")
def share_headlines():
    headlines = get_headlinesLatest()
    headline_msg = 'Alright Sir, I am so glad to announce you the following latest headlines {}'.format(headlines)
    return statement(headline_msg)

## NYT sentiment
@ask.intent("YesIntentNYTSentimentPositive")
def share_headlines():
        headlines = get_positiveSentimentNYT()
        headline_msg = 'Alright Sir, I am so glad to announce you the following top three happiest articles {}'.format(headlines)
        return statement(headline_msg)

@ask.intent("YesIntentNYTSentimentNegative")
def share_headlines():
        headlines = get_negativeSentimentNYT()
        headline_msg = 'Alright Sir, I am so sad to announce you the following top three most awful articles {}'.format(headlines)
        return statement(headline_msg)


## TOI sentiment
@ask.intent("YesIntentTOISentimentPositive")
def share_headlines():
        headlines = get_positiveSentimentTOI()
        headline_msg = 'Alright Sir, I am so glad to announce you the following top three happiest articles {}'.format(headlines)
        return statement(headline_msg)

@ask.intent("YesIntentTOISentimentNegative")
def share_headlines():
        headlines = get_negativeSentimentTOI()
        headline_msg = 'Alright Sir, I am so sad to announce you the following top three most awful articles {}'.format(headlines)
        return statement(headline_msg)

## No intent
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Why the hell did you asked me than?'
    return statement(bye_text)

## Print results

b = get_negativeSentimentTOI()
print(b)


# TOI
x = get_headlinesTop()
print(x)
y = get_headlinesLatest()
print(y)
    
# NYT
x = get_headlinesHome()
print(x)   
y = get_headlinesSports()
print(y)    
z = get_headlinesTechnology()
print(z)    
aa = get_headlinesPolitics()
print(aa)
    
if __name__ == '__main__':
    app.run(debug=True)
