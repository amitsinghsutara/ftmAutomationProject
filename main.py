import functions_framework
import re
import unicodedata
import requests
import os
import functions_framework
import codecs
import random
import googleapiclient
import googleapiclient.errors
from datetime import datetime
import xml.etree.ElementTree as ET
import os
import json
import csv
import pygsheets
import unicodedata
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.discovery import build
root_drive_id="0AArPHFZAiZRmUk9PVA"
drive_folder_id = "16mfArt7NQds_jTYPYAp_Hp7thkQ3SD8v"
teamid = "0AArPHFZAiZRmUk9PVA"
## client secrets location
sec_file = './credentials.json'
amit_json ='./sec.json'
# The Google Drive API version to use.
API_VERSION = 'v3'
lang="English"
feedback_audios=["fantastic","great","amazing"]
# Create a service account credentials object.
credentials = service_account.Credentials.from_service_account_file(
    sec_file, scopes=['https://www.googleapis.com/auth/drive'])

# Create a Drive API service.
drive_service = build('drive', API_VERSION, credentials=credentials)

@functions_framework.http
def content_verification(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    
    
    gc = pygsheets.authorize(service_file=sec_file)
    # gc.drive.enable_team_drive(teamid);

    request_json = request.get_json(silent=True)
    request_args = request.args
    
    
    body = "Hello,\n\n"
    if request_json and "sheet_id" in request_json:
        sheet_id = request_json["sheet_id"]
    elif request_json and "lang" in request_json:
        lang =request_json["lang"]
    else:
        sheet_id = request.args.get("sheet_id", "English")
        lang=request.args.get("lang","English")
       
    assesment_data=get_assessment_data(gc,sheet_id)
    missing_audio_assets=check_missing_audio_assets_in_drive(drive_service, root_drive_id,root_drive_id,depth=0)
    return f"missing audios in google drive-->{body}"

def get_assessment_data(gc, sheet_id):
    # connect to the spreadsheet
    fetched_sheet = gc.open_by_key(sheet_id)
    fetched_content = fetched_sheet[1].get_values("B1","B150")
    unique_content=get_unique_content(fetched_content)
    return unique_content



def get_unique_content(fetched_content):
    unique_characters = set()
    for sublist in fetched_content:
      for item in sublist:
        item = unicodedata.normalize('NFKD',item)
        unique_characters.update(item.split(','))
    return unique_characters

def check_missing_audio_assets_in_drive(drive_service, root_drive_id,drive_id,depth ):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': root_drive_id,
        'q': f"'{drive_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
    }
    missing_audios= set()
    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])
    try:
    
        for i, content in enumerate(contents, start=1):
            print('  ' * depth + f'{content["name"]} ({content["id"]})')
            if content["id"] =="1241p6yE0at78OZVdTewJSWS6XdjPjx93":
                check_missing_audio_assets_in_drive(drive_service,root_drive_id,content["id"],depth+1)
            elif content["id"]=="16mfArt7NQds_jTYPYAp_Hp7thkQ3SD8v":
            #    missing_feedback_audios= check_feedback_audios_in_drive(drive_service,root_drive_id,content["id"],depth+1)
               missing_audios= check_audios_in_folder(drive_service,root_drive_id,content["id"],depth+1)
            
    except googleapiclient.errors.HttpError as e:
        error_details = e._get_reason()
        if 'notFound' in error_details:
            print("Shared drive not found. Skipping...")
        else:
            # Handle other types of errors
            print("An error occurred:", error_details)        
                         
    
    
    return missing_audios

def check_audios_in_folder(drive_service, root_drive_id,drive_id,depth):
    
    print(">>>>")
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': root_drive_id,
        'pageSize':500,
        'q': f"'{drive_id}' in parents ",
    }
    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])
    for i, content in enumerate(contents, start=1):
        print('  ' * depth + f'{content["name"]} ({content["id"]})')
        if content["id"]=="1_OKwBPcv9PQqp8v-L4sNTFhX0tF6NtgH":
            check_audios_in_folder(drive_service, root_drive_id,content["id"],depth)
            
        if lang.lower() ==content["name"].lower():
            missing_audios= check_audios_in_lang_folder(drive_service, root_drive_id,content["id"],depth)
    return depth

def check_audios_in_lang_folder(drive_service, root_drive_id,drive_id,depth ):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': root_drive_id,
        'pageSize':500,
        'q': f"'{drive_id}' in parents ",
    }
    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])
    for i, content in enumerate(contents, start=1):
        print('  ' * depth + f'{content["name"]} ({content["id"]})'+">>>>")
        check_audios_in_lang_folder(drive_service, root_drive_id,content["id"],depth)
    return depth
def check_feedback_audios_in_drive(drive_service, root_drive_id,drive_id,depth ):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': root_drive_id,
        'q': f"'{drive_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
    }
    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])
    for i, content in enumerate(contents, start=1):
        print('  ' * depth + f'{content["name"]} ({content["id"]})')
        # if content["id"]=="1cDNqpl6hpponslP8XFAc37BNlZv3bW4X" or content["id"]=="1eXmu1e8G7l881tHB-g6zL9FBPMmlNvI3" or content["id"]=="1qhKKLccb2jznBY070Cq4h5ozL41EweSk":
        #     check_feedback_audios_in_drive(drive_service,root_drive_id,content["id"],depth+1)


        if lang.lower() == content["name"].lower():
            missing_audios=list_missing_feedback_audios(drive_service,root_drive_id,content["id"],depth+1)
        
    return depth

def list_missing_feedback_audios(drive_service, root_drive_id,drive_id,depth):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': root_drive_id,
        'pageSize':500,
        'q': f"'{drive_id}' in parents ",
    }
    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])
    for i, content in enumerate(contents, start=1):
        filename, extension = os.path.splitext(content["name"].lower())
        if filename in feedback_audios:
            print("feedback audios available")
        
        print('  ' * depth + f'{content["name"]} ({content["id"]})'+lang.lower())
        
            
        
    return depth