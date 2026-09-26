def calculate_second_life_score(
    soh,
    rul_years,
):
    """
    Calculate a prototype second-life suitability score.

    The score combines:
        - State of Health (SoH)
        - Remaining Useful Life (RUL)

    Returns a score from 0 to 100.
    """

    if soh < 0 or soh > 100:
        raise ValueError(
            "SoH must be between 0 and 100."
        )

    if rul_years < 0:
        raise ValueError(
            "RUL cannot be negative."
        )

    # SoH contributes 60% of the score.
    health_score = soh

    # RUL is normalized against a 10-year reference.
    rul_score = min(
        (rul_years / 10.0) * 100,
        100.0,
    )

    score = (
        0.6 * health_score
        + 0.4 * rul_score
    )

    return round(score, 2)


def classify_second_life_suitability(score):
    """
    Classify second-life suitability.
    """

    if score >= 70:
        return "Highly Suitable"

    if score >= 50:
        return "Suitable"

    if score >= 30:
        return "Marginal"

    return "Not Suitable"


def recommend_second_life_application(
    score,
    soh,
):
    """
    Recommend a potential second-life application.

    This is a prototype recommendation and is not
    a safety certification.
    """

    if score < 30 or soh < 40:
        return "Not Recommended"

    if score >= 70 and soh >= 70:
        return "Stationary Energy Storage"

    if score >= 50 and soh >= 60:
        return "Backup Power"

    return "Low-Demand Energy Storage"