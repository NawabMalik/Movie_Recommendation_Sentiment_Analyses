# Movie_Recommendation_with_Sentiment_Analyses
The Movies details like Title, posters, rating, genres etc. has been fetched from TMDB website "https://www.themoviedb.org/documentation/api", using TMDB API. The Movies reviews has been retrieved through Webscraping from TMDB website using the IMDB ID of movies in API and I performed sentiments Analyses on the reviews given by user for that movie.
You please go through the application on Heroku cloud: "https://movie-recommendation-sentiment.herokuapp.com/"

How to Run the Application:
Click on the above link
Type the movie name on search box and press enter, it will displayed the searched movie information like Actor and Actress with their information, movie rating and reviewes given by users and i performed sentiments Analyses on these reviews with either "Good" or "BAD", also below you will see all recommended movies similar to the movie you seached

How to get an API key form TBMD website?
Create your account on TMDB website "https://www.themoviedb.org/", click on the API link from the left hand sidebar in your account settings and fill all the details to apply for API key. If you are asked for the website URL, just give "NA" if you don't have one. You will see the API key in your API sidebar once your request is approved.

How to run this project?
Clone this repository to your local machine.
Install all the libraries mentioned in the requirements.txt file
Replace YOUR_API_KEY in two lines 15 & 29 in recommend.js file present in static folder .
Open your terminal/command prompt from your project directory and run the file app.py .
Go to your browser and type http://127.0.0.1:5000/ in the address bar.
Hurray! That's it.


Similarity Score :
Similar score basically used to determine the item which is most similary to the item user have searched or user likes. that's why i used similarity score here.

It is a numerical value ranges between zero to one which helps to determine how much two items are similar to each other on a scale of zero to one. This similarity score is obtained measuring the similarity between the text details of both of the items. So, similarity score is the measure of similarity between given text details of two items. This can be done by cosine-similarity.

How does Cosine Similarity work?
Cosine similarity is a metric used to measure how similar the documents are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance (due to the size of the document), chances are they may still be oriented closer together. The smaller the angle, higher the cosine similarity.

image

More about Cosine Similarity : Understanding the Math behind Cosine Similarity


