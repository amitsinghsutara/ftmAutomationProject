
# import json

# # Step 1: Load the content.json file
# with open('./content.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
# count =209;
# # Step 2: Get unique languages based on the "language" field
# unique_languages = {}
# for app in data['web_apps']:
#     lang = app['language']
#     if lang not in unique_languages:
#         count+=1
#         unique_languages[lang] = {
#             "appId": count,
#             "appIconUrl": "https://devcuriousreader.wpcomstaging.com/container_app_manifest/icons/Parent_Survey.png",
#             "title": "Parent Survey"+" "+lang,
#             "appUrl": "https://docs.google.com/forms/d/e/1FAIpQLSfbQlN7luAb-CUe7ryrmtG6vQQyNxisCTWCRWUYOsIddkrtLw/viewform?usp=pp_url&entry.258668693=",
#             "language": lang,
#             "languageInEnglishName": app['languageInEnglishName'],
#               # You can populate this list as needed
#         }

import json

# Step 1: Load the content.json file
with open('./content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Step 2: Update appId for each web_app
start_count = 82
for i, app in enumerate(data['web_apps']):
    app['appId'] = start_count + i

# Step 3: Save updated structure to a new file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ Process completed. Updated {len(data['web_apps'])} web apps starting from appId {start_count}.")
