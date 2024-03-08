
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# The above is used when we do login registration, flask-bcrypt should already be in your env check the pipfile

# Remember 'fat models, skinny controllers' more logic should go in here rather than in your controller. Your controller should be able to just call a function from the model for what it needs, ideally.


class User:
    db = "cookbook_1.0_schema"  # which database are you using for this project

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        # What changes need to be made above for this project?
        # What needs to be added here for class association?

    @classmethod
    def register_user(cls, user_data):
        if not cls.validate_user_info(user_data):
            return False
        user_data = user_data.copy()
        user_data['password'] = bcrypt.generate_password_hash(
            user_data['password'])
        query = """
                INSERT INTO users (first_name, last_name, user_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(user_name)s, %(email)s, %(password)s)
                ;"""
        registered_user = connectToMySQL(cls.db).query_db(query, user_data)
        session['user_id'] = registered_user
        session['user_login'] = f"{user_data['user_name']}"
        return registered_user

    @classmethod
    def login_user(cls, data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_login'] = f"{this_user.user_name}"
                return True
        flash('Your login information was incorrect!  Please try again!')
        return False
    # Read Users Models

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    # Update Users Models

    # Delete Users Models

    @staticmethod
    def validate_user_info(data):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!, Please use a valid email address!!")
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('Email has been used.  Please use a different email!')
            is_valid = False
        if len(data['first_name']) < 3:
            flash('Invalid First Name.  Must be a minimum of 3 characters!')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Invalid Last Name.  Must be a minimum of 3 characters!')
            is_valid = False
        if len(data['user_name']) < 3:
            flash('Invalid User Name.  Must be a minimum of 3 characters!')
            is_valid = False
        if len(data['password']) < 8:
            flash('Invalid Password.  Must be at least 8 characters!')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match!  Please try again.')
            is_valid = False
        return is_valid
