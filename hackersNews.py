import requests

#get all top stories ID
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
reponse = requests.get(url)
story_id = reponse.json()

#grab the storyIDs

for i in range(5):
    current_story_id = story_id[i]

    #find first story info
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{current_story_id}.json"
    story_data = requests.get(item_url).json() 

    #print
    print(i+1,f"------------------------")
    print(f"Top story is: {story_data["title"]}")
    print(f"Author: {story_data["by"]}")
    print(f"Points: {story_data["score"]}")
    #print(f"Link: {story_data.get("url", "no url")}")
