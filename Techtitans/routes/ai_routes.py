from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request,
    jsonify
)

from models import db
from models.application import Application


# Create AI blueprint
ai_bp = Blueprint(
    "ai_routes",
    __name__,
    url_prefix="/ai"
)


# =========================================================
# AI ASSISTANT PAGE
# =========================================================

@ai_bp.route("/assistant")
def ai_assistant():

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    return render_template(
        "ai_assistant.html",
        user_name=session.get("user_name", "Citizen")
    )


# =========================================================
# AI APPLICATION ANALYSIS
# =========================================================

@ai_bp.route(
    "/analyze/<int:application_id>",
    methods=["POST"]
)
def analyze_application(application_id):

    # Check login
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    application_data = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first()

    if not application_data:
        return jsonify({
            "success": False,
            "message": "Application not found."
        }), 404

    # Temporary AI response
    # Real AI/OCR logic will be added later
    analysis_result = {
        "application_id": application_data.id,
        "application_number": application_data.application_number,
        "status": application_data.status,
        "risk_level": application_data.risk_level,
        "message": (
            "AI analysis is currently running in demo mode. "
            "The final decision will be made by an authorized officer."
        )
    }

    return jsonify({
        "success": True,
        "analysis": analysis_result
    })


# =========================================================
# AI CHAT API
# =========================================================

@ai_bp.route("/chat", methods=["POST"])
def ai_chat():

    # Check login
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "success": False,
            "message": "Please enter a message."
        }), 400

    # Temporary response
    # Actual AI API integration will be added later
    response_message = (
        "Thank you for your message. "
        "This AI assistant is currently in demo mode. "
        "Please consult an authorized government officer "
        "for the final application decision."
    )

    return jsonify({
        "success": True,
        "user_message": user_message,
        "response": response_message
    })