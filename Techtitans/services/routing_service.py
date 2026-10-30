def route_application(service_name):
    """
    Application ko service ke basis par suitable department
    assign karta hai.
    """

    if not service_name:
        return {
            "department": "General Department",
            "priority": "Normal",
            "message": "Service information missing hai."
        }

    service = service_name.lower()

    # Education-related applications
    if any(word in service for word in [
        "scholarship",
        "education",
        "student",
        "school",
        "college"
    ]):
        department = "Education Department"

    # Health-related applications
    elif any(word in service for word in [
        "health",
        "medical",
        "hospital",
        "medicine"
    ]):
        department = "Health Department"

    # Agriculture-related applications
    elif any(word in service for word in [
        "agriculture",
        "farmer",
        "crop",
        " खेती",
        "kisan"
    ]):
        department = "Agriculture Department"

    # Transport-related applications
    elif any(word in service for word in [
        "driving",
        "vehicle",
        "transport",
        "license",
        "licence"
    ]):
        department = "Transport Department"

    # Identity-related applications
    elif any(word in service for word in [
        "aadhaar",
        "identity",
        "certificate",
        "birth",
        "death"
    ]):
        department = "Citizen Services Department"

    # Income and financial applications
    elif any(word in service for word in [
        "income",
        "pension",
        "financial",
        "bank",
        "ration"
    ]):
        department = "Social Welfare Department"

    else:
        department = "General Department"

    return {
        "department": department,
        "priority": "Normal",
        "message": (
            "Application successfully routed to "
            + department
        )
    }