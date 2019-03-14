"""
Module name  : api_ex_2_template_2.py
Purpose      : Define two endpoints 'home' and 'about' and use html files in the templates folder to implement them
Functionality: Apply Flask render_template function to integrate the Jinja2 template engine with the application
  - home_2.html and about_2.html are files in the templates folder
    - Run the HTML via render_template
    - The common code for title for home_2.html and about_2.html is defined in layout_2.html in the templates folder
    - Use block content defined common code
Testing
   - Visit the below URLs to test the endpoints
     - http://127.0.0.1:5000/home
     - http://127.0.0.1:5000/about
Notes:
  The code is adaped from "Python Flask Tutorial: Full-Featured Web App Part 2 - Templates" by Corey Schafer
  - Please refer to https://www.youtube.com/watch?v=QnDWIZuWYW0 for thr details
  - Can add HTML inside the Python code. Or create a html file and use  render_template to run the html file.

Modification History
mmmyy        Author        Description
==================================================================================================================================
Mar 2019   Sophia Yue      Initiation
"""
from flask import Flask, render_template, url_for
app = Flask(__name__)
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home_2.html', posts=posts)
@app.route("/about")
def about():
    return render_template('about_2.html', title='About')
if __name__ == '__main__':
    app.run(debug=True)
