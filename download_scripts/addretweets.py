#!/usr/bin/python

import sys
import json
import twitter
import datetime
import time
import pprint

input_filename = sys.argv[1]

api = twitter.Api(consumer_key = "NNYKKS1PdpSD6a218rvTotvAo",
    consumer_secret = "Z2Q8iFt8nKzXsJGNG1pW6AgBmsPM06db0FCe8c53eQ909CGR8d", 
    access_token_key = "1184909629-czUfqbQOZSZgwp6j2G6nx4HadSRHBmXGRma32ae", 
    access_token_secret = "olru9xkjHWmonuFOVupsoLnq7X0ZpWVnQNWSfjXYnRYqd")

with open(input_filename) as input_file:
    input_data = json.load(input_file)

total_tweets_with_retweets = 0

for tweet in input_data:
    if int(tweet["retweets"]) > 0:
        total_tweets_with_retweets = total_tweets_with_retweets + 1

total_seconds_estimated = total_tweets_with_retweets * 15

print("Current time is " + time.strftime("%l:%M%p %b %-d") + "\n")

current_time_object = datetime.datetime.now()
ending_time_estimate_object = current_time_object + datetime.timedelta(0, total_seconds_estimated)

print("Estimated completion time is " + ending_time_estimate_object.strftime("%l:%M%p %b %-d") + "\n\n")

for index, tweet in enumerate(input_data):
    if int(tweet["retweets"]) > 0:
        while True:
            try:
                # This means we should retrieve the first 100 retweets for this one
                print("Now attempting tweet number " + str(index + 1) + "...")
                retweets = api.GetRetweets(tweet["id"], count = 100, trim_user = False)
                # Convert retweets list of "Status" objects to list of dictionaries
                retweets_dictionaries = []
                for status in retweets:
                    retweets_dictionaries.append({
                        "id" : str(status.id), 
                        "date" : status.created_at, 
                        "text" : status.text, 
                        "username" : status.user.screen_name
                    })
                input_data[index]["retweets_data"] = retweets_dictionaries
                break
            except:
                print("Error encountered, waiting 15 seconds and trying again...")
                time.sleep(15.0)

final_json = json.dumps(input_data, separators=(",",":"))
final_file = open(input_filename[:-5] + "_with_retweets.json", "w")
final_file.write(final_json)
final_file.close()
