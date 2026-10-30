from flask import ( 
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session, 
    flash 
) 
 
from flask_bcrypt import Bcrypt 
from werkzeug.utils import secure_filename 
 
import os 
import uuid 
 
from routes.admin_routes import admin_bp 
from routes.officer_routes import officer_bp 
from routes.verification_routes import verification_bp 
from routes.ai_routes import ai_bp 
from routes.report_routes import report_bp 
from routes.document_routes import document_bp 
 
from config import Config 
 
from models import db 
from models.user import User 
from models.application import Application 
from models.document import Document 
 
 
# ========================================================= 
# APP CONFIGURATION 
# ========================================================= 
 
app = Flask(__name__) 
app.config.from_object(Config) 
 
 
# ========================================================= 
# DATABASE 
# ========================================================= 
 
db.init_app(app) 
 
 
# ========================================================= 
# PASSWORD HASHING 
# ========================================================= 
 
bcrypt = Bcrypt(app) 
 
 
# ========================================================= 
# REGISTER BLUEPRINTS 
# ========================================================= 
 
app.register_blueprint(admin_bp) 
app.register_blueprint(officer_bp) 
app.register_blueprint(verification_bp) 
app.register_blueprint(ai_bp) 
app.register_blueprint(report_bp) 
app.register_blueprint(document_bp) 
 
 
# ========================================================= 
# FILE UPLOAD SETTINGS 
# ========================================================= 
 
ALLOWED_EXTENSIONS = { 
    "pdf", 
    "png", 
    "jpg", 
    "jpeg" 
} 
 
 
def allowed_file(filename): 
 
    return ( 
        "." in filename 
        and filename.rsplit(".", 1)[1].lower() 
        in ALLOWED_EXTENSIONS 
    ) 
 
 
# ========================================================= 
# CREATE DATABASE TABLES 
# ========================================================= 
 
with app.app_context(): 
 
    db.create_all() 
 
    os.makedirs( 
        app.config["UPLOAD_FOLDER"], 
        exist_ok=True 
    ) 
 
 
# ========================================================= 
# HELPER FUNCTIONS 
# ========================================================= 
 
def is_logged_in(): 
 
    return "user_id" in session 
 
 
def current_role(): 
 
    return session.get( 
        "user_role", 
        "" 
    ).lower() 
 
 
def redirect_by_role(): 
 
    """ 
    Redirect user to the correct dashboard 
    according to their role. 
    """ 
 
    role = current_role() 
 
    if role == "officer": 
 
        return redirect( 
            url_for( 
                "officer_routes.officer_dashboard" 
            ) 
        ) 
 
    elif role in [ 
        "admin", 
        "super_admin" 
    ]: 
 
        return redirect( 
            url_for( 
                "admin_routes.admin_dashboard" 
            ) 
        ) 
 
    elif role == "citizen": 
 
        return redirect( 
            url_for( 
                "citizen_dashboard" 
            ) 
        ) 
 
    return redirect( 
        url_for("login") 
    ) 
 
 
# ========================================================= 
# HOME 
# ========================================================= 
 
@app.route("/") 
def home(): 
 
    # User is not logged in 
    if not is_logged_in(): 
 
        return render_template( 
            "login.html" 
        ) 
 
    # User is logged in 
    return redirect_by_role() 
 
 
# ========================================================= 
# REGISTER 
# ========================================================= 
 
