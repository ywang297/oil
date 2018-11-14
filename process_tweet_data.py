# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:02:01 2018

@author: yishu
"""

import pandas as pd
import datetime

tweet = pd.read_csv("table_big_new.csv")
#length: 244700

# extract 'date' from 'time' column
tweet['date'] = tweet['time'].apply(lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d').date())

# get a column of cleaner tweet without http address
# based on the observation that url address (might include hashtags) is always at the end of the text


## the following function decompose tweet text into text part and url address part, and return both
def decompose_text_into_nourl_and_url(text):
    url = "http://"
    pos = text.find(url)
    if pos == -1:
        return text, ''
    else:
        return text[:pos], text[pos:]

tweet['tweet_nourl'] = tweet['tweet'].apply(lambda x: decompose_text_into_nourl_and_url(x)[0])
tweet['tweet_url'] = tweet['tweet'].apply(lambda x: decompose_text_into_nourl_and_url(x)[1]) ## this column just for inspection

tweet_nodup = tweet[~tweet.duplicated(subset=['tweet_nourl', 'time'])]  
# length 16677


from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
sia = SIA()
scores = ['neg', 'neu', 'pos', 'compound']
for score in scores:
    tweet_nodup[score] = tweet_nodup['tweet_nourl'].apply(lambda x: sia.polarity_scores(x)[score])

tweet_nodup.to_csv("tweet_nodup_sentiment_new.csv", index=False)
    
## Next we can aggregate the sentiment scores for each date
sentiment_byday = tweet_nodup.groupby('date')['compound'].mean()    
 
sentiment_byday.to_csv("sentiment_byday_big_new.csv")