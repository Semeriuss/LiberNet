import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

#set DATABASE_URL= "postgres://tmzgtmwfpuvzup:82d8da4476a90cf9f0acbc8ea68182cb85cbaba50dc31b77e8bcc960030b5e98@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d3cbu5g4n0alq"

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project One: TODO"


if __name__ == '__main__':
    app.run(debug=True)
