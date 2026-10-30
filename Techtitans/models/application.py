from models import db


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    application_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    service = db.Column(
        db.String(100),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Submitted"
    )

    risk_score = db.Column(
        db.Integer,
        default=0
    )

    risk_level = db.Column(
        db.String(20),
        default="Low"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    documents = db.relationship(
        "Document",
        backref="application",
        lazy=True,
        cascade="all, delete-orphan"
    )