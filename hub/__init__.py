import os

from flask import Flask, session, render_template, request
from flask_session import Session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


#set DATABASE_URL= "postgres://tmzgtmwfpuvzup:82d8da4476a90cf9f0acbc8ea68182cb85cbaba50dc31b77e8bcc960030b5e98@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d3cbu5g4n0alq"
#export DATABASE_URL= "postgresql://tmzgtmwfpuvzup:82d8da4476a90cf9f0acbc8ea68182cb85cbaba50dc31b77e8bcc960030b5e98@ec2-18-206-20-102.compute-1.amazonaws.com:5432/d3cbu5g4n0alq"
app = Flask(__name__)

# Check for environment variable
#if not os.getenv("DATABASE_URL"):
    #raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Sign session cookies for protection against cookie data tampering.
app.config["SECRET_KEY"] = '21b4e5e125d4155fac5997fc3d4c19f721a5df193d3f9c59'

Session(app)



# For Local Database
# engine = create_engine("postgresql://postgres:root@localhost/libernet")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# Encryption
bcrypt = Bcrypt(app)

# Modularized routing functions
from hub import routes