from datetime import datetime

from models import db


class Verification(db.Model):

    __tablename__ = "verifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id"),
        nullable=True
    )

    verification_type = db.Column(
        db.String(100),
        nullable=False
    )

    extracted_data = db.Column(
        db.Text,
        nullable=True
    )

    result = db.Column(
        db.String(50),
        default="Pending"
    )

    remarks = db.Column(
        db.Text,
        nullable=True
    )

    verified_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Verification "
            f"{self.id} - {self.result}>"
        )