import re


def estimate_quality(
    query: str,
    answer: str
) -> float:

    score = 0.50

    answer_length = len(
        answer.strip()
    )

    if answer_length >= 120:
        score += 0.15

    if answer_length >= 500:
        score += 0.10

    if any(
        symbol in answer
        for symbol in [
            "1.",
            "2.",
            "-",
            "•"
        ]
    ):
        score += 0.05

    if re.search(
        r"[.!?]",
        answer
    ):
        score += 0.05

    if (
        query.lower().strip()
        in answer.lower()
    ):
        score -= 0.05

    if answer_length < 40:
        score -= 0.15

    return round(
        max(
            0.0,
            min(
                1.0,
                score
            )
        ),
        3
    )