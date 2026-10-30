from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User


# Create authentication blueprint
auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =========================================================
# REGISTER
# =========================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # Validate fields
        if not full_name or not email or not password:
            flash(
                "Please fill all required fields.",
                "danger"
            )
            return redirect(url_for("auth.register"))

        # Check password confirmation
        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "danger"
            )
            return redirect(url_for("auth.register"))

        # Check existing user
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            flash(
                "Email already registered.",
                "warning"
            )
            return redirect(url_for("auth.register"))

        # Hash password
        hashed_password = generate_password_hash(
            password
        )

        # Create user
        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            role="citizen"
        )

        db.session.add(new_user)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        # Check login details
        if user and check_password_hash(
            user.password,
            password
        ):

            session["user_id"] = user.id
            session["user_name"] = user.full_name
            session["role"] = user.role

            flash(
                "Welcome back!",
                "success"
            )

            return redirect(
                url_for("citizen_dashboard")
            )

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )