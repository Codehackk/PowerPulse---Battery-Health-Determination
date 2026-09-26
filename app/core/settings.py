APP_VERSION = "1.0.0"
ENVIRONMENT = "Prototype"

DEFAULT_CURRENCY = "INR"

SECOND_LIFE_SCORE_REFERENCE_YEARS = 10.0

SOH_HEALTHY_THRESHOLD = 80.0
SOH_MODERATE_THRESHOLD = 60.0
SOH_DEGRADED_THRESHOLD = 40.0


def get_application_settings():
    """
    Return the current PowerPulse application settings.
    """

    return {
        "app_version": APP_VERSION,
        "environment": ENVIRONMENT,
        "currency": DEFAULT_CURRENCY,
        "second_life_reference_years": (
            SECOND_LIFE_SCORE_REFERENCE_YEARS
        ),
        "soh_thresholds": {
            "healthy": SOH_HEALTHY_THRESHOLD,
            "moderate": SOH_MODERATE_THRESHOLD,
            "degraded": SOH_DEGRADED_THRESHOLD,
        },
    }