#!/usr/bin/python

import sys
import json

input_user_database_filename = sys.argv[1]
input_user_timeline_filename = sys.argv[2]

with open(input_user_database_filename) as input_user_database_file:
    input_user_database = json.load(input_user_database_file)

with open(input_user_timeline_filename) as input_user_timeline_file:
    input_user_timeline = json.load(input_user_timeline_file)

# Loop through each user in the database, and for each user loop through the 
# tweets database to aggregate the number of times the specific user:
#     - Retweeted an @fredhutch tweet
#     - Favorited an @fredhutch tweet
#     - Was mentioned in an @fredhutch tweet

for i, user in enumerate(input_user_database):
    if i % 30 == 0:
        print(str(float(float(i) / float(len(input_user_database))) * 100.0)[:3] + "% done...")
    mentions_count = 0
    retweets_count = 0
    favorites_count = 0
    for tweet in input_user_timeline:
        # First add mentions from current tweet
        mentions = tweet["mentions"].split(" ")
        for k, screenname in enumerate(mentions):
            mentions[k] = str(mentions[k][1:]).lower()
        if str(user["screen_name"]).lower() in mentions:
            mentions_count = mentions_count + 1
        # Now add retweets from current tweet
        if "retweets_data" in tweet:
            for retweeter in tweet["retweets_data"]:
                if retweeter["username"].lower() == user["screen_name"].lower():
                    retweets_count = retweets_count + 1
        # Now add favorites from current tweet
        if "favoriting_users" in tweet:
            for favoriting_user in tweet["favoriting_users"]:
                if str(favoriting_user) == str(user["id"]):
                    favorites_count = favorites_count + 1
    # Now add this data to the user database
    input_user_database[i]["interactions_mentions_count"] = mentions_count
    input_user_database[i]["interactions_retweets_count"] = retweets_count
    input_user_database[i]["interactions_favorites_count"] = favorites_count

# Save the user database

user_database_json_string = json.dumps(input_user_database, separators=(',',':'))
user_database_file = open(input_user_database_filename[:-5] + "_with_interactions.json", "w")
user_database_file.write(user_database_json_string)
user_database_file.close()
