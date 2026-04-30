# Import Flask tools
# Flask = creates the web app
# render_template = loads HTML files from templates folder
# request = gets form data submitted by the user
# redirect = sends the user to another route/page
from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import secrets
import os
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import base64

# Create the Flask application
app = Flask(__name__)
app.secret_key = "digibooth_secret_key"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------
# DATABASE & EMAIL HELPER FUNCTIONS
# --------------------------------
def allowed_file(filename):
    """
    Checks if uploaded file is an accepted image type.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
# Additions of database helper function 
DATABASE = "digibooth.db"

# Database user table function 
def create_users_table():
    """
    Creates the users table.
    This table stores account information for DigiBooth users.
    """
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            confirmed INTEGER DEFAULT 0,
            confirmation_code TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
def get_db_connection():
    """
    Opens a connection to the SQLite database.
    row_factory lets us access columns by name instead of index.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# UH Email Validation Function 
def validate_hawaii_email(email):
    """
    Checks that the user entered a hawaii.edu email.
    This helps limit DigiBooth sign-ups to UH users.
    """
    return email.lower().endswith("@hawaii.edu")

# Confirmation code function
def generate_confirmation_code():
    """
    Generates a secure random 6-digit confirmation code.
    This code will be emailed to the user later.
    """
    return str(secrets.randbelow(900000) + 100000)

# Duplicate User Check 
def user_exists(username, email):
    """
    Checks whether a username or email is already in the database.
    Prevents duplicate accounts.
    """
    conn = get_db_connection()

    existing_user = conn.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?",
        (username, email)
    ).fetchone()

    conn.close()

    return existing_user is not None

