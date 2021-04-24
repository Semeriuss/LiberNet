from hub import db
import csv

# Data importing function
def importBooks():
    with open('./hub/books.csv', 'r') as file:
        books = csv.reader(file)
        next(books)
        for isbn,title,author,year in books:
            db.execute("insert into books(isbn, title, author,year,review_count, average_rating) values (:isbn, :title, :author, :year, :review_count, :average_rating)", {'isbn':isbn, 'title':title, 'author':author, 'year':year,'review_count':0,'average_rating':0})
        
        db.commit()
        file.close()
        print("Finished!!!")

# Database running function 
# Run only once!
def createDatabase():
    db.execute("CREATE TABLE users(id SERIAL PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL, psd TEXT NOT NULL, pic TEXT DEFAULT 'default.jpg') ");
    db.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, title TEXT NOT NULL, author TEXT NOT NULL, year, INTEGER NOT NULL, );")
    db.execute("CREATE TABLE reviews(id INTEGER PRIMARY KEY, userID TEXT NOT NULL, bookID TEXT NOT NULL, rating TEXT NOT NULL, FOREIGN KEY(userID) REFERENCES users, FOREIGN Key(bookID), REFERENCES books, );");


importBooks()          