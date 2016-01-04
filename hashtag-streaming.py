'''Hashtag Streaming - Twitter Streaming API consumer '''

# Use the following modules to request and handle data from twitter, allowing this to be written to a csv file
import twitter, json, sys, csv

# == OAuth Authentication ==
# The consumer keys can be found at https://dev.twitter.com/apps ("Keys and Access tokens" tab). These should not be made public

consumer_key=""
consumer_secret=""

# Create an access token under the the "Your access token" section and copy the details below. These should not be made public

access_token=""
access_token_secret=""

# Then perform the authentication request using your consumer key and access tokens above to access the streaming API
auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

# open a csv file and write tweets collected to the file, tweet entites collected defined below 
# if you run the same code more than once, change from 'w' (write) to 'a' (append)
csvfile = open('SR15.csv', 'w')
csvwriter = csv.writer(csvfile)

# list column heading names to be included in the csv file, defined later in script
csvwriter.writerow(['created_at',
                    'user-screen_name',
                    'text',
                    'coordinates lng',
                    'coordinates lat',
                    'place',
                    'user-location',
                    'user-geo_enabled',
                    'user-lang',
                    'user-time_zone',
                    'user-statuses_count',
                    'user-followers_count',
                    'user-created_at'
                    ])

# desired keywords to define which tweets to extract from Twiiter streaming API see https://dev.twitter.com/docs/streaming-apis
q = "#SR15, #SpendingReview, #AutumnStatement"
print 'Filtering the public timeline for keyword="%s"' % (q)
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track=q)


# a loop for cleaning data, unpacking dictionaries, encoding text as unicode to handle a wider range of characters

# clean tweet text
def getVal(val):
    clean = ""
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val
    if val:
        clean = val.encode('utf-8') 
    return clean

# clean longitude 
def getLng(val):
    if isinstance(val, dict):
        return val['coordinates'][0]

# clean latitude
def getLat(val):
    if isinstance(val, dict):
        return val['coordinates'][1]

# clean place name
def getPlace(val):
    if isinstance(val, dict):
        return val['full_name'].encode('utf-8')


# main loop to collect tweet entities and define entities written to csv file under headings listed earlier in script
for tweet in stream:
    try:
        csvwriter.writerow([tweet['created_at'],
                            getVal(tweet['user']['screen_name']),
                            getVal(tweet['text']),
                            getLng(tweet['coordinates']),
                            getLat(tweet['coordinates']),
                            getPlace(tweet['place']),
                            getVal(tweet['user']['location']),
                            getVal(tweet['user']['geo_enabled']),
                            getVal(tweet['user']['lang']),
                            getVal(tweet['user']['time_zone']),
                            getVal(tweet['user']['statuses_count']),
                            getVal(tweet['user']['followers_count']),
                            getVal(tweet['user']['created_at'])
                            ])
# display live feed of tweets whilst script is running 
        print getVal(tweet['user']['screen_name']), getVal(tweet['text']), tweet['coordinates'], getPlace(tweet['place'])
    except Exception as e:
        print e

# this script will continue to run through the loops until it is stopped manually
# ctrl-c to stop this script
