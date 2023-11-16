from google.oauth2 import service_account
from googleapiclient.discovery import build
import gdown
import base64
import requests
import shutil
import json
import re
import subprocess
from pydub import AudioSegment

# Path to the JSON key file you downloaded when setting up the service account.
KEY_FILE = '/run/media/amitsingh/New Volume/Sutara/NewProject/FeedTheMonsterJS/Automation Scripts/credentials.json'
missing_audios_on_drive= set()
present_audios_on_drive= set()
# The Google Drive API version to use.
API_VERSION = 'v3'

# Create a service account credentials object.
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=['https://www.googleapis.com/auth/drive'])

# Create a Drive API service.
drive_service = build('drive', API_VERSION, credentials=credentials)


def download_audio_files(drive_id,folder_id,file_name,lang,wav_unique_prompt_texts,unique_prompt_texts,depth=0):
    # # Query for audio files in the selected folder
    
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': drive_id,
        'q': f"'{folder_id}' in parents ",
    }
    
    results = drive_service.files().list(**query_params).execute()
    audio_files = results.get('files', [])
    if not audio_files:
        return
    
    

    # Loop through the audio files and download each one
    for audio_file in audio_files:
        file_name = audio_file["name"]
        file_id = audio_file["id"]
        file_name=get_correct_file_name(file_name)

        if file_name in wav_unique_prompt_texts or file_name in unique_prompt_texts:
            if file_name not in present_audios_on_drive:
                name=file_name.lower()
    
                if name.endswith('.wav'):
                    new_file_name=name.replace(".wav", ".mp3")
                    present_audios_on_drive.add(new_file_name)
                elif name.endswith('.mp3'):
                    present_audios_on_drive.add(name)
                
                        


def get_correct_file_name(filename):
    keywords_to_remove = ["_feedback", "_sound", "_word", "_syllable", "_memory"]
    if filename == "fantastic1.wav" or filename == "fantastic1.mp3":
        filename = "fantastic.wav"
        print(filename+"<<<<<<<<<<<")

        
    for keyword in keywords_to_remove:
        if keyword in filename:
            filename = filename.replace(keyword, "")

    return filename.lower()






def list_contents_and_download(drive_id, folder_id,lang,wav_unique_prompt_texts,unique_prompt_texts, depth=0):
    # Query for contents in the selected folder
    
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': drive_id,
        'q': f"'{folder_id}' in parents ",
    }
    
    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])

    # Create the output folder if it doesn't exist
    

    for content in contents:
        if content['mimeType'] == 'application/vnd.google-apps.folder':
            # If it's a folder, call the function recursively
            list_contents_and_download(drive_id, content['id'],lang,wav_unique_prompt_texts,unique_prompt_texts, depth + 1)
        
            
        download_audio_files(drive_id, content['id'],content['name'],lang,wav_unique_prompt_texts,unique_prompt_texts,depth+1)


def list_english_content(drive_id, folder_id,unique_prompt_texts,lang,wav_unique_prompt_texts, depth):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': drive_id,
        'q': f"'{folder_id}' in parents",
    }

    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])

    for i, content in enumerate(contents, start=1):
        content_name=content["name"].lower()
        processed_string = content_name.replace(" ", "").replace("-", "").lower()
        if lang in processed_string:
            list_contents_and_download(drive_id,content["id"],lang,wav_unique_prompt_texts,unique_prompt_texts,depth+1)

def list_contents_of_folder(drive_id, folder_id,unique_prompt_texts,lang,wav_unique_prompt_texts, depth=0):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': drive_id,
        'q': f"'{folder_id}' in parents",
    }

    results = drive_service.files().list(**query_params).execute()
    contents = results.get('files', [])
    
    selected_folder=None

    for i, content in enumerate(contents, start=1):
        content_name=content["name"].lower()
        if "english" in content_name:
            list_english_content(drive_id, content["id"],unique_prompt_texts,lang,wav_unique_prompt_texts, depth + 1)
        
        if lang in content_name:
            list_contents_and_download(drive_id,content["id"],lang,wav_unique_prompt_texts,unique_prompt_texts,depth+1)
        
    

def check_in_drive(drive_id, folder_id, desired_folder_id,unique_prompt_texts,wav_unique_prompt_texts,lang,depth =0):
    query_params = {
        'supportsAllDrives': True,
        'includeItemsFromAllDrives': True,
        'corpora': 'drive',
        'driveId': drive_id,
        'q': f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'",
    }
    results = drive_service.files().list(**query_params).execute()
    folders = results.get('files', [])
    if not folders:
        return

    for folder in folders:
        if folder["id"] == desired_folder_id:
            # You've reached the desired folder, now you can list its contents or perform any desired actions.
            list_contents_of_folder(drive_id, folder["id"],unique_prompt_texts,lang,wav_unique_prompt_texts, depth + 1)
           
                        
        else:
            if folder["id"]=="1241p6yE0at78OZVdTewJSWS6XdjPjx93" or folder["id"]=="1lsbOukZZTFGJI8tTMRGDTi1QpuiAGJaR" or folder["id"]=="1dVw3lRUcP0vHP8qGhGqeHmG0Elflx2HY" or folder["id"]=="1xTln0bFAGJe3hhWu_KdpdQb7gQcSAktG":
                check_in_drive(drive_id, folder['id'], desired_folder_id,unique_prompt_texts,wav_unique_prompt_texts,lang, depth + 1)
    
    missing_audios_on_drive =unique_prompt_texts-present_audios_on_drive            
    return missing_audios_on_drive