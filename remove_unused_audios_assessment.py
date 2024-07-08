import json
import os


# # Initialize a set to hold distinct item names
def find_prompt_audios(json_path):
    with open(json_path, "r",encoding="utf8") as json_file:
            data = json.load(json_file)
    item_names = set()
# Iterate through buckets and items to collect item names
    for bucket in data['buckets']:
      for item in bucket['items']:
        audios=item['itemName']+".mp3"
        item_names.add(audios.lower())

    return item_names



def construct_json_path(root_folder, language):
    # language=language.replace(" ","-")
    json_path = os.path.join(root_folder,"data", f"{language}-lettersounds.json")
    return json_path

def find_audios_in_folder(audios_folder):
    try:
        audio_files = [filename for filename in os.listdir(audios_folder) if os.path.isfile(os.path.join(audios_folder, filename))]
        return audio_files
    except Exception as e:
        print("Error finding audio files in folder:", e)
        return []

def deleteAudio(file_path):
    if os.path.exists(file_path):
        #  os.remove(file_path)
         print(f"File {file_path} has been deleted.")
    else:
     print(f"The file {file_path} does not exist.")

def remove_unused_audios(json_path, audios_folder, prompt_audio_urls):
    # try:
        audio_files_in_folder=find_audios_in_folder(audios_folder)
        for audio_file in audio_files_in_folder:
            if audio_file.lower() not in prompt_audio_urls:
               
                audio_path=os.path.join(audios_folder,audio_file)
                
                deleteAudio(audio_path)

if __name__ == "__main__":
    root_folder = r"../assessment-survey-js/"
   
    language = input("Enter the language: ")
    language = language.replace(" ","-")
    json_path = construct_json_path(root_folder, language)
    audios_folder = os.path.join(root_folder, "audio",f"{language}-lettersounds")
    
    prompt_audio_urls = find_prompt_audios(json_path)
    remove_unused_audios(json_path, audios_folder, prompt_audio_urls)



