import requests
import json
import operator
import sys
import twitter
import pickle
import matplotlib
import numpy

matplotlib.use('Agg')
import matplotlib.pyplot as plt # Do not do this prior to calling use()

from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

twitter_consumer_key = "hovMS6BEaHjfgqKS551sBMsJP"
twitter_consumer_secret = "ruue4Ummrs5a2m9GXZcdChJntlpeeoArHMkQ2AXjFR6QGcTrLh"
twitter_access_token = "200271259-KVIcKdpSXZVc4OTKZBc4tFmZ4aIptNQE0jthaZZv"
twitter_access_secret = "DLjLcKRXVUy3uUR6rdfYIRMZGJAl7JU0xMsASE59ncRUl"


def extractFeatures(tweet):
	words = set(tweet)
	features = {}
	for word in wordFeatures:
		features[word] = (word in words)
	return features

f = open('wordFeatures.pickle', 'rb')
wordFeatures = pickle.load(f)
f.close()

f = open('naiveClassifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()


def obtainTuits(user):
    
    text = ""
    positive, negative = 0,0 
    
    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token,
    access_token_secret=twitter_access_secret)
        
    tuits = twitter_api.GetUserTimeline(screen_name=user, count=50, include_rts=False)
    
    for s in tuits:
        tweet = s.text
        text += tweet.encode('utf-8')
        prediction = classifier.classify(extractFeatures(tweet.split()))
        if prediction == 'positive':
            positive += 1
        elif prediction == 'negative':
            negative += 1 
        print(prediction, tweet)
        print("--------------------------------")
    return text, positive, negative 
    
def analyzeUser(text):
    
    watson_username = 'ea3c98f7-26b9-47ae-89d6-e635b5e43515'
    watson_password = '87VkD8C1Zzdh'
    
    watson_result = PersonalityInsights(username=watson_username, password=watson_password).profile(text)
    return watson_result
    
def parse(json):
    data = {}
    for c in json['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if c4['category'] == 'personality':
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if c3['category'] == 'personality':
                                            data[c3['id']] = c3['personality']
    return data
    
    
def pieChart(pos, neg):
    labels = 'Positive', 'Negative'
    sizes = [pos, neg]
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    fig1.savefig('pieCharPosNeg.png') # Any filename will do
    
def barChart(data):
    objects = data.keys()
    y_pos = numpy.arange(len(objects))
    performance = data.values()
    
    fig = plt.figure()
    
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    
    fig.autofmt_xdate()
    
    plt.savefig("barChartPersonality.png")

text = obtainTuits('@depressed_cat')

pos , neg = text[1], text[2]

pieChart(pos, neg)

text = text[0]

personality = analyzeUser(text)

parsed_results = parse(personality)

personalityItems = ['Excitement-seeking', 'Anxiety', 'Emotionality', 'Friendliness', 'Depression', 'Anger', 'Cheerfulness']
perValues = {}
for key, value in parsed_results.items():
    if key in personalityItems:
        perValues[key] = value
        print '%-22s  %.2f' % (key, value*100)
    
barChart(perValues)