#!/usr/bin/python

import __future__
import sys
import json
import twitter
import datetime
import time

# This script takes a JSON tweet info file like the ones in ./jsondata and 
# fills a separate JSON file with the user information from that database. The 
# purpose of having a separate JSON file that's just user information is to 
# prevent needlessly redownloading and "copy-pasting" user information into 
# the tweet databases we have, instead creating a "master user database" that 
# can be grabbed from to fill the other database with information. 
# 
# This script will go through each tweet (and retweet if available), checking 
# if the user who created the tweet or retweet is already in the user 
# database; if they aren't then add them to the database will all available 
# information. 
# 
# After this user database is filled we could possibly create CSV files that 
# can contain user location and other information, allowing a greater degree 
# of data analysis than before.

input_user_list_filename = sys.argv[1]
input_user_database_filename = sys.argv[2]

with open(input_user_list_filename) as input_user_list_file:
    input_user_list_data = json.load(input_user_list_file)

user_database = []

api = twitter.Api(consumer_key = "f6A1A608PQldoOdpkpd79gZ1Q",
    consumer_secret = "jqOoY4wjKgrLdj7LzSFNi0lBe6vZwRJW0uUrtbhJwNjo0qlJiG", 
    access_token_key = "898010337089265664-UiiDbwZ4meFJc0GMsgampuLJMUwgcgg", 
    access_token_secret = "qnXC6axFM18NQ2yWouTdpoJdkCk8okI9urmNjUAGa8zKo",
    sleep_on_rate_limit = True)

for username in input_user_list_data:
    print(username)
    for i in xrange(900):
        try:
            # Add new user to database
            new_user_twitter_object = api.GetUser(screen_name = username)
            new_user_object = {}
            new_user_object["created_at"] = new_user_twitter_object.created_at
            new_user_object["description"] = new_user_twitter_object.description
            new_user_object["favourites_count"] = new_user_twitter_object.favourites_count
            new_user_object["followers_count"] = new_user_twitter_object.followers_count
            new_user_object["friends_count"] = new_user_twitter_object.friends_count
            new_user_object["geo_enabled"] = new_user_twitter_object.geo_enabled
            new_user_object["id"] = str(new_user_twitter_object.id)
            new_user_object["lang"] = new_user_twitter_object.lang
            new_user_object["listed_count"] = new_user_twitter_object.listed_count
            new_user_object["location"] = new_user_twitter_object.location
            new_user_object["name"] = new_user_twitter_object.name
            new_user_object["profile_background_color"] = new_user_twitter_object.profile_background_color
            new_user_object["profile_background_image_url"] = new_user_twitter_object.profile_background_image_url
            new_user_object["profile_banner_url"] = new_user_twitter_object.profile_banner_url
            new_user_object["profile_image_url"] = new_user_twitter_object.profile_image_url
            new_user_object["profile_link_color"] = new_user_twitter_object.profile_link_color
            new_user_object["profile_sidebar_fill_color"] = new_user_twitter_object.profile_sidebar_fill_color
            new_user_object["profile_text_color"] = new_user_twitter_object.profile_text_color
            new_user_object["screen_name"] = new_user_twitter_object.screen_name
            new_user_object["statuses_count"] = new_user_twitter_object.statuses_count
            new_user_object["time_zone"] = new_user_twitter_object.time_zone
            new_user_object["url"] = new_user_twitter_object.url
            new_user_object["utc_offset"] = new_user_twitter_object.utc_offset
            new_user_object["verified"] = new_user_twitter_object.verified
            # Append to list
            user_database.append(new_user_object)
            break
        except Exception:
            # Depending on the exception, try to either redo the user download or
            # simply continue on with the download. Error code 50 means user wasn't
            # found and program can continue, otherwise the program should wait 
            # up to 15 minutes
            error_code = None
            print(sys.exc_info())
            if sys.exc_info()[0] == twitter.error.TwitterError:
                try:
                    error_code = sys.exc_info()[1][0][0]["code"]
                except:
                    # Couldn't even retrieve the code... So try again for a 
                    # maximum of up to 15 minutes...
                    print("Unable to retrieve \"" + username + "\", waiting and trying again...")
                    time.sleep(1.05)
                    continue
            if error_code == 50:
                break
            else:
                print("Unable to retrieve \"" + username + "\", waiting and trying again...")
                time.sleep(1.05)

# Write to the user database

user_database_json_string = json.dumps(user_database, separators=(',',':'))
user_database_file = open(input_user_database_filename, "w")
user_database_file.write(user_database_json_string)
user_database_file.close()