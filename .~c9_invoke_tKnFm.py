import sys
import re
import nltk
from nltk.corpus import stopwords
import pickle
import random

def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(word_list):
	word_list = nltk.FreqDist(word_list)
	word_features = word_list.keys()
	return word_features

'''def extract_features(tweet):
	tweet_words = set(tweet)
	features = {}
	for word in word_features:
		features["%s" % word] = (word in tweet_words)
	return features'''

data = []

with open('training.csv', 'r') as training:
	for line in training:
		line = re.split('","', line)
		line[0] = line[0][1:]
		line[1] = line[1][:-2]
		if line[0] == '0':
			line[0] = "negative"
		else:
			line[0] = "positive"
		print((line[0], line[1]))
	training.close()

#print(data[:10])

'''random.shuffle(data)
tweets = []

stop_words = set(stopwords.words("english"))

for (sentiment, tweet) in data:
    tweet_filtered = [(word.strip(".,\"")).lower() for word in tweet.split() if ((len(word) >= 3) and (not '@' in word) and (word not in stop_words) and (not '#' in word))]
    tweets.append((tweet_filtered, sentiment))
    print(sentiment, tweets)'''

'''word_features = get_word_features(get_words_in_tweets(tweets))
f = open('word_features.pickle', 'wb')
pickle.dump(word_features, f)
f.close()

training_set = nltk.classify.apply_features(extract_features, tweets)

classifier = nltk.NaiveBayesClassifier.train(training_set)
f = open('naive_bayes_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

print classifier.show_most_informative_features(32)'''