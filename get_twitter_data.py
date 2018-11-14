# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:48:09 2018

@author: yishu
"""

import got3 as got
import pandas as pd
from tqdm import tqdm
from datetime import timedelta, date


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield (date1 + timedelta(n), date1 + timedelta(n+1))

start_dt = date(2015, 12, 15)
end_dt = date(2018, 11, 13)
table_list = []
for dt in tqdm(daterange(start_dt, end_dt)):
    #print(dt[0].strftime("%Y-%m-%d")+' '+dt[1].strftime("%Y-%m-%d")) 
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch("oil price opec").setSince(dt[0].strftime("%Y-%m-%d")).setUntil(dt[1].strftime("%Y-%m-%d")).setLang('en').setMaxTweets(300)
    tweet_list = got.manager.TweetManager.getTweets(tweetCriteria)
    tweet_text = [tweet.text for tweet in tweet_list]
    tweet_time = [tweet.date for tweet in tweet_list]
    table_list.append(pd.DataFrame({'tweet':tweet_text, 'time':tweet_time}))

table = pd.concat(table_list)
table.to_csv("table_big_new.csv", index=False)