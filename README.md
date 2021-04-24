Project 1 Assignment: Web Programming with Python and JavaScript based on CS50

https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/

Name of Application: LiberNet
Purpose: To search books from a local database and get details from an API (Google Books)
Used: Python (Flask), Bootstrap, HTML, CSS, JS

How to use
- Register
- Search books by ISBN, title, author, or publication year
- Click the ISBN link to get more detail about the book and review
- Get info about a book and submit your own review!
- Alternatively, click the Explore link to get the top rated books 

To Setup on your own
# Clone repo
$ git clone https://github.com/intro-web-programming/projectone-Semeriuss.git
$ cd projectone-Semeriuss

# Install all dependencies
$ pip install -r requirements.txt

# ENV Variables
$ set FLASK_APP = application.py # python -m application
$ set DATABASE_URL = Heroku Postgres DB URI or Local Postgres lin
$ set SECRET_KEY = secret key env variable

# You need to run import.py and create the database before you run the app

DB Schema
users: id (primary), username, email, password
books: id (primary), isbn, title, author, year
reviews: id (primary), user_id (foreign key), book_id (foreign key), description, rating


Landing Page

<img width="956" alt="Home" src="https://user-images.githubusercontent.com/50263682/115961084-83df0d80-a51d-11eb-9cb5-f34c41800ddc.PNG">


Registration Page

<img width="572" alt="Registration" src="https://user-images.githubusercontent.com/50263682/115961436-f2709b00-a51e-11eb-9fc1-1633efa26895.PNG">


Login Page

<img width="960" alt="Login" src="https://user-images.githubusercontent.com/50263682/115961110-9d805500-a51d-11eb-8f12-d954064a567c.PNG">



Search Page

<img width="956" alt="Search Page" src="https://user-images.githubusercontent.com/50263682/115961117-a96c1700-a51d-11eb-931c-e683b6f35457.PNG">



Search Results with ISBN Links

<img width="933" alt="Results" src="https://user-images.githubusercontent.com/50263682/115961123-b4bf4280-a51d-11eb-9295-46e0890bc06a.PNG">


Details and Review Page

<img width="923" alt="Review" src="https://user-images.githubusercontent.com/50263682/115961136-c3a5f500-a51d-11eb-8b11-fb081de2330d.PNG">


Explore Page

<img width="956" alt="Explore" src="https://user-images.githubusercontent.com/50263682/115961151-d3bdd480-a51d-11eb-803c-b42e3c36f6c4.PNG">


Feel Free to build up on it. Enjoy!
