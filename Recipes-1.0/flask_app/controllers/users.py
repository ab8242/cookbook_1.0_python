from flask_app import app
from flask import render_template, redirect, request, session
# import entire file, rather than class, to avoid circular imports
from flask_app.models import user, recipe
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request

# Create New User


@app.route('/create/user', methods=['POST'])
def register_user():
    if user.User.register_user(request.form):
        return redirect('/dashboard')
    return redirect('/register')


@app.route('/register')
def register():
    return render_template('register_page.html')

# Login previously registered User


@app.route('/login', methods=['POST'])
def login():
    if user.User.login_user(request.form):
        return redirect('/dashboard')
    return redirect('/')


@app.route('/')
def index():
    return render_template('index.html')

# Read Users Controller to main page


@app.route('/dashboard')
def dashboard_page():
    if 'user_id' not in session:
        return redirect('/')
    all_recipes = recipe.Recipe.view_all_recipes_with_authors()
    return render_template('dashboard.html', all_recipes=all_recipes)

# Logout of App


@app.route('/logout')
def logout():
    if 'user_id' not in session:
        return redirect('/')
    session.clear()
    return redirect('/')


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal


# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.
