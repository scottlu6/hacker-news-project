import requests
import csv
from datetime import datetime, timedelta

#get all top stories ID
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
response = requests.get(url)
story_id = response.json()

#grab dates
current_date = datetime.now().strftime("%Y-%m-%d")
yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

#make dict(hashmap) for o(1) lookup
yesterday_data = {}

#add yesterdays data in dict
with open("data/snapshots/top_stories_" + yesterday_date +".csv", "r") as yesterday_file:
    reader = csv.reader(yesterday_file)
    next(reader) #skip first row

    for row in reader:
        storyID =int(row[1])
        rank = int(row[0])

        yesterday_data[storyID] = rank
    

#add or update ranks
with open("data/snapshots/top_stories_" + current_date + ".csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Story Id", "Title", "Author", "Score", "Rank update"])

    #grab the storyIDs
    for i in range(50):
        current_story_id = story_id[i]

        #find first story info
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_story_id}.json"
        story_data = requests.get(item_url).json() 
        
        rank = i+1
        title = story_data["title"]
        author = story_data["by"]
        score = story_data["score"]

        ##compare to yesterday
        if current_story_id in yesterday_data:
            yesterday_rank = yesterday_data[current_story_id]
            rank_delta = yesterday_rank - rank     #delta is change in math

            if rank_delta > 0:
                rank_delta = f"↑{rank_delta}"
            else:
                rank_delta = f"↓{abs(rank_delta)}"
        else:
            rank_delta = "New!"

        writer.writerow([rank, current_story_id, title, author, score, rank_delta])

        

        