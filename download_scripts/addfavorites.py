#!/usr/bin/python

import sys
import json
import twitter
import datetime
import time
import pprint
import urllib2
import re

input_filename = sys.argv[1]

api = twitter.Api(consumer_key = "NNYKKS1PdpSD6a218rvTotvAo",
    consumer_secret = "Z2Q8iFt8nKzXsJGNG1pW6AgBmsPM06db0FCe8c53eQ909CGR8d", 
    access_token_key = "1184909629-czUfqbQOZSZgwp6j2G6nx4HadSRHBmXGRma32ae", 
    access_token_secret = "olru9xkjHWmonuFOVupsoLnq7X0ZpWVnQNWSfjXYnRYqd", 
    sleep_on_rate_limit = True)

# PROBLEM WITH THIS FUNCTION: it includes @fredhutch in the list returned, so 
# a way to fix this is possibly to just filter out @fredhutch every time

def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urllib2.urlopen('https://twitter.com/i/activity/favorited_popup?id=' + post_id).read()
        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
        unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
        unique_ids.remove("16645335")
        return unique_ids
    except urllib2.HTTPError:
        raise ValueError("Retrieval of favoriting users for tweet \"" + post_id + "\" failed")

with open(input_filename) as input_file:
    input_data = json.load(input_file)

total_tweets_with_favorites = 0

for tweet in input_data:
    if int(tweet["favorites"]) > 0:
        total_tweets_with_favorites = total_tweets_with_favorites + 1

total_seconds_estimated = total_tweets_with_favorites * 15

print("Current time is " + time.strftime("%l:%M%p %b %-d") + "\n")

current_time_object = datetime.datetime.now()
ending_time_estimate_object = current_time_object + datetime.timedelta(0, total_seconds_estimated)

print("Estimated completion time is " + ending_time_estimate_object.strftime("%l:%M%p %b %-d") + "\n\n")

for index, tweet in enumerate(input_data):
    if int(tweet["favorites"]) > 0:
        incrementer = 0
        while True:
            try:
                # This means we should retrieve the first 100 favorites for this one
                print("Now attempting tweet index " + str(index) + "...")
                favoriting_users = get_user_ids_of_post_likes(str(tweet["id"]))
                if int(input_data[index]["favorites"]) != int(len(favoriting_users)):
                    print("Count discrepancy at tweet with ID \"" + str(tweet["id"]) + "\"")
                    input_data[index]["favorites"] = str(api.GetStatus(status_id = int(tweet["id"])).favorite_count)
                input_data[index]["favoriting_users"] = favoriting_users
#                retweets = api.GetRetweets(tweet["id"], count = 100, trim_user = False)
#                # Convert retweets list of "Status" objects to list of dictionaries
#                retweets_dictionaries = []
#                for status in retweets:
#                    retweets_dictionaries.append({
#                        "id" : str(status.id), 
#                        "date" : status.created_at, 
#                        "text" : status.text, 
#                        "username" : status.user.screen_name
#                    })
#                input_data[index]["retweets_data"] = retweets_dictionaries
                break
            except Exception as e:
                print("Error encountered, waiting 15 seconds and trying again...")
                print("Error message: " + str(e))
                incrementer = incrementer + 1
                if incrementer >= 5:
                    print("Tried 5 times, failing and moving on...")
                    break
                time.sleep(15.0)

final_json = json.dumps(input_data, separators=(",",":"))
final_file = open(input_filename[:-5] + "_with_favorites.json", "w")
final_file.write(final_json)
final_file.close()
