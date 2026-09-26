def generate_battery_report(
    soh,
    health_class,
    rul_years,
    residual_value,
    value_retention,
    second_life_score,
    second_life_suitability,
    recommended_application,
):
    """
    Generate a consolidated battery assessment report.

    This returns structured report data that can later
    be used by the Reports UI or exported to PDF.
    """

    return {
        "battery_health": {
            "soh": round(soh, 2),
            "classification": health_class,
        },
        "remaining_useful_life": {
            "years": round(rul_years, 2),
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
        },
        "second_life": {
            "score": round(
                second_life_score,
                2,
            ),
            "suitability": second_life_suitability,
            "recommended_application": (
                recommended_application
            ),
        },
    }


def create_report_summary(report):
    """
    Create a short human-readable summary
    from a generated battery report.
    """

    health = report["battery_health"]
    rul = report["remaining_useful_life"]
    valuation = report["valuation"]
    second_life = report["second_life"]

    return (
        f"SoH: {health['soh']:.2f}% "
        f"({health['classification']})\n"
        f"RUL: {rul['years']:.2f} years\n"
        f"Residual Value: "
        f"{valuation['residual_value']:.2f}\n"
        f"Value Retention: "
        f"{valuation['value_retention']:.2f}%\n"
        f"Second-Life Score: "
        f"{second_life['score']:.2f}/100\n"
        f"Second-Life Suitability: "
        f"{second_life['suitability']}\n"
        f"Recommended Application: "
        f"{second_life['recommended_application']}"
    )