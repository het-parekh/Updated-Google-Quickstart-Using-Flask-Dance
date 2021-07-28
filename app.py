import os
from dotenv import load_dotenv
from flask import Flask, render_template ,redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import json

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("APP_SECRET_KEY")



blueprint = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return "GOTO /login/google to authorize yourself"
    resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")
    print(resp.json())
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])


