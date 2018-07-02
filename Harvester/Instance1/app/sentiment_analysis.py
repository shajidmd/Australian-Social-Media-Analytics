from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalysis(object):

    def get_sentiment(tweet_text):     
        analyzer = SentimentIntensityAnalyzer()
        return analyzer.polarity_scores(tweet_text)
