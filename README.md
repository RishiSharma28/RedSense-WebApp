
# RedSense: Real-Time Reddit Sentiment Analyzer

RedSense is a powerful web application that provides real-time sentiment analysis of Reddit discussions. By leveraging advanced natural language processing (NLP) techniques, RedSense offers valuable insights into the collective opinions within any public subreddit.

## Live Demo
Experience RedSense in action: [RedSense Live Demo](https://red-sense-web-app.vercel.app)

## Key Features

- *Effortless Sentiment Analysis*: Simply enter a subreddit name and specify the number of posts to analyze. RedSense processes Reddit comments using sophisticated algorithms to determine overall sentiment (positive, negative, or neutral).
- *Interactive Visualizations*: Gain clear insights through dynamic charts powered by Chart.js, presenting sentiment distribution in an easily digestible format.
- *Top Comment Showcase*: Explore the most representative voices within the subreddit. RedSense highlights top positive, negative, and neutral comments, offering a nuanced view of diverse perspectives.
- *Real-Time Insights*: Get up-to-the-minute sentiment snapshots, ensuring you're always in tune with the latest Reddit discussions.
- *Advanced NLP Techniques*: Utilizes the Snowball stemmer for precise word processing, enhancing the accuracy of sentiment analysis.

## Technical Stack

- *Frontend*: HTML, CSS (Tailwind CSS), JavaScript, Chart.js
- *Backend*: Python (Flask)
- *Deployment*: Vercel (Serverless Functions)
- *Data Source*: Reddit API
- *NLP Libraries*: PRAW, VADER, NLTK

## How It Works

1. Enter your desired subreddit name.
2. Specify the number of posts to analyze (consider Reddit API limitations for optimal performance).
3. Click "Explore" to receive comprehensive sentiment insights.
4. Explore the generated charts and representative comments to understand the subreddit's sentiment landscape.

## Limitations

- The free tier of the Reddit API imposes restrictions on the number of posts that can be analyzed. Larger sample sizes generally provide more accurate results but may be limited by API constraints.
- RedSense is designed to analyze public subreddits only.

## Future Enhancements

- Implement sentiment analysis for specific keywords within comments.
- Introduce user authentication for personalized experiences and saved preferences.
- Develop functionality to track and visualize sentiment trends over time.

## Development
RedSense is built with a focus on modularity and scalability:

- The Flask backend is hosted as a serverless function on Vercel, ensuring efficient processing and deployment.
- NLP processing is handled through a combination of PRAW for Reddit data retrieval, VADER for sentiment scoring, and NLTK for advanced text processing.

## Contribute
We welcome contributions to RedSense! Whether you're interested in adding new features, improving documentation, or fixing bugs, please feel free to submit pull requests or open issues on our GitHub repository.
