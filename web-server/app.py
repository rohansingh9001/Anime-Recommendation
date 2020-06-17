# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import json
import random
import itertools
from utils import *


# Loading The Model in !!!
global reversed_movies_dict, item_item_dist, item_item_recommendation, movies_dict
colnames=['userId', 'animeId', 'rating'] 
df = pd.read_csv("main.txt",delimiter=' ', names=colnames, header=None)

interactions = create_interaction_matrix(df, 'userId', 'animeId', 'rating')

user_dict = create_user_dict(interactions=interactions)
movies_dict = json.load(open('anime_id_to_name.json'))
reversed_movies_dict = json.load(open('anime_name_to_id.json'))

mf_model = runMF(interactions = interactions,
                n_components = 30,
                loss = 'warp',
                epoch = 30,
                n_jobs = 4)  

item_item_dist = create_item_emdedding_distance_matrix(model = mf_model,interactions = interactions)
print("Model Loaded")


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/suggest', methods=['POST'])
def predict():

    try:

        list_watched = request.json["animes"]
        
        suggestions = []

        for anime in list_watched:
            id = int(reversed_movies_dict[anime])
            rec_list = item_item_recommendation(item_emdedding_distance_matrix = item_item_dist,
                                                item_id = id,
                                                item_dict = movies_dict,
                                                n_items = 10)
            # print(rec_list)
            suggestions.append(rec_list)
        
        suggestions = list(set(itertools.chain.from_iterable(suggestions)))

        random.shuffle(suggestions)

        return jsonify({'suggestions': suggestions, 'error': None})
    
    except Exception as e:

        print("SomeThing Went Wrong",e)

        return jsonify({'suggestions': None,'error': 'Something Went Wrong'})                   

if __name__ == '__main__':
    
    app.run()