@app.route( 
    "/register", 
    methods=["GET", "POST"] 
) 
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
 
        role = request.form.get( 
            "role", 
            "citizen" 
        ).lower() 
 
        department = request.form.get( 
            "department", 
            "" 
        ).strip() 
 
 
        # ------------------------------------------------- 
        # BASIC VALIDATION 
        # ------------------------------------------------- 
 
        if ( 
            not full_name 
            or not email 
            or not password 
            or not confirm_password 
        ): 
 
            flash( 
                "Please fill all required fields.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
        # ------------------------------------------------- 
        # PASSWORD MATCH 
        # ------------------------------------------------- 
 
        if password != confirm_password: 
 
            flash( 
                "Passwords do not match.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
        # ------------------------------------------------- 
        # PASSWORD LENGTH 
        # ------------------------------------------------- 
 
        if len(password) < 8: 
 
            flash( 
                "Password must contain at least 8 characters.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
        # ------------------------------------------------- 
        # VALID ROLE 
        # ------------------------------------------------- 
 
        if role not in [ 
            "citizen", 
            "officer" 
        ]: 
 
            flash( 
                "Invalid role selected.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
        # ------------------------------------------------- 
        # OFFICER DEPARTMENT 
        # ------------------------------------------------- 
 
        if role == "officer" and not department: 
 
            flash( 
                "Please select a department.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
        # ------------------------------------------------- 
        # CHECK EXISTING USER 
        # ------------------------------------------------- 
 
        existing_user = User.query.filter_by( 
            email=email 
        ).first() 
 
        if existing_user: 
 
            flash( 
                "Email already registered. Please login.", 
                "warning" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
        # ------------------------------------------------- 
        # HASH PASSWORD 
        # ------------------------------------------------- 
 
        hashed_password = ( 
            bcrypt 
            .generate_password_hash(password) 
            .decode("utf-8") 
        ) 
 
 
        # ------------------------------------------------- 
        # CREATE USER 
        # ------------------------------------------------- 
 
        new_user = User( 
 
            full_name=full_name, 
 
            email=email, 
 
            password=hashed_password, 
 
            role=role, 
 
            department=( 
                department 
                if role == "officer" 
                else None 
            ) 
        ) 
 
 
        try: 
 
            db.session.add( 
                new_user 
            ) 
 
            db.session.commit() 
 
            flash( 
                "Account created successfully. Please login.", 
                "success" 
            ) 
 
            return redirect( 
                url_for("login") 
            ) 
 
        except Exception as e: 
 
            db.session.rollback() 
 
            print( 
                "Registration Error:", 
                e 
            ) 
 
            flash( 
                "Something went wrong while creating account.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("register") 
            ) 
 
 
    return render_template( 
        "register.html" 
    ) 
 
 
# ========================================================= 
# LOGIN 
# ========================================================= 
 
@app.route( 
    "/login", 
    methods=["GET", "POST"] 
) 
def login(): 
 
    # ----------------------------------------------------- 
    # GET 
    # ----------------------------------------------------- 
 
    if request.method == "GET": 
 
        # If already logged in, go to dashboard 
        if is_logged_in(): 
 
            return redirect_by_role() 
 
        return render_template( 
            "login.html" 
        ) 
 
 
    # ----------------------------------------------------- 
    # POST 
    # ----------------------------------------------------- 
 
    email = request.form.get( 
        "email", 
        "" 
    ).strip().lower() 
 
    password = request.form.get( 
        "password", 
        "" 
    ) 
 
 
    # ----------------------------------------------------- 
    # VALIDATION 
    # ----------------------------------------------------- 
 
    if not email or not password: 
 
        flash( 
            "Please enter email and password.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    # ----------------------------------------------------- 
    # FIND USER 
    # ----------------------------------------------------- 
 
    user = User.query.filter_by( 
        email=email 
    ).first() 
 
 
    if not user: 
 
        flash( 
            "Invalid email or password.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    # ----------------------------------------------------- 
    # CHECK PASSWORD 
    # ----------------------------------------------------- 
 
    if not bcrypt.check_password_hash( 
        user.password, 
        password 
    ): 
 
        flash( 
            "Invalid email or password.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    # ----------------------------------------------------- 
    # CLEAR OLD SESSION 
    # ----------------------------------------------------- 
 
    session.clear() 
 
 
    # ----------------------------------------------------- 
    # CREATE NEW SESSION 
    # ----------------------------------------------------- 
 
    session["user_id"] = user.id 
 
    session["user_name"] = user.full_name 
 
    session["user_role"] = ( 
        user.role.lower() 
    ) 
 
 
    # ----------------------------------------------------- 
    # ROLE BASED REDIRECT 
    # ----------------------------------------------------- 
 
    return redirect_by_role() 
 
 
# ========================================================= 
# CITIZEN DASHBOARD 
# ========================================================= 
 
@app.route( 
    "/citizen/dashboard" 
) 
def citizen_dashboard(): 
 
    # ----------------------------------------------------- 
    # LOGIN CHECK 
    # ----------------------------------------------------- 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    # ----------------------------------------------------- 
    # ROLE CHECK 
    # ----------------------------------------------------- 
 
    if current_role() != "citizen": 
 
        flash( 
            "Access denied. This dashboard is for citizens only.", 
            "danger" 
        ) 
 
        return redirect_by_role() 
 
 
    # ----------------------------------------------------- 
    # FETCH CITIZEN APPLICATIONS 
    # ----------------------------------------------------- 
 
    applications = ( 
        Application.query 
        .filter_by( 
            user_id=session["user_id"] 
        ) 
        .order_by( 
            Application.id.desc() 
        ) 
        .all() 
    ) 
 
 
    # ----------------------------------------------------- 
    # USER NAME 
    # ----------------------------------------------------- 
 
    user_name = session.get( 
        "user_name", 
        "Citizen" 
    ) 
 
 
    # ----------------------------------------------------- 
    # RENDER DASHBOARD 
    # ----------------------------------------------------- 
 
    return render_template( 
 
        "citizen_dashboard.html", 
 
        applications=applications, 
 
        user_name=user_name 
    ) 
 
# ========================================================= 
## ========================================================= 
# NEW APPLICATION 
# ========================================================= 
 
@app.route( 
    "/application", 
    methods=["GET", "POST"] 
) 
def application(): 
 
    # ----------------------------------------------------- 
    # LOGIN CHECK 
    # ----------------------------------------------------- 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
    # ----------------------------------------------------- 
    # ONLY CITIZENS CAN SUBMIT APPLICATION 
    # ----------------------------------------------------- 
 
    if current_role() != "citizen": 
 
        flash( 
            "Only citizens can submit applications.", 
            "danger" 
        ) 
 
        return redirect_by_role() 
 
    # ----------------------------------------------------- 
    # GET REQUEST 
    # ----------------------------------------------------- 
 
    if request.method == "GET": 
 
        return render_template( 
            "application.html" 
        ) 
 
    # ----------------------------------------------------- 
    # SERVICE 
    # ----------------------------------------------------- 
 
    service = request.form.get( 
        "service", 
        "" 
    ).strip() 
 
    if not service: 
 
        flash( 
            "Please select a service.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("application") 
        ) 
 
    # ----------------------------------------------------- 
    # GENERATE APPLICATION NUMBER 
    # ----------------------------------------------------- 
 
    application_number = ( 
        "GVA-" 
        + str(uuid.uuid4())[:8].upper() 
    ) 
 
    # ----------------------------------------------------- 
    # CREATE APPLICATION 
    # ----------------------------------------------------- 
 
    new_application = Application( 
 
        application_number=application_number, 
 
        user_id=session["user_id"], 
 
        service=service, 
 
        status="Submitted", 
 
        risk_score=0, 
 
        risk_level="Low" 
    ) 
 
    uploaded_count = 0 
 
    try: 
 
        # Save application first 
        db.session.add( 
            new_application 
        ) 
 
        # Generate application ID 
        db.session.flush() 
 
        # ------------------------------------------------- 
        # DOCUMENT TYPES 
        # ------------------------------------------------- 
 
        document_types = [ 
            "identity_proof", 
            "address_proof", 
            "income_proof" 
        ] 
 
        # ------------------------------------------------- 
        # DOCUMENT UPLOAD 
        # ------------------------------------------------- 
 
        for document_type in document_types: 
 
            file = request.files.get( 
                document_type 
            ) 
 
            if not file or not file.filename: 
 
                continue 
 
            # --------------------------------------------- 
            # FILE TYPE CHECK 
            # --------------------------------------------- 
 
            if not allowed_file( 
                file.filename 
            ): 
 
                flash( 
                    f"Invalid file type for {document_type}. " 
                    "Allowed: PDF, JPG, JPEG, PNG.", 
                    "danger" 
                ) 
 
                continue 
 
            # --------------------------------------------- 
            # SECURE ORIGINAL FILE NAME 
            # --------------------------------------------- 
 
            original_filename = secure_filename( 
                file.filename 
            ) 
 
            if not original_filename: 
 
                flash( 
                    f"Invalid filename for {document_type}.", 
                    "danger" 
                ) 
 
                continue 
 
            # --------------------------------------------- 
            # UNIQUE FILE NAME 
            # --------------------------------------------- 
 
            unique_filename = ( 
                str(uuid.uuid4()) 
                + "_" 
                + original_filename 
            ) 
 
            filepath = os.path.join( 
                app.config["UPLOAD_FOLDER"], 
                unique_filename 
            ) 
 
            # --------------------------------------------- 
            # SAVE FILE 
            # --------------------------------------------- 
 
            file.save( 
                filepath 
            ) 
 
            # --------------------------------------------- 
            # CREATE DOCUMENT RECORD 
            # --------------------------------------------- 
 
            new_document = Document( 
 
                application_id=new_application.id, 
 
                document_type=document_type, 
 
                filename=original_filename, 
 
                file_path=filepath 
            ) 
 
            db.session.add( 
                new_document 
            ) 
 
            uploaded_count += 1 
 
        # ------------------------------------------------- 
        # SAVE APPLICATION AND DOCUMENTS 
        # ------------------------------------------------- 
 
        db.session.commit() 
 
    except Exception as e: 
 
        db.session.rollback() 
 
        print( 
            "Application Submission Error:", 
            e 
        ) 
 
        flash( 
            "Application submit nahi ho saki. Please try again.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("application") 
        ) 
 
    # ----------------------------------------------------- 
    # SUCCESS MESSAGE 
    # ----------------------------------------------------- 
 
    if uploaded_count > 0: 
 
        flash( 
            f"Application {application_number} submitted " 
            f"successfully with {uploaded_count} document(s).", 
            "success" 
        ) 
 
    else: 
 
        flash( 
            f"Application {application_number} " 
            "submitted successfully.", 
            "success" 
        ) 
 
    # ----------------------------------------------------- 
    # RETURN TO CITIZEN DASHBOARD 
    # ----------------------------------------------------- 
 
    return redirect( 
        url_for( 
            "citizen_dashboard" 
        ) 
    ) 
 
 
# ========================================================= 
# APPLICATION DETAILS 
# ========================================================= 
 
@app.route( 
    "/application/<int:application_id>" 
) 
def application_details( 
    application_id 
): 
 
    # ----------------------------------------------------- 
    # LOGIN CHECK 
    # ----------------------------------------------------- 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    # ----------------------------------------------------- 
    # ONLY CITIZEN CAN USE THIS ROUTE 
    # ----------------------------------------------------- 
 
    if current_role() != "citizen": 
 
        flash( 
            "Access denied.", 
            "danger" 
        ) 
 
        return redirect_by_role() 
 
 
    # ----------------------------------------------------- 
    # FETCH ONLY LOGGED-IN CITIZEN'S APPLICATION 
    # ----------------------------------------------------- 
 
    application_data = ( 
        Application.query 
        .filter_by( 
 
            id=application_id, 
 
            user_id=session["user_id"] 
        ) 
        .first_or_404() 
    ) 
 
 
    # ----------------------------------------------------- 
    # SHOW APPLICATION DETAILS 
    # ----------------------------------------------------- 
 
    return render_template( 
 
        "application_details.html", 
 
        application=application_data 
    ) 
 
 
# ========================================================= 
# UPDATE PROFILE 
# ========================================================= 
 
@app.route( 
    "/profile", 
    methods=["GET", "POST"] 
) 
def update_profile(): 
 
    # ----------------------------------------------------- 
    # LOGIN CHECK 
    # ----------------------------------------------------- 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    # ----------------------------------------------------- 
    # GET CURRENT USER 
    # ----------------------------------------------------- 
 
    user = User.query.get_or_404( 
        session["user_id"] 
    ) 
 
 
    # ----------------------------------------------------- 
    # UPDATE PROFILE 
    # ----------------------------------------------------- 
 
    if request.method == "POST": 
 
        full_name = request.form.get( 
            "full_name", 
            "" 
        ).strip() 
 
        email = request.form.get( 
            "email", 
            "" 
        ).strip().lower() 
 
 
        # ------------------------------------------------- 
        # VALIDATION 
        # ------------------------------------------------- 
 
        if not full_name or not email: 
 
            flash( 
                "Name and email are required.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("update_profile") 
            ) 
 
 
        # ------------------------------------------------- 
        # CHECK DUPLICATE EMAIL 
        # ------------------------------------------------- 
 
        existing_user = User.query.filter( 
 
            User.email == email, 
 
            User.id != user.id 
 
        ).first() 
 
 
        if existing_user: 
 
            flash( 
                "This email is already registered.", 
                "danger" 
            ) 
 
            return redirect( 
                url_for("update_profile") 
            ) 
 
 
        # ------------------------------------------------- 
        # SAVE CHANGES 
        # ------------------------------------------------- 
 
        user.full_name = full_name 
 
        user.email = email 
 
        db.session.commit() 
 
 
        # ------------------------------------------------- 
        # UPDATE SESSION 
        # ------------------------------------------------- 
 
        session["user_name"] = user.full_name 
 
 
        flash( 
            "Profile updated successfully.", 
            "success" 
        ) 
 
 
        # ------------------------------------------------- 
        # RETURN TO CORRECT DASHBOARD 
        # ------------------------------------------------- 
 
        return redirect_by_role() 
 
 
    # ----------------------------------------------------- 
    # OPEN PROFILE PAGE 
    # ----------------------------------------------------- 
 
    return render_template( 
 
        "profile.html", 
 
        user=user 
    ) 
# ========================================================= 
# SETTINGS 
# ========================================================= 
 
@app.route("/settings") 
def settings(): 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
    return render_template( 
        "settings.html" 
    ) 
# ========================================================= 
# CHANGE PASSWORD 
# ========================================================= 
 
@app.route( 
    "/change-password", 
    methods=["POST"] 
) 
def change_password(): 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
    current_password = request.form.get( 
        "current_password", 
        "" 
    ) 
 
    new_password = request.form.get( 
        "new_password", 
        "" 
    ) 
 
    confirm_password = request.form.get( 
        "confirm_password", 
        "" 
    ) 
 
    # Check empty fields 
 
    if not current_password or not new_password or not confirm_password: 
 
        flash( 
            "Please fill all password fields.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("settings") 
        ) 
 
    # Check current password 
 
    user = User.query.get_or_404( 
        session["user_id"] 
    ) 
 
    if not bcrypt.check_password_hash( 
        user.password, 
        current_password 
    ): 
 
        flash( 
            "Current password is incorrect.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("settings") 
        ) 
 
    # Check new password length 
 
    if len(new_password) < 8: 
 
        flash( 
            "New password must contain at least 8 characters.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("settings") 
        ) 
 
    # Check new passwords match 
 
    if new_password != confirm_password: 
 
        flash( 
            "New passwords do not match.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("settings") 
        ) 
 
    # Prevent same password 
 
    if current_password == new_password: 
 
        flash( 
            "New password must be different from current password.", 
            "danger" 
        ) 
 
        return redirect( 
            url_for("settings") 
        ) 
 
    # Hash and save new password 
 
    user.password = ( 
        bcrypt 
        .generate_password_hash(new_password) 
        .decode("utf-8") 
    ) 
 
    try: 
 
        db.session.commit() 
 
        flash( 
            "Password changed successfully.", 
            "success" 
        ) 
 
    except Exception as e: 
 
        db.session.rollback() 
 
        print( 
            "Password Change Error:", 
            e 
        ) 
 
        flash( 
            "Password change failed. Please try again.", 
            "danger" 
        ) 
 
    return redirect( 
        url_for("settings") 
    ) 
 
# ========================================================= 
# HELP AND SUPPORT 
# ========================================================= 
 
@app.route( 
    "/help-support" 
) 
def help_support(): 
 
    # ----------------------------------------------------- 
    # LOGIN CHECK 
    # ----------------------------------------------------- 
 
    if not is_logged_in(): 
 
        flash( 
            "Please login first.", 
            "warning" 
        ) 
 
        return redirect( 
            url_for("login") 
        ) 
 
 
    return render_template( 
        "help_support.html" 
    ) 
 
 
# ========================================================= 
# LOGOUT 
# ========================================================= 
 
@app.route( 
    "/logout" 
) 
def logout(): 
 
    # Clear complete session 
    session.clear() 
 
 
    flash( 
        "You have been logged out.", 
        "success" 
    ) 
 
 
    return redirect( 
        url_for("login") 
    ) 
 
 
# ========================================================= 
# RUN APPLICATION 
# ========================================================= 
 
if __name__ == "__main__": 
 
    app.run( 
        debug=True 
    )