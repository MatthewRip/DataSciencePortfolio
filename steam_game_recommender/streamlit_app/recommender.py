# import model
import pickle
# process text
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# metrics
from sklearn.metrics.pairwise import cosine_similarity
# data analysis
import pandas as pd


# import data
# df = pd.read_csv('resources/data/data.csv')
# df.dropna(inplace=True)

# 
def remove_punctuation(tags):
    # list to string
    tags = ','.join([str(tag) for tag in tags])
    return tags.replace('[', '').replace(']', '').replace("'", '')

# tokenizer
def tokenizer(str_input):
    # split string on comma/remove white spaces
    tags = str_input.lower().split(',')
    return [tag.strip() for tag in tags if tag != '']


# if game is unknown
def preprocessing():
    """



    """

    return None


#########  title based recommendation  ##########

def title_recommendation(feature_sense, game, top_n=10):
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

    max_features = {0: None, 1: 200, 2: 100, 3: 50, 4: 25, 5: 10}

    cosine_sim_scores = []
    count_vec = CountVectorizer(
        tokenizer=tokenizer, max_features=max_features.get(feature_sense))

    # get cluster number
    cluster = df[df['title'] == game]['cluster'].values[0]
    # drop other clusters
    subsection = df[df['cluster'] == cluster]
    # reset indexs
    subsection.reset_index(drop=True, inplace=True)
    # index of game we are comparing
    index = subsection[subsection['title'] == game].index[0]
    # list of features to compare game apon
    X = count_vec.fit_transform(subsection.tags).toarray()
    # calculate cosine_similarity
    for i in X:
        score = cosine_similarity([i], [X[index]])
        cosine_sim_scores.append(score[0][0])

    subsection['score'] = cosine_sim_scores
    subsection = subsection.sort_values('score', ascending=False)

    return subsection[1:top_n + 1]

#########  for url based recommendation  ##########


def determine_cluster(tags):
    UTILS_PATH = 'resources/ults/'
    # tfidfvectorizer
    tfidf = pickle.load(open(UTILS_PATH + 'tfidf.pkl', 'rb'))
    # dimensionality reduction
    pca = pickle.load(open(UTILS_PATH + 'pca.pkl', 'rb'))
    # kmeans model
    model = pickle.load(open(UTILS_PATH + 'model.pkl', 'rb'))

    # list comes in as x amount of elements and we have to chage it to be a list of 1
    tags = remove_punctuation(tags)
    tags = [tags]

    matrix = tfidf.transform(tags).toarray()
    X = pca.transform(matrix)
    cluster = model.predict(X)

    return cluster[0]


def url_recommendation(game, tags, cluster, feature_sense, top_n=10):
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
    max_features = {0: None, 1: 200, 2: 100, 3: 50, 4: 25, 5: 10}

    cosine_sim_scores = []
    count_vec = CountVectorizer(
        tokenizer=tokenizer, max_features=max_features.get(feature_sense))

    # debugging
    # print(len(tags))
    # print(tags)

    tags = remove_punctuation(tags)
    tags = [tags]

    # drop other clusters
    subsection = df[df['cluster'] == cluster]
    # it has a bug where subsection returns an empty dataframe
    if subsection.empty:
        subsection = df[(df.cluster > cluster - 1) &
                        (df.cluster < cluster + 1)]
    # reset indexs
    subsection.reset_index(drop=True, inplace=True)
    # list of features to compare game apon
    X = count_vec.fit_transform(subsection.tags).toarray()
    new_title = count_vec.transform(tags).toarray()
    # calculate cosine_similarity

    for i in X:
        score = cosine_similarity([i], new_title)
        cosine_sim_scores.append(score[0][0])

    subsection['score'] = cosine_sim_scores
    subsection = subsection.sort_values('score', ascending=False)
    subsection.drop_duplicates(keep=False, inplace=True)
    return subsection[0:top_n]
