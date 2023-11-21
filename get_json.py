import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the JSON key file you downloaded when setting up the service account.
KEY_FILE = './credentials.json'

# The Google Drive API version to use.
API_VERSION = 'v3'

# Create a service account credentials object.
credentials = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=['https://www.googleapis.com/auth/drive'])

# Create a Drive API service.
drive_service = build('drive', API_VERSION, credentials=credentials)


def get_json_data(lang,drive_id,folder_id,depth=0):
    
    is_json_generated= list_initial_files(drive_id,"18SRLdZK-n2QismpXY1Cn-FFqrJutIU8I",depth+1,lang)
    return is_json_generated
    




def list_initial_files(drive_id,folder_id,depth,lang):
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
        file_name=content["name"].lower()
        if file_name == lang:
          is_generation_sucessful=  generate_json_file(lang,content["id"]);
          return is_generation_sucessful
            
    

def generate_json_file(lang,id):
    url = 'https://us-central1-ftm-b9d99.cloudfunctions.net/hello-world?act=generate&sheet='+id
    
    
    response = requests.get(url)

# Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Parse the JSON content
        json_data = response.json()
        
    
        result =ProcessLookupError(json_data)

        return json_data
    else:
        print(f"Failed to fetch JSON data. Status code: {response.status_code}")
        return  null

    
def process_data(json_data):
    # Example operation: Summing values in a list
    if 'values' in json_data and isinstance(json_data['values'], list):
        total = sum(json_data['values'])
        return total
    else:
        return "Invalid JSON format"