# Saves user
def save_new_user(name, username, email, confirmation_code):
    """
    Saves a new user to the SQLite database.
    New users are saved as unconfirmed until they enter the correct code.
    """
    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO users (name, username, email, confirmed, confirmation_code, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            username,
            email,
            0,
            confirmation_code,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

# Automated email confirmation 
def send_confirmation_email(to_email, confirmation_code):
    """
    Sends the confirmation code to the user's hawaii.edu email.
    Email login information is stored in environment variables
    instead of being written directly in the code.
    """

    sender_email = os.getenv("DIGIBOOTH_EMAIL")
    sender_password = os.getenv("DIGIBOOTH_EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials are missing.")
        return False

    message = EmailMessage()
    message["Subject"] = "Your DigiBooth Confirmation Code"
    message["From"] = sender_email
    message["To"] = to_email

    message.set_content(f"""
Aloha,

Thank you for signing up for DigiBooth!

Your confirmation code is:

{confirmation_code}

Enter this code on the DigiBooth confirmation page to activate your account.

Mahalo,
The DigiBooth Team
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)

        return True

    except Exception as error:
        print("Email failed to send:", error)
        return False

# --------------------------------
# INITIAL HELPER FUNCTIONS
# --------------------------------

def validate_required_fields(name, username, email):
    """
    Checks that the user filled out all required sign-up fields.
    Returns True if all fields are filled in.
    Returns False if any field is missing.
    """
    if not name or not username or not email:
        return False
    return True


# Cleaned up route section 
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup")
def signup():
    return render_template("signup.html", error=None)


@app.route("/signin")
def signin():
    return render_template("signin.html", error=None)


@app.route("/signin_submit", methods=["POST"])
def signin_submit():
    username_or_email = request.form.get("username_or_email", "").strip().lower()

    if not username_or_email:
        return render_template(
            "signin.html",
            error="Please enter your username or email."
        )

    conn = get_db_connection()

    user = conn.execute(
        """
        SELECT username, email, confirmed
        FROM users
        WHERE username = ? OR email = ?
        """,
        (username_or_email, username_or_email)
    ).fetchone()

    conn.close()

    if user is None:
        return render_template(
            "signup.html",
            error="No account was found with that username or email. Please create an account first."
        )

    if user["confirmed"] == 0:
        return render_template(
            "confirm_email.html",
            email=user["email"],
            error="Your account exists, but it has not been confirmed yet. Please enter your confirmation code.",
            message=None
        )

    session["username"] = user["username"]
    return redirect("/feed")



@app.route("/signup_submit", methods=["POST"])
def signup_submit():
    """
    Handles the sign-up form submission.
    Validates fields, checks hawaii.edu email, prevents duplicate users,
    generates a confirmation code, and saves the user to SQLite.
    """

    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()

    if not validate_required_fields(name, username, email):
        return render_template(
            "signup.html",
            error="All fields are required. Please complete the full form."
        )

    if not validate_hawaii_email(email):
        return render_template(
            "signup.html",
            error="Please use a valid @hawaii.edu email address."
        )

    if user_exists(username, email):
        return render_template(
            "signin.html",
            error="That account already exists. Please sign in instead."
        )
    confirmation_code = generate_confirmation_code()

    save_new_user(name, username, email, confirmation_code)

    email_sent = send_confirmation_email(email, confirmation_code)

    if email_sent:
        return render_template(
            "confirm_email.html",
            email=email,
            message="Account created! We sent a confirmation code to your email.",
            error=None
        )
    else:
        return render_template(
            "confirm_email.html",
            email=email,
            message=None,
            error="Account was created, but the confirmation email could not be sent. Please check that the email address is real and typed correctly. If this is a school email, make sure it can receive outside messages."
        )
@app.route("/logout")
def logout():
    session.clear()   # removes username + any session data
    return redirect("/")

@app.route("/confirm")
def confirm():
    """
    Displays the email confirmation page.
    """
    return render_template("confirm_email.html", error=None, message=None)


@app.route("/feed")
def feed():
    """
    Feed page route.
    Users must be signed in before viewing the feed.
    """
    if "username" not in session:
        return render_template(
            "signin.html",
            error="Please sign in before viewing the feed."
        )

    return render_template("feed.html", username=session["username"])

def confirm_user_email(email, confirmation_code):
    """
    Checks whether the email and confirmation code match a user in the database.
    If they match, the user's account is marked as confirmed.
    """
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND confirmation_code = ?",
        (email, confirmation_code)
    ).fetchone()

    if user is None:
        conn.close()
        return False

    conn.execute(
        "UPDATE users SET confirmed = 1 WHERE email = ?",
        (email,)
    )

    conn.commit()
    conn.close()

    return True


@app.route("/confirm_submit", methods=["POST"])
def confirm_submit():
    """
    Handles confirmation form submission.
    If the code is correct, the user account becomes active.
    """

    email = request.form.get("email", "").strip().lower()
    confirmation_code = request.form.get("confirmation_code", "").strip()

    if not email or not confirmation_code:
        return render_template(
            "confirm_email.html",
            error="Please enter both your email and confirmation code.",
            message=None
        )

    if confirm_user_email(email, confirmation_code):
        return render_template(
            "signin.html",
            error=None,
            message="Your account has been confirmed! Please sign in to continue."
        )
    
    return render_template(
        "confirm_email.html",
        error="Invalid email or confirmation code.",
        message=None
        )

@app.route("/booth")
def booth():
    """
    Photobooth page.
    User must be signed in.
    """
    if "username" not in session:
        return render_template(
            "signin.html",
            error="Please sign in before using the photobooth."
        )

    return render_template(
        "booth.html",
        username=session["username"],
        error=None
    )

@app.route("/booth_capture", methods=["POST"])
def booth_capture():
    """
    Handles photos taken from the camera in booth.html.
    Saves captured images to static/uploads.
    """

    if "username" not in session:
        return render_template(
            "signin.html",
            error="Please sign in before using the photobooth."
        )

    captured_images = request.form.getlist("captured_images")

    filter_choice = request.form.get("filter_choice", "none")
    frame_choice = request.form.get("frame_choice", "classic")
    layout_choice = request.form.get("layout_choice", "strip")

    if not captured_images:
        return render_template(
            "booth.html",
            username=session["username"],
            error="Please take at least one photo first."
        )

    saved_images = []

    for image_data in captured_images:
        if "," in image_data:
            image_data = image_data.split(",")[1]

        try:
            image_bytes = base64.b64decode(image_data)
        except Exception:
            return render_template(
                "booth.html",
                username=session["username"],
                error="Photo could not be saved. Please retake your photos."
            )

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filename = f"{session['username']}_{timestamp}.png"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        with open(file_path, "wb") as image_file:
            image_file.write(image_bytes)

        saved_images.append(filename)

    booth_data = {
        "image_filenames": saved_images,
        "filter_choice": filter_choice,
        "frame_choice": frame_choice,
        "layout_choice": layout_choice,
        "username": session["username"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    session["booth_data"] = booth_data

    return render_template("booth_preview.html", booth_data=booth_data)

    

    if "username" not in session:
        return render_template(
            "signin.html",
            error="Please sign in before uploading photos."
        )

    uploaded_files = request.files.getlist("images")

    filter_choice = request.form.get("filter_choice", "none")
    frame_choice = request.form.get("frame_choice", "none")
    layout_choice = request.form.get("layout_choice", "single")

    if not uploaded_files or uploaded_files[0].filename == "":
        return render_template(
            "booth.html",
            username=session["username"],
            error="Please upload at least one image."
        )

    saved_images = []

    for image in uploaded_files:
        if image.filename == "":
            continue

        if not allowed_file(image.filename):
            return render_template(
                "booth.html",
                username=session["username"],
                error="Invalid file type. Please upload PNG, JPG, JPEG, or GIF images."
            )

        safe_filename = secure_filename(image.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        final_filename = f"{session['username']}_{timestamp}_{safe_filename}"

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], final_filename)
        image.save(file_path)

        saved_images.append(final_filename)

    booth_data = {
        "image_filenames": saved_images,
        "filter_choice": filter_choice,
        "frame_choice": frame_choice,
        "layout_choice": layout_choice,
        "username": session["username"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    session["booth_data"] = booth_data

    return render_template("booth_preview.html", booth_data=booth_data)


@app.route("/booth_next")
def booth_next():
    """
    Placeholder page for the next phase.
    No post database is created yet.
    """
    if "username" not in session:
        return render_template(
            "signin.html",
            error="Please sign in first."
        )

    booth_data = session.get("booth_data")

    if booth_data is None:
        return redirect("/booth")

    return render_template("booth_next.html", booth_data=booth_data)

# --------------------------------
# RUN THE APPLICATION
# --------------------------------

# This makes the app run only when we directly run app.py.
# debug=True helps during development because it shows errors
# and reloads the app when we save changes.
# Ensures the database/table exists every time the app is ran.
if __name__ == "__main__":
    create_users_table()
    app.run(debug=True)