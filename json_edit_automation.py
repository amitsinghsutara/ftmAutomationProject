
import json

# Step 1: Load the content.json file
with open('./content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
count =209;
# Step 2: Get unique languages based on the "language" field
unique_languages = {}
for app in data['web_apps']:
    lang = app['language']
    if lang not in unique_languages:
        count+=1
        unique_languages[lang] = {
            "appId": count,
            "appIconUrl": "https://devcuriousreader.wpcomstaging.com/container_app_manifest/icons/Parent_Survey.png",
            "title": "Parent Survey"+" "+lang,
            "appUrl": "https://docs.google.com/forms/d/e/1FAIpQLSfbQlN7luAb-CUe7ryrmtG6vQQyNxisCTWCRWUYOsIddkrtLw/viewform?usp=pp_url&entry.258668693=",
            "language": lang,
            "languageInEnglishName": app['languageInEnglishName'],
              # You can populate this list as needed
        }

# Step 3: Create a new JSON structure with language-specific content
output = {
    'version': data['version'],
    'web_apps': list(unique_languages.values())
}

# Optional: Save it back to a new file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print("✅ Process completed. `output.json` generated.",count)
