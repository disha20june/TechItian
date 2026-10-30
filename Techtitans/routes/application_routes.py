from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models import db
from models.application import Application


# Create application blueprint
application_bp = Blueprint(
    "application_routes",
    __name__,
    url_prefix="/applications"
)


# =========================================================
# APPLICATION LIST
# =========================================================

@application_bp.route("/dashboard")
def application_dashboard():

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Get applications of logged-in citizen
    applications = Application.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Application.created_at.desc()
    ).all()

    return render_template(
        "citizen_dashboard.html",
        applications=applications,
        user_name=session.get("user_name", "Citizen")
    )


# =========================================================
# APPLICATION DETAILS
# =========================================================

@application_bp.route("/<int:application_id>")
def application_details(application_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Fetch only the logged-in user's application
    application_data = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template(
        "application_details.html",
        application=application_data
    )


# =========================================================
# TRACK APPLICATION
# =========================================================

@application_bp.route("/track/<string:application_number>")
def track_application(application_number):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    application_data = Application.query.filter_by(
        application_number=application_number,
        user_id=session["user_id"]
    ).first_or_404()

    return render_template(
        "track_application.html",
        application=application_data
    )