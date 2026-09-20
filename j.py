"""
FLASK APPLICATION MAIN FILE
This file controls routing, logic, session, cookies, file upload, and template rendering.
"""
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.secret_key = "secrete123"
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
@app.route('/')
def home():
    """
    Home page route
    Renders the home.html template
    """
    return render_template('home.html')
@app.route('/hello/<name>')
def hello(name):
    """
    Variable route example
    Captures <name> from URL and displays a personalized message
    """
    return f"Hello, {name}, welcome to Flask!"
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login route to handle GET and POST requests
    GET: Displays login page
    POST: Process login form and store username in session
    """
    if request.method == 'POST':
        username = request.form['username']
        session['user'] = username
        flash("Login successful!")
        return redirect(url_for('dashboard'))
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    """
    Dashboard route
    Displays a personalized dashboard using session data
    """
    user = session.get('user')
    return render_template('dashboard.html', user=user)
@app.route('/logout')
def logout():
    """
    Logout route
    Clears session data and redirects to home page
    """
    session.pop('user', None)
    flash("Logged out successfully!")
    return redirect(url_for('home'))
@app.route('/set_cookie')
def set_cookie():
    """
    set a browser cookie
    """
    response = make_response("Cookie has been set")
    response.set_cookie('course', 'Flask')
    return response
@app.route('/get_cookie')
def get_cookie():
    """
    Retrieve a browser cookie
    """
    course = request.cookies.get('course')
    return f"Cookie value is: {course}"
@app.route('/upload', methods=["GET", "POST"])
def upload():
    """
    File upload route
    GET: Render upload page
    POST: Handle file upload, save file, and display flash message
    """
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            flash("No file selected", "error")
            return redirect(url_for("upload"))

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("File uploaded successfully!", "success")
        return redirect(url_for("upload"))
    return render_template("upload.html")
@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error page
    """
    return render_template('404.html'), 404
if __name__ == '__main__':
    """
    Run Flask development server with debug mode enabled
    """
    app.run(debug=True)


    