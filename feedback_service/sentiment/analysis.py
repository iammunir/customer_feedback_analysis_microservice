from rake_nltk import Rake
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze(feedback_text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(feedback_text)    
    if sentiment_scores['compound'] >= 0.05:
        sentiment_label = 'Positive'
    elif sentiment_scores['compound'] <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'
    
    return sentiment_label

def extract_keywords(feedback_text, max_keywords=5):
    rake = Rake()
    rake.extract_keywords_from_text(feedback_text)
    ranked_phrases = rake.get_ranked_phrases()
    return ranked_phrases[:max_keywords]
