from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import secrets
import os
import smtplib
from email.message import EmailMessage
import base64
import json
import pandas as pd

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
            created_at TEXT NOT NULL,
            profile_image TEXT,
            bio TEXT,
            user_type TEXT DEFAULT 'public'
        )
    """)

    try:
        conn.execute("ALTER TABLE users ADD COLUMN profile_image TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE users ADD COLUMN bio TEXT")
    except sqlite3.OperationalError:
        pass

    try:
        conn.execute("ALTER TABLE users ADD COLUMN user_type TEXT DEFAULT 'public'")
    except sqlite3.OperationalError:
        pass

    conn.execute("""
        UPDATE users
        SET user_type = CASE
            WHEN LOWER(email) LIKE '%@hawaii.edu' THEN 'uh'
            ELSE 'public'
        END
        WHERE user_type IS NULL
    """)

    conn.commit()
    conn.close()


def create_posts_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            image_filenames TEXT NOT NULL,
            filter_choice TEXT,
            frame_choice TEXT,
            layout_choice TEXT,
            caption TEXT,
            tags TEXT,
            timestamp TEXT NOT NULL,
            privacy TEXT DEFAULT 'public'
        )
    """)

    try:
        conn.execute("ALTER TABLE posts ADD COLUMN privacy TEXT DEFAULT 'public'")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


def create_likes_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            UNIQUE(post_id, username)
        )
    """)

    conn.commit()
    conn.close()


def create_follows_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS follows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            follower_username TEXT NOT NULL,
            followed_username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            UNIQUE(follower_username, followed_username)
        )
    """)

    conn.commit()
    conn.close()


def get_user_type(email):
    if email.lower().endswith("@hawaii.edu"):
        return "uh"
    return "public"


def is_uh_user(username):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT user_type FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    return user is not None and user["user_type"] == "uh"


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


def username_exists(username):
    conn = get_db_connection()

    existing_user = conn.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()
    return existing_user is not None


