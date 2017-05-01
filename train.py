import sys
import re
import nltk
from nltk.corpus import stopwords
import pickle
import random

def getWords(tweets):
	allWords = []
	for (words, sentiment) in tweets:
		allWords.extend(words)
	return allWords

def getFeatures(words):
	words = nltk.FreqDist(words)
	wordFeatures = words.keys()
	return wordFeatures

def extractDeatures(tweet):
	words = set(tweet)
	features = {}
	for word in wordFeatures:
		features["%s" % word] = (word in words)
	return features

data = []

with open('training.csv', 'r') as training:
	for line in training:
		line = re.split('","', line)
		line[0] = line[0][1:]
		line[1] = line[1][:-2]
		data.append((line[0], line[1]))
	training.close()

random.shuffle(data)
tweets = []

stop_words = set(stopwords.words("english"))

for (sentiment, tweet) in data:
    tweet_filtered = [(word.strip(".,\"")).lower() for word in tweet.split() if ((len(word) >= 3) and (not '@' in word) and (word not in stop_words) and (not '#' in word))]
    tweets.append((tweet_filtered, sentiment))

wordFeatures = getFeatures(getWords(tweets))
f = open('wordFeatures.pickle', 'wb')
pickle.dump(wordFeatures, f)
f.close()

trainingSet = nltk.classify.apply_features(extractDeatures, tweets)
classifier = nltk.NaiveBayesClassifier.train(trainingSet)
f = open('naiveClassifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

print classifier.show_most_informative_features(32)