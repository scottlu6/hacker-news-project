import requests
import csv
from datetime import datetime

#get all top stories ID
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
reponse = requests.get(url)
story_id = reponse.json()

current_date = datetime.now().strftime("%Y-%m-%d")

#write into csv ('with' auto closes file)
with open("data/top_stories_" + current_date + ".csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Title", "Author", "Score"])

    #grab the storyIDs
    for i in range(5):
        current_story_id = story_id[i]

        #find first story info
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_story_id}.json"
        story_data = requests.get(item_url).json() 
        
        rank = i+1
        title = story_data["title"]
        author = story_data["by"]
        score = story_data["score"]

        writer.writerow([rank, title, author, score])


        #print
        print(i+1,f"------------------------")
        print(f"Top story is: ", title)
        print(f"Author: ", author)
        print(f"Points: ", score)