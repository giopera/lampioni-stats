from datetime import datetime
import json
import os
from types import NoneType
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA_DIR = "./data/"
STAT_DIR = DATA_DIR + datetime.today().strftime('%Y-%m-%d') + "/"
IMG_DIR = "./img/"
OUT_DIR = IMG_DIR + datetime.today().strftime('%Y-%m-%d') + "/"

def get_ints_tuple(tup, index, default=0):
    try:
        if type(tup[index]) is NoneType:
            return 0
        return tup[index]
    except IndexError:
        return default

def tags_total(stats):
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=False))
    user = list(sorted_stats.keys())
    number = list(sorted_stats.values())

    fig, ax = plt.subplots(figsize=(30, len(user) * 0.3))

    ax.barh(user, number)
    ax.set_xlabel('Total Number')
    ax.set_ylabel('Tags')

    plt.savefig(OUT_DIR + "tags_total.svg")

    plt.tight_layout()
    plt.close()

def users_total(stats):
    sorted_stats = dict(sorted(stats.items(), key=lambda x: x[1], reverse=False))
    user = list(sorted_stats.keys())
    number = list(sorted_stats.values())

    fig, ax = plt.subplots(figsize=(30, len(user) * 0.3))
    #fig, ax = plt.subplots(figsize=(30, len(user) * 0.3))

    ax.barh(user, number)
    ax.set_xlabel('Total Number')
    ax.set_ylabel('Users')

    plt.savefig(OUT_DIR + "users_total.svg")

    plt.tight_layout()
    plt.close()


def users_daily(stats, all_users):
    converted_stats = {}
    for date_str, data in stats.items():
        try:
            dt_obj = datetime.strptime(date_str, '%Y-%m-%d') 
            converted_stats[dt_obj] = data
        except ValueError:
            continue

    sorted_stats = dict(sorted(converted_stats.items()))
    dates = list(sorted_stats.keys())
    
    users_values = {user: [] for user in all_users}

    for _, day_data in sorted_stats.items():
            for user in all_users:
                val = day_data.get(user, 0)
                
                prev_val = 0
                if users_values[user]:
                    last_entry = users_values[user][-1]
                    if last_entry is not None:
                        prev_val = last_entry
                
                current_total = prev_val + val

                if current_total == 0:
                    users_values[user].append(None)
                else:
                    users_values[user].append(current_total)
    
    users_values = dict(sorted(users_values.items(), key=lambda x: get_ints_tuple(x[1], -1, default=0)))

    fig, ax = plt.subplots(figsize=(20, 30)) 

    labels_to_plot = []
    colors = ['blue','green','red','cyan','magenta','yellow','black']
    
    i = 0
    for user, values in users_values.items():
        if any(v is not None for v in values):
            line, = ax.plot(dates, values, label=user, color=colors[i])
            i = i + 1
            i = i % len(colors)
            
            if values[-1] is not None:
                labels_to_plot.append({
                    "val": values[-1], 
                    "user": user, 
                    "color": line.get_color()
                })

    labels_to_plot.sort(key=lambda x: x["val"])

    last_y = 0
    spacing_factor = 1.1 

    for item in labels_to_plot:
        val = item["val"]
        color = item["color"]
        user = item["user"]

        text_y = max(val, last_y * spacing_factor)
        last_y = text_y
        ax.text(
            1.02, text_y, 
            user, 
            color=color, 
            transform=ax.get_yaxis_transform(),
            va='center',
            weight='bold',
            fontsize=10
        )

    ax.set_yscale('log')
    ax.set_xlabel('Dates')
    ax.set_ylabel('Cumulative Users')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    plt.subplots_adjust(right=0.85) 

    plt.tight_layout()
    plt.savefig(OUT_DIR + "users_daily.svg")
    plt.close()

def users_daily_cropped(stats, all_users):
    converted_stats = {}
    for date_str, data in stats.items():
        try:
            dt_obj = datetime.strptime(date_str, '%Y-%m-%d') 
            converted_stats[dt_obj] = data
        except ValueError:
            continue

    sorted_stats = dict(sorted(converted_stats.items()))
    dates = list(sorted_stats.keys())
    
    users_values = {user: [] for user in all_users}

    for _, day_data in sorted_stats.items():
            for user in all_users:
                val = day_data.get(user, 0)
                
                prev_val = 0
                if users_values[user]:
                    last_entry = users_values[user][-1]
                    if last_entry is not None:
                        prev_val = last_entry
                
                current_total = prev_val + val

                if current_total == 0:
                    users_values[user].append(None)
                else:
                    users_values[user].append(current_total)
    
    users_values = sorted(users_values.items(), key=lambda x: get_ints_tuple(x[1], -1, default=0), reverse=True)

    tmp = []
    for i in range(20):
        tmp.append(users_values[i])

    users_values = dict(tmp)

    fig, ax = plt.subplots(figsize=(20, 30)) 

    labels_to_plot = []
    colors = ['blue','green','red','cyan','magenta','yellow','black']
    
    i = 0
    for user, values in users_values.items():
        if any(v is not None for v in values):
            line, = ax.plot(dates, values, label=user, color=colors[i])
            i = i + 1
            i = i % len(colors)
            
            if values[-1] is not None:
                labels_to_plot.append({
                    "val": values[-1], 
                    "user": user, 
                    "color": line.get_color()
                })

    labels_to_plot.sort(key=lambda x: x["val"])

    last_y = 0
    spacing_factor = 1.1 

    for item in labels_to_plot:
        val = item["val"]
        color = item["color"]
        user = item["user"]

        text_y = max(val, last_y * spacing_factor)
        last_y = text_y
        ax.text(
            1.02, text_y, 
            user, 
            color=color, 
            transform=ax.get_yaxis_transform(),
            va='center',
            weight='bold',
            fontsize=10
        )

    ax.set_yscale('log')
    ax.set_xlabel('Dates')
    ax.set_ylabel('Cumulative Users')
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    plt.subplots_adjust(right=0.85) 

    plt.tight_layout()
    plt.savefig(OUT_DIR + "users_daily_cropped.svg")
    plt.close()

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    users = {}
    with open(STAT_DIR + "users_total.json", 'r') as f:
        users = json.loads(f.read())
        users_total(users)

    users = set(users.keys())
    with open(STAT_DIR + "users_daily.json", 'r') as f:
        users_daily(json.loads(f.read()), users)

    with open(STAT_DIR + "users_daily.json", 'r') as f:
        users_daily_cropped(json.loads(f.read()), users)

    with open(STAT_DIR + "tags_total.json", 'r') as f:
        tags_total(json.loads(f.read()))