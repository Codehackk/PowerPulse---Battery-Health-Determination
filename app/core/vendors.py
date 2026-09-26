class Vendor:
    """
    Represents a vendor in the PowerPulse prototype directory.
    """

    def __init__(
        self,
        name,
        service_type,
        specialization,
        location,
        contact,
        status="Available",
    ):
        self.name = name
        self.service_type = service_type
        self.specialization = specialization
        self.location = location
        self.contact = contact
        self.status = status

    def to_dict(self):
        """
        Convert vendor information into a dictionary.
        """

        return {
            "name": self.name,
            "service_type": self.service_type,
            "specialization": self.specialization,
            "location": self.location,
            "contact": self.contact,
            "status": self.status,
        }


def get_demo_vendors():
    """
    Return prototype/demo vendor records.

    These are demonstration records only and should
    eventually be replaced with verified vendor data.
    """

    return [
        Vendor(
            name="Demo Battery Recycler",
            service_type="Battery Recycling",
            specialization="EV Battery",
            location="Delhi",
            contact="demo-recycler@example.com",
        ),
        Vendor(
            name="Demo Energy Storage",
            service_type="Second-Life Storage",
            specialization="Battery Repurposing",
            location="Mumbai",
            contact="demo-storage@example.com",
        ),
        Vendor(
            name="Demo Battery Service",
            service_type="Battery Diagnostics",
            specialization="EV Battery Health",
            location="Bengaluru",
            contact="demo-service@example.com",
        ),
    ]


def search_vendors(vendors, search_term):
    """
    Search vendors by name, service type,
    specialization, or location.
    """

    if not search_term:
        return vendors

    search_term = search_term.lower().strip()

    return [
        vendor
        for vendor in vendors
        if (
            search_term in vendor.name.lower()
            or search_term in vendor.service_type.lower()
            or search_term in vendor.specialization.lower()
            or search_term in vendor.location.lower()
        )
    ]