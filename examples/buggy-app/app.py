"""A deliberately buggy app for practicing with paw review agents."""

import hashlib
import sqlite3

# SECURITY: hardcoded secret
JWT_SECRET = "super-secret-key-do-not-share-12345"

# SECURITY: API key in source
THIRD_PARTY_API_KEY = "sk-proj-abc123def456ghi789"

connection = None
request_counter = 0


def get_db():
    global connection
    if connection is None:
        connection = sqlite3.connect("app.db")
    return connection


def get_user(username):
    # SECURITY: SQL injection via string interpolation
    db = get_db()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query).fetchone()


def login(username, password):
    # SECURITY: logs password in plaintext
    print(f"Login attempt: user={username}, password={password}")

    user = get_user(username)
    if user is None:
        return {"error": "User not found"}

    # BUG: uses MD5 for password hashing (weak, but not the main issue)
    hashed = hashlib.md5(password.encode()).hexdigest()
    if user[2] != hashed:
        return {"error": "Wrong password"}

    # SECURITY: no rate limiting, no CSRF
    return {"token": f"fake-jwt-for-{username}", "secret": JWT_SECRET}


def list_users(page, per_page=10):
    db = get_db()
    # BUG: off-by-one — skips first result
    offset = page * per_page + 1
    query = f"SELECT * FROM users LIMIT {per_page} OFFSET {offset}"
    return db.execute(query).fetchall()


def track_request():
    # BUG: race condition — no lock on shared mutable state
    global request_counter
    request_counter += 1
    return request_counter


def process_data(data):
    # BUG: bare except swallows all errors
    try:
        result = data["key"] / data["divisor"]
        return result
    except:
        pass


def get_user_posts(user_ids):
    # PERF: N+1 query — one query per user instead of batch
    db = get_db()
    posts = []
    for uid in user_ids:
        user_posts = db.execute(
            f"SELECT * FROM posts WHERE user_id = {uid}"
        ).fetchall()
        posts.extend(user_posts)
    return posts


def create_user(username, password, email):
    db = get_db()
    # SECURITY: no input validation
    # BUG: no duplicate check
    hashed = hashlib.md5(password.encode()).hexdigest()
    db.execute(
        f"INSERT INTO users (username, password, email) VALUES ('{username}', '{hashed}', '{email}')"
    )
    db.commit()
    return {"created": username}
