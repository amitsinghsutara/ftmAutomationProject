import pandas as pd
import unicodedata
import json
import os

def create_json_from_data(data, lang, assessment_type, content_version):
    bucket_name = lang.replace(" ", "-") + "let-b"
    json_data = {
        "quizName": lang + " " + assessment_type.replace("-", " "),
        "appType": "assessment",
        "assessmentType": assessment_type,
        "feedbackText": "fantastic!",
        "contentVersion": content_version,
        "buckets": []
    }

    buckets = {}
    for _, row in data.iterrows():
        bucket_id = row[0]
        item_name = row[1]

        if pd.isna(bucket_id) or pd.isna(item_name):
            continue

        bucket_id = unicodedata.normalize('NFC', str(bucket_id))
        item_name = unicodedata.normalize('NFC', str(item_name))
        item_text = item_name  # Same as item_name unless specified

        if bucket_id not in buckets:
            buckets[bucket_id] = {
                "bucketID": int(bucket_id),
                "bucketName": f"{bucket_name}-{bucket_id}",
                "usedItems": [],
                "items": []
            }

        buckets[bucket_id]["items"].append({
            "itemName": item_name,
            "itemText": item_text
        })

    json_data["buckets"] = list(buckets.values())
    return json_data

def main():
    excel_path = "Assessment Worksheet_Hausa.xlsx"  # Change if your file is named differently
    sheet_name = "Letter Sounds"  # Or "SightWords" etc.
    lang = "hausa"
    assessment_type = "letter-sounds"  # or "letter-sounds"
    content_version = "v0.1"

    if not os.path.exists(excel_path):
        print(f"File '{excel_path}' not found.")
        return

    df = pd.read_excel(excel_path, sheet_name=sheet_name, usecols=[0, 1])
    result = create_json_from_data(df, lang, assessment_type, content_version)

    with open("assessment_output.json", "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("✅ assessment_output.json has been created.")

if __name__ == "__main__":
    main()
