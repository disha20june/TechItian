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
from models.user import User
from models.document import Document


# =========================================================
# OFFICER BLUEPRINT
# =========================================================

officer_bp = Blueprint(
    "officer_routes",
    __name__,
    url_prefix="/officer"
)


# =========================================================
# OFFICER ACCESS CHECK
# =========================================================

def officer_required():

    if "user_id" not in session:

        flash(
            "Please login first.",
            "warning"
        )

        return False

    role = session.get(
        "user_role",
        ""
    ).lower()

    if role not in [
        "officer",
        "admin",
        "super_admin"
    ]:

        return False

    return True


# =========================================================
# OFFICER DASHBOARD
# =========================================================

@officer_bp.route("/dashboard")
def officer_dashboard():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    if not officer_required():

        flash(
            "Officer access required.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # GET APPLICATIONS
    # -----------------------------------------------------

    applications = (
        Application.query
        .order_by(
            Application.created_at.desc()
        )
        .all()
    )


    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    total_applications = (
        Application.query.count()
    )


    pending_applications = (
        Application.query
        .filter_by(
            status="Submitted"
        )
        .count()
    )


    under_review_applications = (
        Application.query
        .filter_by(
            status="Under Review"
        )
        .count()
    )


    reviewed_applications = (
        Application.query
        .filter_by(
            status="Reviewed"
        )
        .count()
    )


    # -----------------------------------------------------
    # RENDER
    # -----------------------------------------------------

    return render_template(

        "officer_dashboard.html",

        applications=applications,

        total_applications=total_applications,

        pending_applications=pending_applications,

        under_review_applications=under_review_applications,

        reviewed_applications=reviewed_applications
    )


# =========================================================
# START APPLICATION REVIEW
# =========================================================

@officer_bp.route(
    "/application/<int:application_id>/review",
    methods=["POST"]
)
def review_application(application_id):

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    if not officer_required():

        flash(
            "Access denied.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # FIND APPLICATION
    # -----------------------------------------------------

    application_data = (
        Application.query
        .get_or_404(application_id)
    )


    # -----------------------------------------------------
    # CHANGE STATUS
    # -----------------------------------------------------

    application_data.status = "Under Review"

    db.session.commit()


    flash(
        "Application is now under review.",
        "success"
    )


    # -----------------------------------------------------
    # IMPORTANT:
    # GO TO OFFICER REVIEW PAGE
    # -----------------------------------------------------

    return redirect(
        url_for(
            "officer_routes.application_review",
            application_id=application_id
        )
    )


# =========================================================
# APPLICATION REVIEW PAGE
# =========================================================

@officer_bp.route(
    "/application/<int:application_id>/review-page",
    methods=["GET"]
)
def application_review(application_id):

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    if not officer_required():

        flash(
            "Access denied.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # GET APPLICATION
    # -----------------------------------------------------

    application_data = (
        Application.query
        .get_or_404(application_id)
    )


    # -----------------------------------------------------
    # GET APPLICANT
    # -----------------------------------------------------

    applicant = User.query.get(
        application_data.user_id
    )


    # -----------------------------------------------------
    # GET DOCUMENTS
    # -----------------------------------------------------

    documents = (
        Document.query
        .filter_by(
            application_id=application_data.id
        )
        .all()
    )


    # -----------------------------------------------------
    # RENDER REVIEW PAGE
    # -----------------------------------------------------

    return render_template(

        "officer_review.html",

        application=application_data,

        applicant=applicant,

        documents=documents
    )


# =========================================================
# COMPLETE APPLICATION REVIEW
# =========================================================

@officer_bp.route(
    "/application/<int:application_id>/complete",
    methods=["POST"]
)
def complete_review(application_id):

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    if not officer_required():

        flash(
            "Access denied.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # FIND APPLICATION
    # -----------------------------------------------------

    application_data = (
        Application.query
        .get_or_404(application_id)
    )


    # -----------------------------------------------------
    # CHANGE STATUS
    # -----------------------------------------------------

    application_data.status = "Reviewed"

    db.session.commit()


    flash(
        "Application review completed.",
        "success"
    )


    return redirect(
        url_for(
            "officer_routes.officer_dashboard"
        )
    )


# =========================================================
# APPROVE APPLICATION
# =========================================================

@officer_bp.route(
    "/application/<int:application_id>/approve",
    methods=["POST"]
)
def approve_application(application_id):

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    if not officer_required():

        flash(
            "Access denied.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # FIND APPLICATION
    # -----------------------------------------------------

    application_data = (
        Application.query
        .get_or_404(application_id)
    )


    # -----------------------------------------------------
    # APPROVE
    # -----------------------------------------------------

    application_data.status = "Approved"

    db.session.commit()


    flash(
        "Application approved successfully.",
        "success"
    )


    return redirect(
        url_for(
            "officer_routes.officer_dashboard"
        )
    )


# =========================================================
# REJECT APPLICATION
# =========================================================

@officer_bp.route(
    "/application/<int:application_id>/reject",
    methods=["POST"]
)
def reject_application(application_id):

    # -----------------------------------------------------
    # ACCESS CHECK
    # -----------------------------------------------------

    if not officer_required():

        flash(
            "Access denied.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # FIND APPLICATION
    # -----------------------------------------------------

    application_data = (
        Application.query
        .get_or_404(application_id)
    )


    # -----------------------------------------------------
    # REJECT
    # -----------------------------------------------------

    application_data.status = "Rejected"

    db.session.commit()


    flash(
        "Application rejected.",
        "warning"
    )


    return redirect(
        url_for(
            "officer_routes.officer_dashboard"
        )
    )