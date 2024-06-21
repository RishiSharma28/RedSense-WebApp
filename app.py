from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

# Initialize PRAW with your Reddit API credentials
reddit = praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                     client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                     user_agent='my-app by u/Significant_Ad_4786')

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize NLTK's Snowball Stemmer and stopwords
stemmer = SnowballStemmer('english')
stop_words = set(stopwords.words('english'))

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
                words = [stemmer.stem(word) for word in words if word not in stop_words]
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


@app.route('/redditSentiments', methods=[ 'POST'])
def redditSentiments():
    data = request.get_json()
    print(data)
    subreddit_name = data.get('subname')
    num_posts = int(data['posts'])
        
    (positive_sentiments, negative_sentiments, neutral_sentiments,
         top_positive_comment, top_negative_comment, top_neutral_comment) = analyze_and_visualize(subreddit_name, num_posts)

    # print('Top Positive Comment',top_positive_comment)
    # print(top_negative_comment)
    # print(top_neutral_comment)
    print(positive_sentiments)
    print(negative_sentiments)
    print(neutral_sentiments)

    return  jsonify({
        'comments': [top_positive_comment,top_negative_comment,top_neutral_comment],
        'positive_sentiments':positive_sentiments,
        'negative_sentiments':negative_sentiments,
        'neutral_sentiments':neutral_sentiments
    })
                    
if __name__ == '__main__':
    app.run(debug=True)
