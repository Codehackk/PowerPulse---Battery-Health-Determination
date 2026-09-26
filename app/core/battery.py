def calculate_soh(rated_capacity, current_capacity):
    """
    Calculate Battery State of Health (SoH).

    SoH = (Current Capacity / Rated Capacity) × 100
    """

    if rated_capacity <= 0:
        raise ValueError("Rated capacity must be greater than zero.")

    if current_capacity < 0:
        raise ValueError("Current capacity cannot be negative.")

    soh = (current_capacity / rated_capacity) * 100

    # Keep the result within a practical percentage range.
    return min(soh, 100.0)


def classify_health(soh):
    """
    Classify battery health based on State of Health.
    """

    if soh >= 80:
        return "Healthy"

    if soh >= 60:
        return "Moderate"

    if soh >= 40:
        return "Degraded"

    return "Critical"


def calculate_degradation(rated_capacity, current_capacity):
    """
    Calculate capacity degradation percentage.
    """

    if rated_capacity <= 0:
        raise ValueError("Rated capacity must be greater than zero.")

    degradation = (
        (rated_capacity - current_capacity)
        / rated_capacity
    ) * 100

    return max(degradation, 0.0)