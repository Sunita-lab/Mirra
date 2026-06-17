import re


def detect_claims(text):
    claims = []

    # Numerical claims
    percentage_pattern = r"\d+%"
    number_pattern = r"\d+(?:,\d+)?"

    if re.search(percentage_pattern, text):
        claims.append("percentage_claim")

    if re.search(number_pattern, text):
        claims.append("numerical_claim")

    # Authority references
    authority_terms = [
        "who",
        "un",
        "government",
        "study",
        "research",
        "report",
        "survey",
        "experts"
        , "scientists",
        "researchers"
    ]

    text_lower = text.lower()

    for term in authority_terms:
        pattern = rf"\b{re.escape(term)}\b"

        if re.search(pattern, text_lower):
            claims.append("authority_claim")
            break
    return {
        "claim_detected": len(claims) > 0,
        "claim_types": list(set(claims))
    }

if __name__ == "__main__":

    test_1 = """
    A WHO study found that infections decreased by 40%.
    """

    test_2 = """
    I think this policy is unfair.
    """

    print("Test 1:")
    print(detect_claims(test_1))

    print("\nTest 2:")
    print(detect_claims(test_2))