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
    assessment_type=get_assessment_bucket_title(gc, sheet_id,tab_number)
    if "words" in assessment_type:
        assessment_type= "sight-words"
    else:
        assessment_type= "letter-sounds"
        
    # assessment_items = get_assessment_items(gc, sheet_id,tab_number)
    assessment_content= get_assessment_bucket(gc, sheet_id,tab_number)
    content_version=get_and_update_content_version(gc, sheet_id,tab_number)
    # Ensure content is formatted appropriately for HTTP response
    json_content = create_json_from_data(assessment_content,lang,assessment_type,content_version)
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


def get_assessment_bucket_title(gc, sheet_id,tab_number):
    sheet = gc.open_by_key(sheet_id)
     # Fetch the worksheet by tab number (index)
    worksheet = sheet[int(tab_number)]
    
    # Get the name of the tab (worksheet title)
    tab_title = worksheet.title
    
    # Select the first worksheet
    tab_name = worksheet.title
    tab_name=re.sub(r"[ -]", "", tab_name)
    return tab_name

def get_and_update_content_version(gc, sheet_id, tab_number):
    # Connect to the spreadsheet
    sheet = gc.open_by_key(sheet_id)
    
    # Fetch the worksheet by tab number (index)
    worksheet = sheet[int(tab_number)]
    
    # Fetch the current content version from cell E1
    content_version = worksheet.cell("E1").value
    if not content_version:
        content_version = "v0.0"
    # Check if the version starts with 'v' and has a numeric part
    if content_version and content_version.startswith('v'):
        # Extract the numeric part of the version (e.g., "v0.1" -> "0.1")
        numeric_version = content_version[1:]
        
        try:
            # Convert the numeric part to a float
            current_version = float(numeric_version)
            
            # Increment the version by 0.1 (adjust this if needed)
            new_version = current_version + 0.1
            
            # Format the new version string (e.g., "v0.2")
            new_version_str = f"v{new_version:.1f}"
            
            # Update the version in cell E1
            worksheet.update_value("E1", new_version_str)
            
            return new_version_str
        
        except ValueError:
            return "Failed to parse the current version. Ensure it is in the format 'vX.Y'."
    else:
        return "Invalid or missing version format in cell E1."


def get_assessment_bucket(gc, sheet_id,tab_number):
    # Connect to the spreadsheet
    sheet = gc.open_by_key(sheet_id)
    # Select the first worksheet
    fetched_sheet = gc.open_by_key(sheet_id)
    # Fetch values from cells A2 to B150
    fetched_content = fetched_sheet[int(tab_number)].get_values("A2","B151")
    return fetched_content

def create_json_from_data(data,lang,assessment_type,content_version):
    bucket_name=lang.replace(" ","-")+"let-b"
    json_data = {
        "quizName": lang+" "+assessment_type.replace("-"," "),
        "appType": "assessment",
        "assessmentType": assessment_type,
        "feedbackText": "fantastic!",
        "contentVersion": content_version,
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