import requests
import json
import operator
import sys
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

# This function retrieves the last 250 tweets of an account and returns them as one large string
def retrieve_tweets(handle):
print(nltk.__file__)
    # Twitter API credentials
    twitter_consumer_key = 'YOUR_CONSUMER_KEY_HERE'
    twitter_consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
    twitter_access_token = 'YOUR_ACCESS_TOKEN_HERE'
    twitter_access_secret = 'YOUR_ACCESS_SECRET_HERE'
    
    twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)
    
    # Retrieving the last 250 tweets
    tweets = twitter_api.GetUserTimeline(screen_name=handle, count=250, include_rts=False)
    
    # Putting them into one large string
    text = ""
    for t in tweets:
        if t.lang == 'en':
            text += t.text.encode('utf-8')
    
    return text
    
# This function returns Watson PI API result
def analyze(text):
    
    # Watson PI API credentials
    watson_username = 'YOUR_WATSON_PI_USERNAME_HERE'
    watson_password = 'YOUR_WATSON_PI_PASSWORD_HERE'
    
    watson_result = PersonalityInsights(username=watson_username, password=watson_password).profile(text)
    
    return watson_result
    
# This function parses the result from Watson PI API
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
    
handle = "@jack"
tweets = retrieve_tweets(handle)
results = analyze(tweets)
parsed_results = parse(results)

print "\n%s's personality insights\n" % handle
for key, value in parsed_results.items():
    print '%-22s  %.2f' % (key, value)
Contact GitHub API Training Shop Blog About
© 2017 GitHub, Inc. Terms Privacy Security Status Help