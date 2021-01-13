# importing the libraries:

import pandas as pd
import numpy as np
import flask
from flask import Flask, render_template, request, jsonify, json

from bs4 import BeautifulSoup
import urllib.request
import pickle
import requests
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# let's load the NLP_Model and transform model:
clf=pickle.load(open('NLP_MODEL.pkl','rb'))
vectorizer=pickle.load(open('transform.pkl', 'rb'))

def create_similarity():
    data = pd.read_csv('final.csv')
    cv = CountVectorizer()        # lets create a count and similarity matrix
    count_matrix = cv.fit_transform(data['Combinations'])
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def rcmd(x):
    x = x.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if x not in data['movie_title'].unique():
        return('Sorry! The Movie you requested in not present in our database. Please check the spelling or try other Movies.')
    else:
        i = data.loc[data['movie_title']==x].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda y:y[1] ,reverse=True)
        lst = lst[1:11]               #Excluding the first item as its requested movie itself:
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l
    
#converting string list into list of string variables- "['a','b','c']" into ['a','b','c']
def convert_to_list(my_list):
    my_list = my_list.split('","')
    my_list[0] = my_list[0].replace('["','')
    my_list[-1] = my_list[-1].replace('"]','')
    return my_list

def get_suggestions():
    data = pd.read_csv('final.csv')
    return list(data['movie_title'].str.capitalize())

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    suggestions = get_suggestions()
    return render_template('home.html',suggestions=suggestions)

@app.route("/similarity",methods=["POST"])
def similarity():
    movie = request.form['name']
    rc = rcmd(movie)
    if type(rc)==type('string'):
        return rc
    else:
        m_str="---".join(rc)
        return m_str

@app.route("/recommend",methods=["POST"])
def recommend():
#lets get the data from the requests:
    title = request.form['title']
    cast_ids = request.form['cast_ids']
    cast_names = request.form['cast_names']
    cast_chars = request.form['cast_chars']
    cast_bdays = request.form['cast_bdays']
    cast_bios = request.form['cast_bios']
    cast_places = request.form['cast_places']
    cast_profiles = request.form['cast_profiles']
    imdb_id = request.form['imdb_id']
    poster = request.form['poster']
    genres = request.form['genres']
    overview = request.form['overview']
    vote_average = request.form['rating']
    vote_count = request.form['vote_count']
    release_date = request.form['release_date']
    runtime = request.form['runtime']
    status = request.form['status']
    rec_movies = request.form['rec_movies']
    rec_posters = request.form['rec_posters']

#lets get the movie suggestions for auto complete:
    suggestions = get_suggestions()

#lets call the convert_to_list function for every string that needs to be converted to list
    rec_movies = convert_to_list(rec_movies)
    rec_posters = convert_to_list(rec_posters)
    cast_names = convert_to_list(cast_names)
    cast_chars = convert_to_list(cast_chars)
    cast_profiles = convert_to_list(cast_profiles)
    cast_bdays = convert_to_list(cast_bdays)
    cast_bios = convert_to_list(cast_bios)
    cast_places = convert_to_list(cast_places)
    
#lets convert string to list (eg. "[1,2,3]" to [1,2,3])
    cast_ids = cast_ids.split(',')
    cast_ids[0] = cast_ids[0].replace("[","")
    cast_ids[-1] = cast_ids[-1].replace("]","")
    
# rendering the string to python string
    for i in range(len(cast_bios)):
        cast_bios[i] = cast_bios[i].replace(r'\n', '\n').replace(r'\"','\"')
    
#Combining multiple lists as a dictionary which can be passed to the html file so that it can be processed easily and the order of information will be preserved
    movie_cards = {rec_posters[i]: rec_movies[i] for i in range(len(rec_posters))}
    
    casts = {cast_names[i]:[cast_ids[i], cast_chars[i], cast_profiles[i]] for i in range(len(cast_profiles))}

    cast_details = {cast_names[i]:[cast_ids[i], cast_profiles[i], cast_bdays[i], cast_places[i], cast_bios[i]] for i in range(len(cast_places))}

# lets do Web scraping to get user reviews from IMDB site

    source = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = BeautifulSoup(source,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})

    reviews_list = []                # reviews list
    reviews_status = []              # comments list (Good or Bad)
    for reviews in soup_result:
        if reviews.string:
            reviews_list.append(reviews.string)
            movie_review_list = np.array([reviews.string])  # pass the reviews into our model:
            movie_vector = vectorizer.transform(movie_review_list)  #it converts into vectors
            pred = clf.predict(movie_vector)                         # predict the vectors
            reviews_status.append('Good' if pred else 'Bad')         # if vector 1 (Good) else vector 0 (BAD):

# lets Combine the reviews and comments into a dictionary
    movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     

# lets pass the entire data into html file:
    return render_template('recommend.html',title=title,poster=poster,overview=overview,vote_average=vote_average,
        vote_count=vote_count,release_date=release_date,runtime=runtime,status=status,genres=genres,
        movie_cards=movie_cards,reviews=movie_reviews,casts=casts,cast_details=cast_details)

if __name__ == '__main__':
    app.run(debug=True,)
    