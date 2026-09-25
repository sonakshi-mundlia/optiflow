class ComplexityService:

    HIGH_KEYWORDS = {
        "derive",
        "proof",
        "architecture",
        "optimize",
        "algorithm",
        "design",
        "analyze",
        "compare",
        "debug",
        "implement",
    }

    MEDIUM_KEYWORDS = {
        "explain",
        "why",
        "how",
        "example",
        "describe",
        "difference",
    }

    def analyze(self, query: str) -> tuple[str, float]:

        text = query.lower()

        high_score = sum(
            word in text
            for word in self.HIGH_KEYWORDS
        )

        medium_score = sum(
            word in text
            for word in self.MEDIUM_KEYWORDS
        )

        if high_score >= 2:
            return "high", 0.85

        if high_score == 1:
            return "high", 0.70

        if medium_score >= 1:
            return "medium", 0.50

        return "low", 0.20