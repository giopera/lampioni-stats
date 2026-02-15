
from datetime import datetime
import json
import os

DATA_DIR = "./data/"
OUT_DIR = DATA_DIR + datetime.today().strftime('%Y-%m-%d') + "/"

def generate_user_total(base_data):
    base_data = base_data["elements"]
    users={}
    for element in base_data:
        if not users.get(element["user"]):
            users[element["user"]] = 0
        users[element["user"]] = users[element["user"]] + 1
    return users

def generate_user_daily(base_data):
    base_data = base_data["elements"]
    days={}
    for element in base_data:
        date = element["timestamp"].split('T', 1)[0]
        if not days.get(date):
            days[date] = {}
        if not days.get(date).get(element["user"]):
            days[date][element["user"]] = 0
        days[date][element["user"]] = days[date][element["user"]] + 1
    return days

def generate_tags_daily(base_data):
    base_data = base_data["elements"]
    tags={}
    for element in base_data:
        date = element["timestamp"].split('T', 1)[0]
        if not tags.get(date):
            tags[date] = {}
        for tag, value in element["tags"].items():
            key = tag.lower()
            if not tags.get(date).get(key):
                tags[date][key] = 0
            tags[date][key] = tags[date][key] + 1
    return tags

def generate_tags_total(base_data):
    base_data = base_data["elements"]
    tags={}
    for element in base_data:
        for tag, value in element["tags"].items():
            key = tag.lower()
            if not tags.get(key):
                tags[key] = 0
            tags[key] = tags[key] + 1
    return tags

if __name__ == "__main__":
    base_data = {}
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_DIR + "data.json", 'r') as f:
        base_data = json.loads(f.read())
    with open(OUT_DIR + "users_total.json", 'w') as f:
        f.write(json.dumps(generate_user_total(base_data), ensure_ascii=False))
    with open(OUT_DIR + "users_daily.json", 'w') as f:
        f.write(json.dumps(generate_user_daily(base_data), ensure_ascii=False))
    with open(OUT_DIR + "tags_total.json", 'w') as f:
        f.write(json.dumps(generate_tags_total(base_data), ensure_ascii=False))
    with open(OUT_DIR + "tags_daily.json", 'w') as f:
        f.write(json.dumps(generate_tags_daily(base_data), ensure_ascii=False))