"""
Module name:api_hugo_book_award.py
Purpose: Build an API to return data from database and returns data to users 
Input  :
    books.db with five columns id, published, author, title, and first_sentence.

Functionality 
  - Pulls in data from a database
 - Implements error handling
 - Filter books by publication date.
Visit the below URLs to test the new filtering capability
   http://127.0.0.1:5000/api/v1/resources/books/all
   http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis
   http://127.0.0.1:5000/api/v1/resources/books?author=Connie+Willis&published=1999
   http://127.0.0.1:5000/api/v1/resources/books?published=2010
Note
  - The code is adapted from the article "Creating Web APIs with Python and Flask" by Smyth Patrick.
    - Please refer to https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
  -   Please refer to "SQLite Python tutorial" in  http://zetcode.com/db/sqlitepythontutorial/ for For Sqlite  

  - Browse http://127.0.0.1:5000/api/v1/resources/books/all will return all of the available entries in our catalog in Json format
Modification History
mmyy        Author        Description
==================================================================================================================================
Mar 2019   Sophia Yue   Initiation
"""


import flask      # import flask library
from flask import request, jsonify
import sqlite3

"""
Define function for cursor dictionary
"""
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

"""
Creates a Flask instance
"""

app = flask.Flask(__name__)       
app.config["DEBUG"] = True	

"""
Define home page
 - Map URL path ('/') to function, home
 - The @ denotes a decorator, which allows the function, property, or class to be dynamically altered.
"""

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

"""
Display catalog
  - Pull data from Hugo database
  - A route to return all of the available entries in our catalog
  - jsonify(books) - Convert Python dictionary 'books' to Json format 
"""
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')   # Create a connection object
    conn.row_factory = dict_factory      # Use dictionary cursor instead of returning the data in a tuple of tuples
    cur = conn.cursor()                  # Create a cursor object
    all_books = cur.execute('SELECT * FROM books;').fetchall()  # The execute() is a method of the cursor and execute the SQL statement

    return jsonify(all_books)

"""
Error Handler
- In HTML responses
  200: “OK”(the expected data transferred)
  404: “Not Found” (no resource available )
"""

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
"""
Filter function
- Filtering by three different fields: id, published, and author 
"""

@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')    
    author = query_parameters.get('author')
    query = "SELECT * FROM books WHERE"
    to_filter = []
    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)


app.run()   # runs the application server
