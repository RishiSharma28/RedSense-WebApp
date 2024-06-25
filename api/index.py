import os
import logging
import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('punkt')

from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string

# Load environment variables from .env file
load_dotenv()

DEBUG = os.environ.get('FLASK_ENV') == 'development'
logging.basicConfig(level=logging.INFO)

nltk.data.path.append(os.path.join(os.getcwd(),'nltk_data'))

app = Flask(__name__, template_folder='../templates',static_folder='../static',
            static_url_path='/static')
app.config['DEBUG'] = DEBUG
CORS(app)


# Initialize PRAW with your Reddit API credentials
reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
                     client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                     user_agent='my-app by u/Significant_Ad_4786')

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize NLTK's Snowball Stemmer and stopwords
stemmer = SnowballStemmer('english')

# Predefined list of stopwords
STOP_WORDS = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
])

# Function to perform sentiment analysis and visualization
def analyze_and_visualize(subreddit_name, num_posts):
    positive_sentiments = []
    negative_sentiments = []
    neutral_sentiments = []
    top_positive_comment = ""
    top_negative_comment = ""
    top_neutral_comment = ""

    for submission in reddit.subreddit(subreddit_name).new(limit=num_posts):
        total_sentiment = 0
        total_comments = 0
        positive_comments = []
        negative_comments = []
        neutral_comments = []

        for comment in submission.comments:
            if isinstance(comment, praw.models.Comment):
                comment_text = comment.body.lower()
                comment_text = comment_text.translate(str.maketrans('', '', string.punctuation))
                words = nltk.word_tokenize(comment_text)
                words = [stemmer.stem(word) for word in words if word not in STOP_WORDS]
                cleaned_comment = ' '.join(words)

                sentiment = analyzer.polarity_scores(cleaned_comment)
                total_sentiment += sentiment['compound']
                total_comments += 1

                if sentiment['compound'] >= 0.05:
                    positive_comments.append(comment.body)
                elif sentiment['compound'] <= -0.05:
                    negative_comments.append(comment.body)
                else:
                    neutral_comments.append(comment.body)

        if total_comments > 0:
            average_sentiment = total_sentiment / total_comments
            if average_sentiment >= 0.05:
                positive_sentiments.append(average_sentiment)
                top_positive_comment = get_top_comment(positive_comments, sentiment['compound'])
            elif average_sentiment <= -0.05:
                negative_sentiments.append(average_sentiment)
                top_negative_comment = get_top_comment(negative_comments, sentiment['compound'])
            else:
                neutral_sentiments.append(average_sentiment)
                top_neutral_comment = get_top_comment(neutral_comments, sentiment['compound'])

    return (positive_sentiments, negative_sentiments, neutral_sentiments,
            top_positive_comment, top_negative_comment, top_neutral_comment)


# Function to get the top comment for each sentiment
def get_top_comment(comments, sentiment):
    if not comments:
        return "No comments in this category."

    # Find the comment with the highest positive or negative sentiment
    top_comment = max(comments, key=lambda x: analyzer.polarity_scores(x)["compound"])

    return top_comment


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/api/redditSentiments', methods=[ 'POST'])
def redditSentiments():
    data = request.get_json()
    logging.info(f"Received data: {data}")
    print(data)
    subreddit_name = data.get('subname')
    num_posts = int(data['posts'])
        
    (positive_sentiments, negative_sentiments, neutral_sentiments,
         top_positive_comment, top_negative_comment, top_neutral_comment) = analyze_and_visualize(subreddit_name, num_posts)

    return  jsonify({
        'comments': [top_positive_comment,top_negative_comment,top_neutral_comment],
        'positive_sentiments':positive_sentiments,
        'negative_sentiments':negative_sentiments,
        'neutral_sentiments':neutral_sentiments
    })
                   
# Used for running the app locally and in production
if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        port = int(os.environ.get('PORT', 5000))
        app.run(port=port, debug=True)
    else:
        # This branch will be used when deploying to Vercel
        app.run()

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(port=port,debug=True)