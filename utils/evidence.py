EVIDENCE_TERMS = [
    "according to",
    "research",
    "study",
    "survey",
    "report",
    "data",
    "statistics",
    "evidence",
    "analysis",
    "findings",
    "published",
    "journal",
    "source",
    "sources",
    "experts",
    "researchers"
]


def get_evidence_score(text):
    text = text.lower()

    matches = 0

    for term in EVIDENCE_TERMS:
        if term in text:
            matches += 1

    score = min(matches * 10, 100)

    return score

if __name__ == "__main__":
    text = """
    They are hiding the truth from you and nobody wants you to know this.
    """

    print(get_evidence_score(text))