def save_new_user(name, username, email, confirmation_code):
    conn = get_db_connection()

    user_type = get_user_type(email)

    conn.execute(
        """
        INSERT INTO users
        (name, username, email, confirmed, confirmation_code, created_at, user_type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            username,
            email,
            0,
            confirmation_code,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_type
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


def update_user_profile(username, profile_image=None, bio=None):
    conn = get_db_connection()

    if profile_image is not None:
        conn.execute(
            "UPDATE users SET profile_image = ? WHERE username = ?",
            (profile_image, username)
        )

    if bio is not None:
        conn.execute(
            "UPDATE users SET bio = ? WHERE username = ?",
            (bio, username)
        )

    conn.commit()
    conn.close()


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

Your confirmation code is: {confirmation_code}

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


# --------------------------------
# SIGN UP / SIGN IN ROUTES
# --------------------------------

@app.route("/signup_submit", methods=["POST"])
def signup_submit():
    name = request.form.get("name", "").strip()
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip().lower()

    if not name or not username or not email:
        return render_template(
            "signup.html",
            error="All fields are required. Please complete the full form."
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
        SELECT username, email, confirmed, user_type
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
    session["user_type"] = user["user_type"]

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

        user = conn.execute(
            "SELECT username, user_type FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        conn.close()

        if user:
            session["username"] = user["username"]
            session["user_type"] = user["user_type"]
            return redirect("/feed")

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

    current_user = session["username"]
    search_query = request.args.get("q", "").strip().lower()
    view = request.args.get("view", "public")

    conn = get_db_connection()

    current_user_row = conn.execute(
        "SELECT user_type FROM users WHERE username = ?",
        (current_user,)
    ).fetchone()

    current_user_type = current_user_row["user_type"] if current_user_row else "public"
    current_is_uh = current_user_type == "uh"
    session["user_type"] = current_user_type

    if view == "following":
        followed_users = conn.execute(
            "SELECT followed_username FROM follows WHERE follower_username = ?",
            (current_user,)
        ).fetchall()

        followed_usernames = [row["followed_username"] for row in followed_users]
        followed_usernames.append(current_user)

        placeholders = ",".join("?" * len(followed_usernames))

        if current_is_uh:
            posts_rows = conn.execute(
                f"""
                SELECT posts.*, users.user_type
                FROM posts
                JOIN users ON posts.username = users.username
                WHERE posts.username IN ({placeholders})
                AND posts.privacy IN ('public', 'university')
                ORDER BY posts.timestamp DESC
                """,
                followed_usernames
            ).fetchall()
        else:
            posts_rows = conn.execute(
                f"""
                SELECT posts.*, users.user_type
                FROM posts
                JOIN users ON posts.username = users.username
                WHERE posts.username IN ({placeholders})
                AND posts.privacy = 'public'
                ORDER BY posts.timestamp DESC
                """,
                followed_usernames
            ).fetchall()

    elif view == "university":
        if not current_is_uh:
            posts_rows = []
        else:
            posts_rows = conn.execute(
                """
                SELECT posts.*, users.user_type
                FROM posts
                JOIN users ON posts.username = users.username
                WHERE posts.privacy = 'university'
                ORDER BY posts.timestamp DESC
                """
            ).fetchall()

    else:
        view = "public"

        posts_rows = conn.execute(
            """
            SELECT posts.*, users.user_type
            FROM posts
            JOIN users ON posts.username = users.username
            WHERE posts.privacy = 'public'
            ORDER BY posts.timestamp DESC
            """
        ).fetchall()

    posts = []

    for row in posts_rows:
        post = dict(row)
        post["image_filenames"] = json.loads(post["image_filenames"])

        like_count = conn.execute(
            "SELECT COUNT(*) as count FROM likes WHERE post_id = ?",
            (post["id"],)
        ).fetchone()["count"]

        user_liked = conn.execute(
            "SELECT 1 FROM likes WHERE post_id = ? AND username = ?",
            (post["id"], current_user)
        ).fetchone() is not None

        post["like_count"] = like_count
        post["user_liked"] = user_liked

        posts.append(post)

    if search_query:
        filtered_posts = []

        for post in posts:
            username = post.get("username", "").lower()
            caption = post.get("caption", "").lower()
            tags = post.get("tags", "").lower()

            if search_query in username or search_query in caption or search_query in tags:
                filtered_posts.append(post)

        user_rows = conn.execute(
            """
            SELECT username, name, bio, profile_image, user_type
            FROM users
            WHERE username LIKE ? OR name LIKE ? OR bio LIKE ?
            """,
            (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%")
        ).fetchall()

        users = []

        for row in user_rows:
            user = dict(row)

            follower_count = conn.execute(
                "SELECT COUNT(*) as count FROM follows WHERE followed_username = ?",
                (user["username"],)
            ).fetchone()["count"]

            following_count = conn.execute(
                "SELECT COUNT(*) as count FROM follows WHERE follower_username = ?",
                (user["username"],)
            ).fetchone()["count"]

            is_following = False

            if current_user != user["username"]:
                is_following = conn.execute(
                    """
                    SELECT 1 FROM follows
                    WHERE follower_username = ? AND followed_username = ?
                    """,
                    (current_user, user["username"])
                ).fetchone() is not None

            user["follower_count"] = follower_count
            user["following_count"] = following_count
            user["is_following"] = is_following

            users.append(user)

        posts = filtered_posts

    else:
        users = []

    conn.close()

    return render_template(
        "feed.html",
        username=session["username"],
        posts=posts,
        users=users,
        search_query=search_query,
        view=view,
        current_is_uh=current_is_uh,
        error=None
    )


@app.route("/matches")
def matches():
    if "username" not in session:
        return redirect("/signin")

    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect("/signin")

    conn = get_db_connection()

    posts_rows = conn.execute(
        "SELECT username, tags FROM posts WHERE privacy = 'public'"
    ).fetchall()

    conn.close()

    total_posts = len(posts_rows)
    posts_per_user = {}
    tag_counts = {}

    for row in posts_rows:
        username = row["username"]
        posts_per_user[username] = posts_per_user.get(username, 0) + 1

        if row["tags"]:
            tags = clean_tags(row["tags"]).split(",")

            for tag in tags:
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

    top_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
    active_users = sorted(posts_per_user.items(), key=lambda item: item[1], reverse=True)

    matches = get_match_results(session["username"])

    return render_template(
        "dashboard.html",
        total_posts=total_posts,
        top_tags=top_tags,
        active_users=active_users,
        matches=matches
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/signin")


# --------------------------------
# PROFILE ROUTES
# --------------------------------

@app.route("/profile")
@app.route("/profile/")
@app.route("/profile/<username>")
def profile(username=None):
    if "username" not in session:
        return redirect("/signin")

    current_user = session["username"]

    if username is None:
        username = current_user

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if user is None:
        conn.close()
        return "User not found", 404

    current_user_row = conn.execute(
        "SELECT user_type FROM users WHERE username = ?",
        (current_user,)
    ).fetchone()

    current_user_type = current_user_row["user_type"] if current_user_row else "public"

    if current_user == username:
        user_posts = conn.execute(
            """
            SELECT posts.*, users.user_type
            FROM posts
            JOIN users ON posts.username = users.username
            WHERE posts.username = ?
            ORDER BY posts.timestamp DESC
            """,
            (username,)
        ).fetchall()

    elif current_user_type == "uh":
        user_posts = conn.execute(
            """
            SELECT posts.*, users.user_type
            FROM posts
            JOIN users ON posts.username = users.username
            WHERE posts.username = ?
            AND posts.privacy IN ('public', 'university')
            ORDER BY posts.timestamp DESC
            """,
            (username,)
        ).fetchall()

    else:
        user_posts = conn.execute(
            """
            SELECT posts.*, users.user_type
            FROM posts
            JOIN users ON posts.username = users.username
            WHERE posts.username = ?
            AND posts.privacy = 'public'
            ORDER BY posts.timestamp DESC
            """,
            (username,)
        ).fetchall()

    follower_count = conn.execute(
        "SELECT COUNT(*) as count FROM follows WHERE followed_username = ?",
        (username,)
    ).fetchone()["count"]

    following_count = conn.execute(
        "SELECT COUNT(*) as count FROM follows WHERE follower_username = ?",
        (username,)
    ).fetchone()["count"]

    is_following = False

    if current_user != username:
        is_following = conn.execute(
            """
            SELECT 1 FROM follows
            WHERE follower_username = ? AND followed_username = ?
            """,
            (current_user, username)
        ).fetchone() is not None

    posts = []

    for row in user_posts:
        post = dict(row)
        post["image_filenames"] = json.loads(post["image_filenames"])

        like_count = conn.execute(
            "SELECT COUNT(*) as count FROM likes WHERE post_id = ?",
            (post["id"],)
        ).fetchone()["count"]

        user_liked = conn.execute(
            "SELECT 1 FROM likes WHERE post_id = ? AND username = ?",
            (post["id"], current_user)
        ).fetchone() is not None

        post["like_count"] = like_count
        post["user_liked"] = user_liked

        posts.append(post)

    conn.close()

    return render_template(
        "profile.html",
        user=user,
        posts=posts,
        follower_count=follower_count,
        following_count=following_count,
        is_following=is_following,
        is_own_profile=(current_user == username)
    )


@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "username" not in session:
        return redirect("/signin")

    current_username = session["username"]
    new_username = request.form.get("username", "").strip()
    bio = request.form.get("bio", "").strip()

    if not new_username:
        return render_profile_error(current_username, "Username cannot be empty.")

    if new_username != current_username and username_exists(new_username):
        return render_profile_error(current_username, "That username is already taken.")

    profile_image = None

    if "profile_image" in request.files:
        file = request.files["profile_image"]

        if file and file.filename:
            filename = f"{new_username}_profile_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            profile_image = filename

    if new_username != current_username:
        conn = get_db_connection()

        conn.execute(
            "UPDATE users SET username = ? WHERE username = ?",
            (new_username, current_username)
        )

        conn.execute(
            "UPDATE posts SET username = ? WHERE username = ?",
            (new_username, current_username)
        )

        conn.execute(
            "UPDATE likes SET username = ? WHERE username = ?",
            (new_username, current_username)
        )

        conn.execute(
            "UPDATE follows SET follower_username = ? WHERE follower_username = ?",
            (new_username, current_username)
        )

        conn.execute(
            "UPDATE follows SET followed_username = ? WHERE followed_username = ?",
            (new_username, current_username)
        )

        conn.commit()
        conn.close()

        session["username"] = new_username
        username_to_save = new_username

    else:
        username_to_save = current_username

    update_user_profile(username_to_save, profile_image, bio)

    return redirect("/profile")


def render_profile_error(username, error_message):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    user_posts = conn.execute(
        """
        SELECT posts.*, users.user_type
        FROM posts
        JOIN users ON posts.username = users.username
        WHERE posts.username = ?
        ORDER BY posts.timestamp DESC
        """,
        (username,)
    ).fetchall()

    conn.close()

    posts = []

    for row in user_posts:
        post = dict(row)
        post["image_filenames"] = json.loads(post["image_filenames"])
        post["like_count"] = 0
        post["user_liked"] = False
        posts.append(post)

    return render_template(
        "profile.html",
        user=user,
        posts=posts,
        error=error_message
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
        return render_template(
            "signin.html",
            error="Please sign in before using the photobooth."
        )

    captured_images = request.form.getlist("captured_images")

    filter_choice = request.form.get("filter_choice", "none")
    frame_choice = request.form.get("frame_choice", "none")
    layout_choice = request.form.get("layout_choice", "strip")

    if not captured_images:
        return render_template(
            "booth.html",
            username=session["username"],
            error="Please take at least one photo."
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

    current_is_uh = is_uh_user(session["username"])

    return render_template(
        "booth_preview.html",
        booth_data=booth_data,
        current_is_uh=current_is_uh,
        error=None
    )


@app.route("/booth_preview")
def booth_preview():
    if "username" not in session:
        return redirect("/signin")

    booth_data = session.get("booth_data")

    if booth_data is None:
        return redirect("/booth")

    current_is_uh = is_uh_user(session["username"])

    return render_template(
        "booth_preview.html",
        booth_data=booth_data,
        current_is_uh=current_is_uh,
        error=None
    )


@app.route("/booth_next")
def booth_next():
    if "username" not in session:
        return redirect("/signin")

    booth_data = session.get("booth_data")

    if booth_data is None:
        return redirect("/booth")

    current_is_uh = is_uh_user(session["username"])

    return render_template(
        "booth_preview.html",
        booth_data=booth_data,
        current_is_uh=current_is_uh,
        error=None
    )


def clean_tags(tags):
    tag_list = tags.replace("#", "").split()
    cleaned_tags = []

    for tag in tag_list:
        cleaned_tag = tag.strip().lower().replace(" ", "")

        if cleaned_tag:
            cleaned_tags.append(cleaned_tag)

    return ",".join(cleaned_tags)


def get_match_results(current_user):
    conn = get_db_connection()

    posts_rows = conn.execute(
        "SELECT username, tags FROM posts WHERE privacy = 'public'"
    ).fetchall()

    conn.close()

    posts = []

    for row in posts_rows:
        if row["tags"]:
            posts.append({
                "username": row["username"],
                "tags": clean_tags(row["tags"]).split(",")
            })

    if not posts:
        return []

    df = pd.DataFrame(posts)

    user_tags = {}

    for username in df["username"].unique():
        tags_for_user = set()
        user_posts = df[df["username"] == username]

        for tag_list in user_posts["tags"]:
            tags_for_user.update(tag_list)

        user_tags[username] = tags_for_user

    current_tags = user_tags.get(current_user, set())
    match_results = []

    for username, tags in user_tags.items():
        if username == current_user:
            continue

        shared_tags = current_tags.intersection(tags)

        if current_tags:
            match_percent = round((len(shared_tags) / len(current_tags)) * 100)
        else:
            match_percent = 0

        if shared_tags:
            match_results.append({
                "username": username,
                "shared_tags": sorted(shared_tags),
                "match_percent": match_percent
            })

    match_results.sort(key=lambda match: match["match_percent"], reverse=True)

    return match_results


@app.route("/post_to_feed", methods=["POST"])
def post_to_feed():
    if "username" not in session:
        return redirect("/signin")

    booth_data = session.get("booth_data")

    if booth_data is None:
        return redirect("/booth")

    caption = request.form.get("caption", "").strip()
    tags = request.form.get("tags", "").strip()
    tags = clean_tags(tags)
    privacy = request.form.get("privacy", "public")

    if privacy not in ["public", "private", "university"]:
        privacy = "public"

    conn = get_db_connection()

    current_user_row = conn.execute(
        "SELECT user_type FROM users WHERE username = ?",
        (session["username"],)
    ).fetchone()

    current_user_type = current_user_row["user_type"] if current_user_row else "public"

    if privacy == "university" and current_user_type != "uh":
        conn.close()
        return render_template(
            "booth_preview.html",
            booth_data=booth_data,
            current_is_uh=False,
            error="Only verified UH users can post to the UH Only Feed."
        )

    conn.execute(
        """
        INSERT INTO posts
        (username, image_filenames, filter_choice, frame_choice, layout_choice, caption, tags, timestamp, privacy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session["username"],
            json.dumps(booth_data["image_filenames"]),
            booth_data["filter_choice"],
            booth_data["frame_choice"],
            booth_data["layout_choice"],
            caption,
            tags,
            booth_data["timestamp"],
            privacy
        )
    )

    conn.commit()
    conn.close()

    session.pop("booth_data", None)

    if privacy == "university":
        return redirect("/feed?view=university")

    if privacy == "private":
        return redirect("/profile")

    return redirect("/feed?view=public")


