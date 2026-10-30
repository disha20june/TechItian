import re


def analyze_application_text(extracted_text):
    """
    Extracted document text ka basic AI-style analysis karta hai.
    Abhi demo logic hai; real AI API baad mein connect karenge.
    """

    if not extracted_text or not extracted_text.strip():
        return {
            "success": False,
            "message": "No text found for analysis."
        }

    text = extracted_text.lower()

    missing_fields = []

    # Basic required information check
    required_fields = {
        "name": ["name", "applicant"],
        "address": ["address", "village", "city"],
        "phone": ["phone", "mobile", "contact"],
        "identity": ["aadhaar", "identity", "id number"]
    }

    for field, keywords in required_fields.items():

        found = any(
            keyword in text
            for keyword in keywords
        )

        if not found:
            missing_fields.append(field)

    # Simple risk calculation
    if len(missing_fields) == 0:
        risk_level = "Low"
        risk_score = 10

    elif len(missing_fields) <= 2:
        risk_level = "Medium"
        risk_score = 50

    else:
        risk_level = "High"
        risk_score = 80

    # Basic inconsistency check
    has_numbers = bool(
        re.search(r"\d+", extracted_text)
    )

    remarks = []

    if not has_numbers:
        remarks.append(
            "No numeric information detected."
        )

    if missing_fields:
        remarks.append(
            "Some required information may be missing."
        )

    if not remarks:
        remarks.append(
            "Basic document information appears available."
        )

    return {
        "success": True,
        "missing_fields": missing_fields,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "remarks": remarks,
        "message": (
            "Analysis completed. "
            "Final decision must be made by an authorized officer."
        )
    }