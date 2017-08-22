#!/usr/bin/python

import sys
from openpyxl import load_workbook
import json

input_json_filename = sys.argv[1]
input_xlsx_filename = sys.argv[2]

with open(input_json_filename) as input_json_file:
    input_json_data = json.load(input_json_file)

input_workbook = load_workbook(filename = input_xlsx_filename)
input_worksheet = input_workbook.active

input_worksheet_tweet_id_range_cells = input_worksheet["AB2":"AB6830"]
input_worksheet_category_range_cells = input_worksheet["AE2":"AE6830"]
input_worksheet_source_range_cells = input_worksheet["M2":"M6830"]

input_worksheet_tweet_id_list = []
input_worksheet_category_list = []
input_worksheet_source_list = []

for index, item in enumerate(input_worksheet_tweet_id_range_cells):
    input_worksheet_tweet_id_list.append(str(item[0].value))
    input_worksheet_category_list.append(str(input_worksheet_category_range_cells[index][0].value))
    input_worksheet_source_list.append(str(input_worksheet_source_range_cells[index][0].value))

for i, tweet_id in enumerate(input_worksheet_tweet_id_list):
    # Find the tweet in our database that matches this ID and append the other 
    # information to the master database
    for k, tweet in enumerate(input_json_data):
        if str(tweet["id"]) == str(tweet_id):
            # This is the matching tweet in our database, so add the info
            input_json_data[k]["category"] = input_worksheet_category_list[i]
            input_json_data[k]["source"] = input_worksheet_source_list[i]

final_json = json.dumps(input_json_data, separators=(",",":"))
final_file = open(input_json_filename[:-5] + "_with_excel_data.json", "w")
final_file.write(final_json)
final_file.close()