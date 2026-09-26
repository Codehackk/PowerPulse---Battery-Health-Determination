from app.core.battery import (
    BatteryData,
    calculate_soh,
    classify_health,
    calculate_capacity_degradation,
)

from app.core.rul import (
    estimate_rul_years,
    classify_rul,
)

from app.core.valuation import (
    calculate_residual_value,
    calculate_value_retention,
    classify_value_retention,
)

from app.core.second_life import (
    calculate_second_life_score,
    classify_second_life_suitability,
    recommend_second_life_application,
)


def analyze_battery(
    battery,
    annual_degradation_rate,
    minimum_soh=70.0,
    expected_life_years=10.0,
):
    """
    Run the complete PowerPulse battery analysis.

    Parameters
    ----------
    battery : BatteryData
        Shared battery information.

    annual_degradation_rate : float
        Expected annual SoH degradation percentage.

    minimum_soh : float, optional
        Minimum SoH used by the RUL model.
        Default is 70.0%.

    expected_life_years : float, optional
        Expected total battery life used by the
        valuation model.
        Default is 10.0 years.

    Returns
    -------
    dict
        Consolidated battery analysis results.
    """

    # ---------------------------------------------------------
    # Validate battery object
    # ---------------------------------------------------------

    if not isinstance(battery, BatteryData):
        raise TypeError(
            "battery must be a BatteryData instance."
        )

    # ---------------------------------------------------------
    # Validate analysis parameters
    # ---------------------------------------------------------

    if annual_degradation_rate <= 0:
        raise ValueError(
            "Annual degradation rate must be greater than zero."
        )

    if minimum_soh < 0 or minimum_soh >= 100:
        raise ValueError(
            "Minimum SoH must be between 0 and 100."
        )

    if expected_life_years <= 0:
        raise ValueError(
            "Expected battery life must be greater than zero."
        )

    # ---------------------------------------------------------
    # State of Health
    # ---------------------------------------------------------

    soh = calculate_soh(
        battery.rated_capacity,
        battery.current_capacity,
    )

    health_class = classify_health(
        soh
    )

    capacity_degradation = (
        calculate_capacity_degradation(
            battery.rated_capacity,
            battery.current_capacity,
        )
    )

    # ---------------------------------------------------------
    # Remaining Useful Life
    # ---------------------------------------------------------

    rul_years = estimate_rul_years(
        current_soh=soh,
        annual_degradation_rate=(
            annual_degradation_rate
        ),
        minimum_soh=minimum_soh,
    )

    rul_class = classify_rul(
        rul_years
    )

    # ---------------------------------------------------------
    # Valuation
    # ---------------------------------------------------------

    residual_value = calculate_residual_value(
        original_value=battery.original_value,
        current_soh=soh,
        current_rul_years=rul_years,
        expected_life_years=(
            expected_life_years
        ),
    )

    value_retention = calculate_value_retention(
        original_value=battery.original_value,
        residual_value=residual_value,
    )

    value_class = classify_value_retention(
        value_retention
    )

    # ---------------------------------------------------------
    # Second Life
    # ---------------------------------------------------------

    second_life_score = (
        calculate_second_life_score(
            soh=soh,
            rul_years=rul_years,
        )
    )

    second_life_suitability = (
        classify_second_life_suitability(
            second_life_score
        )
    )

    recommended_application = (
        recommend_second_life_application(
            score=second_life_score,
            soh=soh,
        )
    )

    # ---------------------------------------------------------
    # Consolidated result
    # ---------------------------------------------------------

    return {
        "battery": battery.to_dict(),

        "health": {
            "soh": round(
                soh,
                2,
            ),
            "classification": health_class,
            "capacity_degradation": round(
                capacity_degradation,
                2,
            ),
        },

        "rul": {
            "years": round(
                rul_years,
                2,
            ),
            "classification": rul_class,
        },

        "valuation": {
            "residual_value": round(
                residual_value,
                2,
            ),
            "value_retention": round(
                value_retention,
                2,
            ),
            "classification": value_class,
        },

        "second_life": {
            "score": round(
                second_life_score,
                2,
            ),
            "suitability": (
                second_life_suitability
            ),
            "recommended_application": (
                recommended_application
            ),
        },
    }