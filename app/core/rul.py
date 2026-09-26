def estimate_rul_years(
    current_soh,
    annual_degradation_rate,
    minimum_soh=70.0,
):
    """
    Estimate Remaining Useful Life (RUL) in years.

    Simplified linear model:

        RUL = (Current SoH - Minimum SoH)
              / Annual Degradation Rate

    Example:

        Current SoH = 86.7%
        Annual degradation = 2.8%/year
        Minimum SoH = 70%

        RUL = (86.7 - 70) / 2.8
            ≈ 5.96 years
    """

    if current_soh < 0 or current_soh > 100:
        raise ValueError(
            "Current SoH must be between 0 and 100."
        )

    if annual_degradation_rate <= 0:
        raise ValueError(
            "Annual degradation rate must be greater than zero."
        )

    if minimum_soh < 0 or minimum_soh >= 100:
        raise ValueError(
            "Minimum SoH must be between 0 and 100."
        )

    if current_soh <= minimum_soh:
        return 0.0

    rul = (
        current_soh - minimum_soh
    ) / annual_degradation_rate

    return max(rul, 0.0)


def classify_rul(rul_years):
    """
    Classify the estimated remaining useful life.
    """

    if rul_years >= 5:
        return "Long remaining life"

    if rul_years >= 3:
        return "Moderate remaining life"

    if rul_years >= 1:
        return "Limited remaining life"

    return "Near end of useful life"