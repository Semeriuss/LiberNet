from flask import render_template, url_for, flash, redirect, request, session
from hub import app, db, bcrypt
from hub.forms import RegistrationForm, LoginForm, ReviewForm
from hub.functions import authorize, is_authorized, api_search
from flask_login import login_user, current_user, logout_user, login_required

# Route for home page
@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    if request.method == "GET":
        return render_template("index.html", user=session.get("user"))
    
   
# Route for search page
@app.route("/search", methods=['POST', 'GET'])
@authorize
def search():
    # Return just the search page if GET request 
    if request.method == 'GET':
        return render_template('search.html')
        
    # Get data from search bar
    string = request.form.get("search_value", None)

    if string == None or string == "":
        flash("You must provide a term to search", 'danger')
        return redirect(url_for('search'))

    # format string for database search
    string = "%{}%".format(string)

    books = db.execute("SELECT * FROM books WHERE (isbn LIKE :isbn OR LOWER(title) LIKE LOWER(:title) OR LOWER(author) LIKE LOWER(:author) OR year LIKE :year)", {"isbn":string, "title":string, "author":string, "year":string}).fetchall()

    if not len(books):
        flash("Not found. Check your input and try again.", 'danger')
        redirect(url_for('search'))
    
    # For POST (searching files) return results of user's search on the same page
    flash("The search results are below. Click the ISBN numbers to check the books in detail.", 'info')
    return render_template("search.html", books=books)

# Route for explore page
@app.route("/explore", methods=['GET', 'POST'])
@authorize
def explore():

    # Search database for top ten results from database based on average rating and in ascending order
    displays = db.execute("SELECT * FROM books ORDER BY average_rating ASC FETCH FIRST 10 ROWS ONLY").fetchall()
    
    # Lists and a function to store image links and isbn
    myList = []
    myIsbn = []
    
    for display in displays:
        book_info = api_search(display[3]) 
        book_img = book_info[3] 
        isbn = display[3]
        myList.append(book_img) 
        myIsbn.append(isbn)

    # Return top ten rated books for GET request
    if request.method == 'GET':
        return render_template('explore.html', myList=myList, myIsbn=myIsbn )

# Helper routing function for getting details about a book from search page or explore page
@app.route("/about/<string:isbn>", methods=['GET', "POST"])
@authorize
def about(isbn):
    # Review form setup
    form = ReviewForm()
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn;", {"isbn": isbn}).fetchone()

    if book is None:
        flash("ISBN Not found on the database.", 'warning')
        redirect(url_for('search'))

   
    reviews = db.execute("SELECT * FROM reviews WHERE book_id= :book_id",{"book_id":book[0]}).fetchall()

    # Check if user has already reviewed a book
    current_user_review = db.execute("SELECT * FROM reviews WHERE book_id = :book_id and user_id = :user_id",{"book_id":book[0],"user_id":session.get("user")[0] }).fetchone()
    
    # bool value to check if user has reviewed book
    hasNotReviewed = False if current_user_review!=None else True

    current_user = session.get("user")[1]
    book_info = api_search(isbn) #returns a list containing page count, average rating, image, and description

    # if user can reveiw add to database
    if form.validate_on_submit():
        rating = int(form.rating.data)
        desc = form.description.data
        flash("You've successfully posted a review.", 'success')

        db.execute("INSERT INTO reviews (user_id,book_id,rating, description) VALUES (:user_id, :book_id, :rating, :description)",
            {"user_id": session.get("user_id"), "book_id": book[0], "rating": rating, "description": desc})
        db.commit()
        return redirect(url_for('index'))

    return render_template("explore.html", book=book, book_info=book_info, reviews=reviews, form=form, hasNotReviewed=hasNotReviewed, current_user=current_user)

# Route for sign up
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        db.execute("INSERT INTO users (username, email, password) VALUES (:uname, :email, :passkey)",
                   {"uname": form.username.data, "email": form.email.data, "passkey": hashed_password})
        db.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)


# Route for signing in 
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.execute("SELECT * FROM users WHERE email = :email;",{"email":form.email.data}).fetchone()
        if user and bcrypt.check_password_hash(user["password"], form.password.data):
            session["user"] = user
            session["user_id"] = user["id"]
            next_page = request.args.get('next')
            flash('You have successfully Logged In!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('search'))
        else:
            flash('Login Unsuccessful. Please Check Email and Password', 'danger')
    return render_template("login.html", title="Login", form=form)
    
# Route for signing in 
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash('You have successfully Logged out!', 'success')
    return redirect(url_for("index"))

