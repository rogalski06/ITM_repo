from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from datetime import datetime
import secrets
import os
import smtplib
from email.message import EmailMessage
import base64


app = Flask(__name__)
app.secret_key = "digibooth_secret_key"


UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


DATABASE = "digibooth.db"




# --------------------------------
# DATABASE HELPERS
# --------------------------------


def get_db_connection():
   conn = sqlite3.connect(DATABASE)
   conn.row_factory = sqlite3.Row
   return conn




def create_users_table():
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




def validate_required_fields(name, username, email):
   return bool(name and username and email)




def validate_hawaii_email(email):
   return email.lower().endswith("@hawaii.edu")




def generate_confirmation_code():
   return str(secrets.randbelow(900000) + 100000)




def user_exists(username, email):
   conn = get_db_connection()


   existing_user = conn.execute(
       "SELECT * FROM users WHERE username = ? OR email = ?",
       (username, email)
   ).fetchone()


   conn.close()


   return existing_user is not None




def save_new_user(name, username, email, confirmation_code):
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




def confirm_user_email(email, confirmation_code):
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




def send_confirmation_email(to_email, confirmation_code):
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
# BASIC ROUTES
# --------------------------------


@app.route("/")
def home():
   return render_template("home.html")




@app.route("/signup")
def signup():
   return render_template("signup.html", error=None)




@app.route("/signin")
def signin():
   return render_template("signin.html", error=None)




@app.route("/logout")
def logout():
   session.clear()
   return redirect("/")




# --------------------------------
# SIGN UP / SIGN IN ROUTES
# --------------------------------


@app.route("/signup_submit", methods=["POST"])
def signup_submit():
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


   return render_template(
       "confirm_email.html",
       email=email,
       message=None,
       error="Account was created, but the confirmation email could not be sent."
   )




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


   if "posts" not in session:
       session["posts"] = []


   return redirect("/feed")




# --------------------------------
# EMAIL CONFIRMATION ROUTES
# --------------------------------


@app.route("/confirm")
def confirm():
   return render_template("confirm_email.html", error=None, message=None)




@app.route("/confirm_submit", methods=["POST"])
def confirm_submit():
   email = request.form.get("email", "").strip().lower()
   confirmation_code = request.form.get("confirmation_code", "").strip()


   if not email or not confirmation_code:
       return render_template(
           "confirm_email.html",
           error="Please enter both your email and confirmation code.",
           message=None
       )


   if confirm_user_email(email, confirmation_code):
       conn = get_db_connection()
       user = conn.execute("SELECT username FROM users WHERE email = ?", (email,)).fetchone()
       conn.close()
       if user:
           session["username"] = user["username"]
           if "posts" not in session:
               session["posts"] = []
           return redirect("/feed")
       else:
           return render_template(
               "confirm_email.html",
               error="Confirmation successful, but unable to sign in. Please try signing in manually.",
               message=None
           )


   return render_template(
       "confirm_email.html",
       error="Invalid email or confirmation code.",
       message=None
   )




# --------------------------------
# FEED ROUTE
# --------------------------------
@app.route("/feed")
def feed():
   if "username" not in session:
       return redirect("/signin")


   search_query = request.args.get("q", "").strip().lower()
   posts = session.get("posts", [])


   if search_query:
       filtered_posts = []


       for post in posts:
           username = post.get("username", "").lower()
           caption = post.get("caption", "").lower()
           tags = post.get("tags", "").lower()


           if (
               search_query in username
               or search_query in caption
               or search_query in tags
           ):
               filtered_posts.append(post)


       posts = filtered_posts


   return render_template(
       "feed.html",
       username=session["username"],
       posts=posts,
       search_query=search_query
   )


# --------------------------------
# PHOTOBOOTH ROUTES
# --------------------------------


@app.route("/booth")
def booth():
   if "username" not in session:
       return redirect("/signin")


   return render_template(
       "booth.html",
       username=session["username"],
       error=None
   )




@app.route("/booth_capture", methods=["POST"])
def booth_capture():
   if "username" not in session:
       return redirect("/signin")


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


   return redirect("/booth_preview")




@app.route("/booth_preview")
def booth_preview():
   if "username" not in session:
       return redirect("/signin")


   booth_data = session.get("booth_data")


   if booth_data is None:
       return redirect("/booth")


   return render_template("booth_preview.html", booth_data=booth_data)




@app.route("/booth_next")
def booth_next():
   if "username" not in session:
       return redirect("/signin")


   booth_data = session.get("booth_data")


   if booth_data is None:
       return redirect("/booth")


   return render_template("booth_next.html", booth_data=booth_data)




@app.route("/post_to_feed", methods=["POST"])
def post_to_feed():
   if "username" not in session:
       return redirect("/signin")


   booth_data = session.get("booth_data")


   if booth_data is None:
       return redirect("/booth")


   caption = request.form.get("caption", "").strip()
   tags = request.form.get("tags", "").strip()


   new_post = {
       "image_filenames": booth_data["image_filenames"],
       "filter_choice": booth_data["filter_choice"],
       "frame_choice": booth_data["frame_choice"],
       "layout_choice": booth_data["layout_choice"],
       "username": session["username"],
       "timestamp": booth_data["timestamp"],
       "caption": caption,
       "tags": tags
   }


   posts = session.get("posts", [])
   posts.append(new_post)
   session["posts"] = posts


   session.pop("booth_data", None)


   return redirect("/feed")




# --------------------------------
# RUN APP
# --------------------------------




if __name__ == "__main__":
   create_users_table()
   app.run(debug=True)