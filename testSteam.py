import sys
import re
import nltk
from nltk.corpus import stopwords
import pickle
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

data = []

with open('testing.csv', 'r') as training:
	for line in training:
		line = re.split('","', line)
		line[0] = line[0][1:]
		line[1] = line[1][:-2]
		data.append((line[0], line[1]))
	training.close()

random.shuffle(data)
tweets = []

stop_words = set(stopwords.words("english"))
sno = nltk.stem.SnowballStemmer('english')

for (sentiment, tweet) in data:
    #tweet_filtered = [(sno.stem(word.strip(".,\"")).lower()) for word in tweet.split() if ((len(word) >= 3) and (not '@' in word) and (word not in stop_words) and (not '#' in word))]
    tweet_filtered = []
    for word in tweet.split():
		if ((len(word) >= 3) and (not '@' in word) and (word not in stop_words) and (not '#' in word)):
			#print(word)
			word = (word.strip(".,\"")).lower()
			word = sno.stem(word)
			tweet_filtered.append(word)
    tweets.append((tweet_filtered, sentiment))

right = 0
total = 0

for (words, sentiment) in tweets:
    prediction = classifier.classify(extractFeatures(words))
    if prediction == sentiment:
    	right += 1
    total += 1
	
accuracy = 0
if total > 0:
	accuracy = (float(right) / float(total))*100

print("Accuracy: {0}%".format(accuracy))
print("Data:")
print("Training data 10000 records")
print("Testing data 2000 records")