# --------------------------------
# LIKES / FOLLOWS
# --------------------------------

@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    if "username" not in session:
        return {"error": "Not logged in"}, 401

    username = session["username"]

    conn = get_db_connection()

    existing_like = conn.execute(
        "SELECT id FROM likes WHERE post_id = ? AND username = ?",
        (post_id, username)
    ).fetchone()

    if existing_like:
        conn.execute(
            "DELETE FROM likes WHERE post_id = ? AND username = ?",
            (post_id, username)
        )
        liked = False
    else:
        conn.execute(
            "INSERT INTO likes (post_id, username, timestamp) VALUES (?, ?, ?)",
            (post_id, username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        liked = True

    like_count = conn.execute(
        "SELECT COUNT(*) as count FROM likes WHERE post_id = ?",
        (post_id,)
    ).fetchone()["count"]

    conn.commit()
    conn.close()

    return {"liked": liked, "like_count": like_count}


@app.route("/follow/<followed_username>", methods=["POST"])
def follow_user(followed_username):
    if "username" not in session:
        return {"error": "Not logged in"}, 401

    follower_username = session["username"]

    if follower_username == followed_username:
        return {"error": "Cannot follow yourself"}, 400

    conn = get_db_connection()

    existing_follow = conn.execute(
        """
        SELECT id FROM follows
        WHERE follower_username = ? AND followed_username = ?
        """,
        (follower_username, followed_username)
    ).fetchone()

    if existing_follow:
        conn.execute(
            """
            DELETE FROM follows
            WHERE follower_username = ? AND followed_username = ?
            """,
            (follower_username, followed_username)
        )
        following = False
    else:
        conn.execute(
            """
            INSERT INTO follows
            (follower_username, followed_username, timestamp)
            VALUES (?, ?, ?)
            """,
            (
                follower_username,
                followed_username,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        following = True

    follower_count = conn.execute(
        "SELECT COUNT(*) as count FROM follows WHERE followed_username = ?",
        (followed_username,)
    ).fetchone()["count"]

    following_count = conn.execute(
        "SELECT COUNT(*) as count FROM follows WHERE follower_username = ?",
        (follower_username,)
    ).fetchone()["count"]

    conn.commit()
    conn.close()

    return {
        "following": following,
        "follower_count": follower_count,
        "following_count": following_count
    }


# --------------------------------
# RUN APP
# --------------------------------

if __name__ == "__main__":
    create_users_table()
    create_posts_table()
    create_likes_table()
    create_follows_table()
    app.run(debug=True)