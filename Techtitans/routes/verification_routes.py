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
from models.verification import Verification


# Create verification blueprint
verification_bp = Blueprint(
    "verification_routes",
    __name__,
    url_prefix="/verification"
)


# =========================================================
# VIEW APPLICATION VERIFICATIONS
# =========================================================

@verification_bp.route("/application/<int:application_id>")
def view_verifications(application_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Check officer/admin role
    if session.get("role") not in [
        "officer",
        "admin",
        "super_admin"
    ]:
        flash("Access denied.", "danger")
        return redirect(url_for("citizen_dashboard"))

    application_data = Application.query.get_or_404(
        application_id
    )

    verifications = Verification.query.filter_by(
        application_id=application_id
    ).order_by(
        Verification.created_at.desc()
    ).all()

    return render_template(
        "verification.html",
        application=application_data,
        verifications=verifications
    )


# =========================================================
# ADD VERIFICATION RESULT
# =========================================================

@verification_bp.route(
    "/application/<int:application_id>/add",
    methods=["POST"]
)
def add_verification(application_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Check officer/admin role
    if session.get("role") not in [
        "officer",
        "admin",
        "super_admin"
    ]:
        flash("Access denied.", "danger")
        return redirect(url_for("citizen_dashboard"))

    application_data = Application.query.get_or_404(
        application_id
    )

    verification_type = request.form.get(
        "verification_type"
    )

    extracted_data = request.form.get(
        "extracted_data"
    )

    result = request.form.get(
        "result"
    )

    remarks = request.form.get(
        "remarks"
    )

    if not verification_type or not result:
        flash(
            "Verification type and result are required.",
            "danger"
        )

        return redirect(
            url_for(
                "verification_routes.view_verifications",
                application_id=application_id
            )
        )

    new_verification = Verification(
        application_id=application_data.id,
        verification_type=verification_type,
        extracted_data=extracted_data,
        result=result,
        remarks=remarks,
        verified_by=session["user_id"]
    )

    db.session.add(new_verification)
    db.session.commit()

    flash(
        "Verification result added successfully.",
        "success"
    )

    return redirect(
        url_for(
            "verification_routes.view_verifications",
            application_id=application_id
        )
    )