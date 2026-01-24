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
    

#add and update ranks
with open("data/snapshots/top_stories_" + current_date + ".csv", "w", newline="") as file:

    snapshots = csv.writer(file)
    snapshots.writerow(["Rank", "Story Id", "Title", "Author", "Score", "Rank update", "total_score"])

    #add to history log
    with open("data/hn_history.csv", "a", newline="") as history_file:
        history_writer = csv.writer(history_file)

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

            snapshots.writerow([rank, current_story_id, title, author, score, rank_delta])
            history_writer.writerow([current_date, current_story_id, rank, score, rank_delta])


history_data = {}
with open("data/hn_history.csv", "r") as history_file:
    reader = csv.reader(history_file)

    for row in reader:
        if row[0] == current_date:
            continue

        storyID = int(row[1])
        rank = int(row[2])
        score = 50-rank

        
        if storyID in history_data:
            history_data[storyID] = history_data[storyID] + score
        else:
            history_data[storyID] = score
    
    
    #sort greatest to least, [(id, total_score), (id,ts), (id,ts)...]
    sorted_data = sorted(history_data.items(), key=lambda x: x[1], reverse=True)

    print("Top 10 Stories of all time by weighted lifespan")

    for x in range(10):
        story_id, total_score = sorted_data[x]
        print(f"{x+1} - {story_id} with the score of: {total_score}")
        
#clean codes now
##add story, fixing issue if yestersterdays file doesnt save
        

