import json
import os

# def construct_json_path(root_folder, language):
#     json_path = os.path.join(root_folder, language, f"ftm_{language}.json")
#     return json_path

# language=input("Enter the language")
# # Load JSON data
# data = json.loads(json_data)

# # Initialize a set to hold distinct item names
def find_prompt_audios(json_path):
    with open(json_path, "r",encoding="utf8") as json_file:
            data = json.load(json_file)
    item_names = set()
# Iterate through buckets and items to collect item names
    for bucket in data['buckets']:
      for item in bucket['items']:
        item_names.add(item['itemName'])

# # Print the set of distinct item names
    # print(item_names)
    return item_names



def construct_json_path(root_folder, language):
    # language=language.replace(" ","-")
    json_path = os.path.join(root_folder,"data", f"{language}-lettersounds.json")
    return json_path

def check_prompt_audios(json_path, audios_folder, prompt_audio_urls):
    try:
        missing_prompt_audios = []

        for prompt_audio_name in prompt_audio_urls:
            prompt_audio_name=prompt_audio_name.lower()
            
            prompt_audio_path = os.path.join(audios_folder, prompt_audio_name+".mp3")
            print(">>>>>>>>>", prompt_audio_path)
            if not os.path.exists(prompt_audio_path.lower()):
                missing_prompt_audios.append(prompt_audio_name)

        if missing_prompt_audios:
            print("Prompt audios missing in the audios folder:")
            for missing_audio in missing_prompt_audios:
                print(missing_audio)
        else:
            print("All prompt audios are present in the audios folder.")
    except Exception as e:
        print("Error checking prompt audios:", e)

if __name__ == "__main__":
    root_folder = r"../assessment-survey-js/"
   
    language = input("Enter the language: ")
    language = language.replace(" ","-")
    json_path = construct_json_path(root_folder, language)
    audios_folder = os.path.join(root_folder, "audio",f"{language}-lettersounds")
    print("Constructed JSON path:", json_path)
    
    prompt_audio_urls = find_prompt_audios(json_path)
    print("Prompt audio URLs:", prompt_audio_urls)
    check_prompt_audios(json_path, audios_folder, prompt_audio_urls)



