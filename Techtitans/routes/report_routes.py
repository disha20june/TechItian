from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    request
)

from models import db
from models.application import Application
from models.document import Document


# Create report blueprint
report_bp = Blueprint(
    "report_routes",
    __name__,
    url_prefix="/reports"
)


# =========================================================
# VIEW APPLICATION REPORTS
# =========================================================

@report_bp.route("/application/<int:application_id>")
def view_reports(application_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    application_data = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first()

    if not application_data:
        flash("Application not found.", "danger")
        return redirect(url_for("citizen_dashboard"))

    documents = Document.query.filter_by(
        application_id=application_id
    ).all()

    return render_template(
        "reports.html",
        application=application_data,
        documents=documents
    )


# =========================================================
# REPORT SUMMARY
# =========================================================

@report_bp.route("/application/<int:application_id>/summary")
def report_summary(application_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    application_data = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first()

    if not application_data:
        flash("Application not found.", "danger")
        return redirect(url_for("citizen_dashboard"))

    documents = Document.query.filter_by(
        application_id=application_id
    ).all()

    return render_template(
        "report_summary.html",
        application=application_data,
        documents=documents
    )