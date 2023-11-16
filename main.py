from flask import escape
from get_json import get_json_data
import functions_framework
from check_in_drive import check_in_drive
from send_report import inform_user_about_updates
import logging
import re

@functions_framework.http
def main_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    shared_drive_id = '0AArPHFZAiZRmUk9PVA'
    root_folder_id = '0AArPHFZAiZRmUk9PVA'  # You can specify the folder ID if you want to start from a specific folder.
    desired_folder_id = '1wwOr5zIuwGWID7m4AW3SInh2M_GN-nwp'   # Replace with the ID of your desired folder.
    receiver=["amit@sutara.org","nikhilchoudhary@sutara.org"]
    
    body = "Hello,\n\n"
    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        lang = request.args.get("lang", "English")
        subject=lang+"  "+"Feed the Monster Automation Report"
        json_data=get_json_data(lang,shared_drive_id,root_folder_id)
        if not json_data:
            body="There was error while generating json,\n Make sure that the language name is correct"
            inform_user_about_updates(receiver,subject,body)
            return
        prompt_text=find_unique_audio_urls(json_data)
        wav_prompt_text=find_unique_wav_audio_texts(prompt_text)
        output= check_in_drive(shared_drive_id,root_folder_id,desired_folder_id,prompt_text,wav_prompt_text,lang)
        body += "JSON generation process is successful.\n"
        body += "Checking for audios is done. Here is the list of missing audios:\n"
        body += "\n".join(output) 
        inform_user_about_updates(receiver,subject,body)
        name = "World"


    return f"missing audios in google drive-->{body}"

                        
                        


def find_unique_audio_urls(obj, unique_audio_keys=None):
    feedback_words = ['amazing.mp3', 'fantastic.mp3', 'great1.mp3', 'amazing.mp3']
    if unique_audio_keys is None:
        unique_audio_keys = set()
    for feedback in feedback_words:
        unique_audio_keys.add(feedback)
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "PromptAudio" or key == "FeedbackAudios" or key == "OtherAudios":
                if isinstance(value, list):
                    for url in value:
                        match = re.search(r'/(\w+\.mp3)$', url)
                        if match:
                            audio_key = match.group(1)
                            unique_audio_keys.add(audio_key)
                elif isinstance(value, str):
                    match = re.search(r'/(\w+\.mp3)$', value)
                    if match:
                        audio_key = match.group(1)
                        unique_audio_keys.add(audio_key)
            if isinstance(value, (dict, list)):
                find_unique_audio_urls(value, unique_audio_keys)

    elif isinstance(obj, list):
        for item in obj:
            if isinstance(item, (dict, list)):
                find_unique_audio_urls(item, unique_audio_keys)

    return unique_audio_keys

def find_unique_wav_audio_texts(unique_prompt_texts):
    wav_prompt_texts=set()
    for prompt_text in unique_prompt_texts:
        wav_prompt = prompt_text.replace(".mp3", ".wav")
        wav_prompt_texts.add(wav_prompt)
    return wav_prompt_texts