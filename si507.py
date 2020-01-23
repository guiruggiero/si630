from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk 
from nltk.corpus import stopwords

## SI 507 - HW5
## Developed by: Gui Ruggiero
## Your section day/time: 3, Wed 10am
## Any names of people you worked with on this assignment: N/A

#Usage: python3 hw5_twitter-edited.py username num_tweets
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

#3#Try to load the cache from file
CACHE_FNAME = 'cache_file_name.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
#I am not considering RTs as real tweets, so include_rts is set to FALSE
params={'screen_name' : username, 'count': num_tweets, 'include_rts' : 'false', 'tweet_mode' : 'extended'}
#print(params)
par = []
for k in sorted(params.keys()):
    par.append("{}-{}".format(k, params[k]))
question = url + "_".join(par)
#print(question)

#Code for Part 3: Caching
def fetch_tweets_using_cache():
    #Look in the cache to see if we already have this data
    if question in CACHE_DICTION:
        print("Fetching cached data...")
        return CACHE_DICTION[question]

    #If not, fetch the data afresh, add it to the cache, then write the cache to file
    else:
        print("Requesting new data...")
        resp = requests.get(url, params, auth=auth)
        CACHE_DICTION[question] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[question]

#Code for Part 1: Get Tweets
def fetch_tweets():
#    return requests.get(url, params, auth=auth).json()
    return fetch_tweets_using_cache()

tweets = fetch_tweets()
#with open('tweet.json', 'w') as outfile:
#    json.dump(tweets.json(), outfile)

#Separating the tweets' contents from all the other data
tweets_content_only = []
for t in tweets:
    #print(t['full_text'])
    tweets_content_only.append(t['full_text'])
#print(tweets_content_only)
#print(len(tweets_content_only))

#COnverting list into string to process with NLTK
tweets_content_only_str = ''.join(str(t) for t in tweets_content_only)
#print(tweets_content_only_str)

#Code for Part 2: Analyze Tweets
tokens = nltk.word_tokenize(tweets_content_only_str)
#print(tokens)
fdist = nltk.FreqDist(tokens)
#print(fdist)

#ignoring...
#...words that do not contain only alphabetic characters [a-zA-Z]
tokens_clean1 = [w for w in tokens if w.isalpha()]
#print(tokens_clean1)

#...words that are in stopwords.words("english") 
stop_words = set(stopwords.words('english'))
tokens_clean2 = [w for w in tokens_clean1 if not w in stop_words]
#print(tokens_clean2)

#...'http', 'https', and 'RT'
twitter_words = ['http', 'https', 'RT']
tokens_clean3 = [w for w in tokens_clean2 if not w in twitter_words]
#print(tokens_clean3)

fdist_clean = nltk.FreqDist(tokens_clean3)
#print(fdist_clean)
print("USER:", username)
print("TWEETS REQUESTED:", num_tweets)
print("TWEETS ANALYZED (excluding RTs):", len(tweets_content_only))
print("5 MOST FREQUENT WORDS:", fdist_clean.most_common(5))

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()