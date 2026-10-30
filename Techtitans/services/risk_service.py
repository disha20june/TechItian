def calculate_risk_level(missing_fields, verification_result):
    """
    Missing fields aur verification result ke basis par
    risk level calculate karta hai.
    """

    if missing_fields is None:
        missing_fields = []

    if verification_result == "Fail":
        return {
            "risk_level": "High",
            "risk_score": 90,
            "remarks": "Document verification fail hui hai."
        }

    if verification_result == "Needs Review":
        return {
            "risk_level": "Medium",
            "risk_score": 60,
            "remarks": "Officer review required hai."
        }

    if len(missing_fields) == 0:
        return {
            "risk_level": "Low",
            "risk_score": 10,
            "remarks": "Required information available hai."
        }

    if len(missing_fields) <= 2:
        return {
            "risk_level": "Medium",
            "risk_score": 50,
            "remarks": "Kuch required information missing hai."
        }

    return {
        "risk_level": "High",
        "risk_score": 80,
        "remarks": "Multiple required fields missing hain."
    }