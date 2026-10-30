from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    flash,
    send_file
)

from models.document import Document
from models.application import Application


# Create document blueprint
document_bp = Blueprint(
    "document_routes",
    __name__,
    url_prefix="/documents"
)


# =========================================================
# VIEW DOCUMENTS OF AN APPLICATION
# =========================================================

@document_bp.route("/application/<int:application_id>")
def application_documents(application_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Check that application belongs to logged-in user
    application_data = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first_or_404()

    # Get documents of this application
    documents = Document.query.filter_by(
        application_id=application_data.id
    ).all()

    return render_template(
        "application_documents.html",
        application=application_data,
        documents=documents
    )


# =========================================================
# DOWNLOAD DOCUMENT
# =========================================================

@document_bp.route("/download/<int:document_id>")
def download_document(document_id):

    # Check login
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))

    # Find document
    document = Document.query.get_or_404(document_id)

    # Check related application
    application_data = Application.query.filter_by(
        id=document.application_id,
        user_id=session["user_id"]
    ).first_or_404()

    # Send document file
    return send_file(
        document.file_path,
        as_attachment=True,
        download_name=document.filename
    )