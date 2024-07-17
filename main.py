import functions_framework
import re
import unicodedata
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import codecs
import random
import googleapiclient
import googleapiclient.errors
from datetime import datetime
import xml.etree.ElementTree as ET
import json
import csv
import pygsheets
from google.oauth2 import service_account
from googleapiclient.discovery import build

sec_file = './credentials.json'

@functions_framework.http
def assessment_json_generation(request):
    gc = pygsheets.authorize(service_file=sec_file)
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request_json and "sheet_id" in request_json:
        sheet_id = request_json["sheet_id"]  
    else:
        sheet_id = request.args.get("sheet_id", "English")
        
    lang = request.args.get("lang", "English")
    tab_number=request.args.get("tab",0)
    feedback_tab_number=request.args.get("feedbacktab",0)
    # assessment_items = get_assessment_items(gc, sheet_id,tab_number)
    assessment_content= get_assessment_bucket(gc, sheet_id,tab_number)
    feedback_text=get_feedback_text(gc,sheet_id,feedback_tab_number)
    # Ensure content is formatted appropriately for HTTP response
    json_content = create_json_from_data(assessment_content,lang,feedback_text)
    return json_content

def get_assessment_items(gc, sheet_id,tab_number):
    # Connect to the spreadsheet
    sheet = gc.open_by_key(sheet_id)
    # Select the first worksheet
    fetched_sheet = gc.open_by_key(sheet_id)
    # Fetch values from cells B1 to B150
    fetched_content = fetched_sheet[int(tab_number)].get_values("B2","B101")
    # print(fetched_content,">>>>>>>")
    return fetched_content

def get_feedback_text(gc, sheet_id,feedback_tab_number):
    # Connect to the spreadsheet
    sheet = gc.open_by_key(sheet_id)
    # Select the first worksheet
    fetched_sheet = gc.open_by_key(sheet_id)

    feedback_text_data = fetched_sheet[int(feedback_tab_number)].get_values("B10","B10")
    for row in feedback_text_data:
        feedback_text=unicodedata.normalize('NFC', row[0])
        print(type(feedback_text))
        
    return feedback_text

def get_assessment_bucket(gc, sheet_id,tab_number):
    # Connect to the spreadsheet
    sheet = gc.open_by_key(sheet_id)
    # Select the first worksheet
    fetched_sheet = gc.open_by_key(sheet_id)
    # Fetch values from cells A2 to B150
    fetched_content = fetched_sheet[int(tab_number)].get_values("A2","B151")
    return fetched_content

def create_json_from_data(data,lang,feedback_text):
    bucket_name=lang.replace(" ","-")+"let-b"
    json_data = {
        "quizName": lang+" letter sounds",
        "appType": "assessment",
        "assessmentType": "letter-sounds",
        "feedbackText": feedback_text+"!",
        "contentVersion": "v0.1",
        "buckets": []
    }

    buckets = {}
    for row in data:
        if len(row) < 2:
            continue  # Skip rows that don't have enough columns
        
        bucketID = unicodedata.normalize('NFC', row[0])
        itemName = unicodedata.normalize('NFC', row[1])
        itemText = unicodedata.normalize('NFC', row[1])  # Assuming itemText is the same as itemName, adjust if needed

        if bucketID not in buckets:
            buckets[bucketID] = {
                "bucketID": int(bucketID),
                "bucketName": f"{bucket_name}-{bucketID}",
                "usedItems": [],
                "items": []
            }

        buckets[bucketID]["items"].append({
            "itemName": itemName,
            "itemText": itemText
        })

    json_data["buckets"] = list(buckets.values())

    return json.dumps(json_data, indent=2)