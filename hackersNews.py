import requests

#get all top stories ID
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
reponse = requests.get(top_stories_url)
story_id = reponse.json()

#grab the first storyID
first_story_id = story_id[0]

#find first story info
item_url = f"https://hacker-news.firebaseio.com/v0/item/{first_story_id}.json"
story_data = requests.get(item_url).json() 

#print
print(f"Top story is: {story_data["title"]}")
print(f"Points: {story_data["score"]}")
print(f"Link: {story_data.get("url", "no url")}")