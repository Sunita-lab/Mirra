CLICKBAIT_TERMS = [
    "shocking",
    "exposed",
    "bombshell",
    "you won't believe",
    "breaking",
    "secret",
    "truth they don't want you to know",
    "must see",
    "unbelievable",
    "what happened next",
    "viral",
    "exclusive",
    "urgent",
    "warning"
]


def get_clickbait_score(text):
    text = text.lower()

    matches = 0

    for term in CLICKBAIT_TERMS:
        if term in text:
            matches += 1

    score = min(matches * 15, 100)

    return score

if __name__ == "__main__":
    text = """
    The government released its annual economic report on Monday.
    """

    print(get_clickbait_score(text))