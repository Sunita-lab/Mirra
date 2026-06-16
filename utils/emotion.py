from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def get_emotion_score(text):
    scores = analyzer.polarity_scores(text)

    compound = abs(scores["compound"])

    emotion_score = round(compound * 100, 2)

    return emotion_score

if __name__ == "__main__":
    text = """
    The government released its annual economic report on Monday.
    """

    print(get_emotion_score(text))

