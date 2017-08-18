#!/usr/bin/python

import sys
import json
import time
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

input_filename = sys.argv[1]

with open(input_filename) as input_file:
    input_data = json.load(input_file)

client = language.LanguageServiceClient()

def determine_sentiment(text):
    return client.analyze_sentiment(document=types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT))

for i, tweet in enumerate(input_data):
    try:
        print("Analyzing sentiment for tweet with ID number \"" + tweet["id"] + "\"")
        time.sleep(0.12)
        input_data[i]["sentiment"] = determine_sentiment(tweet["text_filtered"]).document_sentiment.score
    except Exception as e:
        print("Error encountered, waiting 5 seconds and continuing...")
        print(str(e) + "\n\n\n")
        time.sleep(5.0)

final_json = json.dumps(input_data, separators=(",",":"))
final_file = open(input_filename[:-5] + "_with_sentiment.json", "w")
final_file.write(final_json)
final_file.close()