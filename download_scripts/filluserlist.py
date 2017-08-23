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

input_filename = sys.argv[1]

with open(input_filename) as input_file:
    input_data = json.load(input_file)

with open("userdatabase3.json") as database_file:
    user_database = json.load(database_file)

api = twitter.Api(consumer_key = "f6A1A608PQldoOdpkpd79gZ1Q",
    consumer_secret = "jqOoY4wjKgrLdj7LzSFNi0lBe6vZwRJW0uUrtbhJwNjo0qlJiG", 
    access_token_key = "898010337089265664-UiiDbwZ4meFJc0GMsgampuLJMUwgcgg", 
    access_token_secret = "qnXC6axFM18NQ2yWouTdpoJdkCk8okI9urmNjUAGa8zKo",
    sleep_on_rate_limit = True)

# Go through each tweet/set of retweets (if existing), getting the user 
# screen_name and then testing this against the user_database to see if it's 
# already in the database; if not, then add it to the database

def check_for_screen_name_in_database(screen_name):
    for user in user_database:
        if str(user["screen_name"]).lower() == str(screen_name).lower():
            return True
    return False

def check_for_user_id_number_in_database(id_num):
    for user in user_database:
        if str(user["id"]).lower() == str(id_num).lower():
            return True
    return False

def convert_user_id_to_screen_name(uid):
    screen_name = ""
    for i in range(900):
        try:
            screen_name = str(api.GetUser(user_id = uid).screen_name).lower()
            break
        except Exception as e:
            print(e)
            print("Couldn't retrieve screen name for user with ID \"" + \
            str(uid) + "\", waiting a second and trying again...")
            time.sleep(1.05)
    if screen_name == "":
        raise Exception("Couldn't find id number \"" + str(uid) + "\"")
    return screen_name

names_do_not_try = []

# First, loop through data to get an estimate of how long this'll take to run

full_user_list = ["fredhutch"]

def check_user_in_user_list(screen_name):
    for username in full_user_list:
        if str(screen_name.lower()) == str(username.lower()):
            return True
    return False

for tweet in input_data:
    if "retweets_data" in tweet:
        for retweet in tweet["retweets_data"]:
            if not check_user_in_user_list(retweet["username"]):
                full_user_list.append(str(retweet["username"]))
    mentioned_usernames = tweet["mentions"].split("@")[1:]
    for k, username in enumerate(mentioned_usernames):
        mentioned_usernames[k] = mentioned_usernames[k].strip().lower()
    for username in mentioned_usernames:
        if username != "":
            if str(username)[-4:] == "http":
                username = str(username)[0:len(str(username)) - 4].lower()
            if str(username)[-5:] == "https":
                username = str(username)[0:len(str(username)) - 5].lower()
            if str(username)[-3:] == "pic":
                username = str(username)[0:len(str(username)) - 3].lower()
            if not check_user_in_user_list(username):
                full_user_list.append(username)
    if "favoriting_users" in tweet:
        for favoriting_user_id_string in tweet["favoriting_users"]:
            if not check_user_in_user_list(str(favoriting_user_id_string)):
                full_user_list.append(str(favoriting_user_id_string).strip())

number_of_users_roughly = len(full_user_list)

def remove_all_instances_of_item_from_list(item_to_remove, list_to_use):
    return filter(lambda a: a != item_to_remove, list_to_use)

# Now convert the users in full_user_list that are in numeric form to their 
# username equivalent and delete duplicates

count = 0

for index, username in enumerate(full_user_list):
    in_regular_form = True
    try:
        int(username)
        in_regular_form = False
    except:
        # This means it can't be converted to regular form
        # I.E. it's already in regular form
        True
    if not in_regular_form:
        try:
            full_user_list[index] = convert_user_id_to_screen_name(username).lower()
        except Exception as e:
            print(e)
            # Couldn't find user ID on Twitter
            # Continue without changing the number to a screen_name
            continue
    # Remove any trailing oddities that cause illegitimate usernames
    if str(full_user_list[index])[-4:] == "http":
        full_user_list[index] = \
            str(full_user_list[index])[0:len(str(full_user_list[index])) - 4]
    if str(full_user_list[index])[-5:] == "https":
        full_user_list[index] = \
            str(full_user_list[index])[0:len(str(full_user_list[index])) - 5]
    if str(full_user_list[index])[-3:] == "pic":
        full_user_list[index] = \
            str(full_user_list[index])[0:len(str(full_user_list[index])) - 3]
    # Convert to lowercase for safekeeping
    full_user_list[index] = str(full_user_list[index].lower())
    print(full_user_list[index])

full_user_list = list(set(full_user_list))

# Remove numbers in full_user_list

for user in list(full_user_list):
    in_regular_form = True
    try:
        int(user)
        in_regular_form = False
    except:
        True
    if not in_regular_form:
        full_user_list = remove_all_instances_of_item_from_list(user, full_user_list)

for user in full_user_list:
    in_regular_form = True
    try:
        int(user)
        in_regular_form = False
    except:
        True
    if in_regular_form:
        count = count + 1

# Save the user list to a JSON file

user_list_json_string = json.dumps(full_user_list, separators=(',',':'))
user_list_file = open("userlist.json", "w")
user_list_file.write(user_list_json_string)
user_list_file.close()