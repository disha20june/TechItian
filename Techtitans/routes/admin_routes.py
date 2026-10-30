from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash
)

from models.application import Application
from models.user import User
from models import db

# Create admin blueprint
admin_bp = Blueprint(
    "admin_routes",
    __name__,
    url_prefix="/admin"
)


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@admin_bp.route("/dashboard")
def admin_dashboard():

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Check admin role
    if session.get("role") not in ["admin", "super_admin"]:
        flash("Access denied. Admin permission required.", "danger")
        return redirect(url_for("citizen_dashboard"))

    # Get all applications
    applications = Application.query.order_by(
        Application.created_at.desc()
    ).all()

    # Get total users
    total_users = User.query.count()

    # Application statistics
    total_applications = Application.query.count()

    pending_applications = Application.query.filter_by(
        status="Submitted"
    ).count()

    reviewed_applications = Application.query.filter_by(
        status="Reviewed"
    ).count()

    approved_applications = Application.query.filter_by(
        status="Approved"
    ).count()

    rejected_applications = Application.query.filter_by(
        status="Rejected"
    ).count()

    return render_template(
        "admin_dashboard.html",
        applications=applications,
        total_users=total_users,
        total_applications=total_applications,
        pending_applications=pending_applications,
        reviewed_applications=reviewed_applications,
        approved_applications=approved_applications,
        rejected_applications=rejected_applications
    )


# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@admin_bp.route(
    "/application/<int:application_id>/status/<string:new_status>",
    methods=["POST"]
)
def update_application_status(application_id, new_status):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Check admin role
    if session.get("role") not in ["admin", "super_admin"]:
        flash("Access denied.", "danger")
        return redirect(url_for("citizen_dashboard"))

    allowed_statuses = [
        "Submitted",
        "Under Review",
        "Reviewed",
        "Approved",
        "Rejected"
    ]

    if new_status not in allowed_statuses:
        flash("Invalid application status.", "danger")
        return redirect(url_for("admin_routes.admin_dashboard"))

    application_data = Application.query.get_or_404(
        application_id
    )

    application_data.status = new_status

    db.session.commit()

    flash(
        f"Application status updated to {new_status}.",
        "success"
    )

    return redirect(
        url_for("admin_routes.admin_dashboard")
    )