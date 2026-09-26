class BatteryData:
    """
    Shared battery data used across PowerPulse modules.
    """

    def __init__(
        self,
        rated_capacity,
        current_capacity,
        battery_age_years,
        original_value,
    ):
        if rated_capacity <= 0:
            raise ValueError(
                "Rated capacity must be greater than zero."
            )

        if current_capacity < 0:
            raise ValueError(
                "Current capacity cannot be negative."
            )

        if current_capacity > rated_capacity:
            raise ValueError(
                "Current capacity cannot be greater "
                "than rated capacity."
            )

        if battery_age_years < 0:
            raise ValueError(
                "Battery age cannot be negative."
            )

        if original_value < 0:
            raise ValueError(
                "Original value cannot be negative."
            )

        self.rated_capacity = rated_capacity
        self.current_capacity = current_capacity
        self.battery_age_years = battery_age_years
        self.original_value = original_value

    def to_dict(self):
        """
        Return battery data as a dictionary.
        """

        return {
            "rated_capacity": self.rated_capacity,
            "current_capacity": self.current_capacity,
            "battery_age_years": self.battery_age_years,
            "original_value": self.original_value,
        }


def calculate_soh(
    rated_capacity,
    current_capacity,
):
    """
    Calculate Battery State of Health (SoH).

    SoH = (Current Capacity / Rated Capacity) × 100
    """

    if rated_capacity <= 0:
        raise ValueError(
            "Rated capacity must be greater than zero."
        )

    if current_capacity < 0:
        raise ValueError(
            "Current capacity cannot be negative."
        )

    if current_capacity > rated_capacity:
        raise ValueError(
            "Current capacity cannot be greater than "
            "rated capacity."
        )

    soh = (
        current_capacity
        / rated_capacity
    ) * 100

    return soh


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


def calculate_capacity_degradation(
    rated_capacity,
    current_capacity,
):
    """
    Calculate total capacity degradation.

    This represents capacity already lost relative
    to the original rated capacity.

    It is NOT an annual degradation rate.
    """

    if rated_capacity <= 0:
        raise ValueError(
            "Rated capacity must be greater than zero."
        )

    if current_capacity < 0:
        raise ValueError(
            "Current capacity cannot be negative."
        )

    if current_capacity > rated_capacity:
        raise ValueError(
            "Current capacity cannot be greater than "
            "rated capacity."
        )

    degradation = (
        (
            rated_capacity
            - current_capacity
        )
        / rated_capacity
    ) * 100

    return degradation