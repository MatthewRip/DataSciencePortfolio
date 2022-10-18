# import model
import pickle
# webscraping
from bs4 import BeautifulSoup as soup
import requests
import json


# process text
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# metrics
from sklearn.metrics.pairwise import cosine_similarity

# model

#
import pandas as pd


# import data
df = pd.read_csv('resources/data/clsutered_df.csv')


# load kmeans model
# model = pickle.load(open('model.plk', 'rb'))

# tokenizer
def tokenizer(str_input):
    tags = str_input.lower().split(',')
    return [tag.strip() for tag in tags if tag != '']



# if game is unknown
def preprocessing():
    """



    """

    return None


def tag_based_recommendation(game, top_n=10):
    """

    Parameters
    ----------
    game : str
        game title entered by user
    top_n : int
        number of recommendations to return
        default return 10 most similar games


    Returns
    -------
    list (str)
        titles of the top-n games recommendations to the user

    """
    cosine_sim_scores = []
    # get cluster number
    cluster = df[df['title'] == game]['cluster'].values[0]
    # drop other clusters
    subsection = df[df['cluster'] == cluster]
    # reset indexs
    subsection.reset_index(drop=True, inplace=True)
    # index of game we are comparing
    index = subsection[subsection['title'] == game].index[0]
    # list of features to compare game apon
    count_vec = CountVectorizer(tokenizer=tokenizer, max_features=None)
    X = count_vec.fit_transform(subsection.tags).toarray()
    # calculate cosine_similarity
    for i in X:
        score = cosine_similarity([i], [X[index]])
        cosine_sim_scores.append(score[0][0])

    subsection['score'] = cosine_sim_scores
    subsection = subsection.sort_values('score', ascending=False)
    
    return subsection[1:11]
