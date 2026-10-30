from services.ai_service import analyze_application_text


def verify_document_text(extracted_text):
    """
    Document ke extracted text ki verification karta hai.
    """

    if not extracted_text or not extracted_text.strip():
        return {
            "success": False,
            "result": "Needs Review",
            "remarks": "Document mein readable text nahi mila."
        }

    analysis = analyze_application_text(
        extracted_text
    )

    if not analysis["success"]:
        return {
            "success": False,
            "result": "Needs Review",
            "remarks": analysis["message"]
        }

    missing_fields = analysis["missing_fields"]

    if len(missing_fields) == 0:
        result = "Pass"
        remarks = "Required information available hai."

    elif len(missing_fields) <= 2:
        result = "Needs Review"
        remarks = (
            "Kuch information missing ho sakti hai: "
            + ", ".join(missing_fields)
        )

    else:
        result = "Fail"
        remarks = (
            "Multiple required fields missing hain: "
            + ", ".join(missing_fields)
        )

    return {
        "success": True,
        "result": result,
        "risk_level": analysis["risk_level"],
        "risk_score": analysis["risk_score"],
        "missing_fields": missing_fields,
        "remarks": remarks
    }