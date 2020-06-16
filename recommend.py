import requests
import json

r = requests.get('https://api.jikan.moe/v3/user/rohansingh9001/animelist/all')

user = json.loads(r.text)

for anime in user['anime']:
    print(anime['title'], anime['score'])
