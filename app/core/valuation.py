def calculate_residual_value(
    original_value,
    current_soh,
    current_rul_years,
    expected_life_years=10.0,
):
    """
    Estimate the current residual value of a battery.

    This is a simplified prototype valuation model.

    The estimate considers:
        1. Original battery value
        2. Current State of Health (SoH)
        3. Remaining Useful Life (RUL)

    The model combines SoH and remaining-life factors.

    Parameters
    ----------
    original_value : float
        Original battery value.

    current_soh : float
        Current State of Health as a percentage.

    current_rul_years : float
        Estimated remaining useful life in years.

    expected_life_years : float
        Expected total battery life in years.

    Returns
    -------
    float
        Estimated current residual value.
    """

    if original_value <= 0:
        raise ValueError(
            "Original battery value must be greater than zero."
        )

    if current_soh < 0 or current_soh > 100:
        raise ValueError(
            "Current SoH must be between 0 and 100."
        )

    if current_rul_years < 0:
        raise ValueError(
            "Remaining useful life cannot be negative."
        )

    if expected_life_years <= 0:
        raise ValueError(
            "Expected battery life must be greater than zero."
        )

    # ---------------------------------------------------------
    # Health factor
    # ---------------------------------------------------------

    health_factor = current_soh / 100.0

    # ---------------------------------------------------------
    # Remaining-life factor
    # ---------------------------------------------------------

    remaining_life_factor = (
        current_rul_years / expected_life_years
    )

    remaining_life_factor = min(
        max(remaining_life_factor, 0.0),
        1.0,
    )

    # ---------------------------------------------------------
    # Combined valuation factor
    # ---------------------------------------------------------

    valuation_factor = (
        0.6 * health_factor
        + 0.4 * remaining_life_factor
    )

    # ---------------------------------------------------------
    # Residual value
    # ---------------------------------------------------------

    residual_value = (
        original_value
        * valuation_factor
    )

    return max(
        residual_value,
        0.0,
    )


def calculate_value_retention(
    original_value,
    residual_value,
):
    """
    Calculate the percentage of original value retained.
    """

    if original_value <= 0:
        raise ValueError(
            "Original battery value must be greater than zero."
        )

    if residual_value < 0:
        raise ValueError(
            "Residual value cannot be negative."
        )

    retention = (
        residual_value
        / original_value
    ) * 100

    return min(
        max(retention, 0.0),
        100.0,
    )


def classify_value_retention(retention):
    """
    Classify the estimated value retention.
    """

    if retention >= 75:
        return "High value retention"

    if retention >= 50:
        return "Moderate value retention"

    if retention >= 25:
        return "Low value retention"

    return "Very low value retention"