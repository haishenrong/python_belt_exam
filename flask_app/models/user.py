from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app import app
from flask.helpers import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z0-9]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.count = None

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"
        insertResult = connectToMySQL('paintings_schema').query_db( query, data )
        print(insertResult)
        return insertResult

    @classmethod
    def get_one_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('paintings_schema').query_db( query, data )
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL('paintings_schema').query_db( query, data )
        return cls(result[0])

    @staticmethod
    def validate_form(data):
        is_valid = True # we assume this is true
        query = "SELECT COUNT(email) FROM users WHERE email = %(email)s;"
        result = connectToMySQL('paintings_schema').query_db( query, data )

        if not NAME_REGEX.match(data['first_name']):
            flash("First Name must be at least 2 letters no spaces.")
            is_valid = False
        if not NAME_REGEX.match(data['last_name']):
            flash("Last Name must be at least 2 letters no spaces.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email must be in valid format (ex: aba@example.com)")
            is_valid = False
        if result[0]['COUNT(email)'] > 0:
            flash("Email already registered.")
            is_valid = False
        if not PASSWORD_REGEX.match(data['password']):
            flash("Passwords must be atleast 8 characters. With one uppercase letter and one number")
            is_valid = False
        if data['password'] != data['cPassword']:
            flash("Passwords must be the same.")
            is_valid = False
        #if is_valid:
            #flash("Registration Sucessful.")
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True    
        if not data['loggedUser']:
            flash("Invalid Email/Password")
            is_valid = False
        elif not bcrypt.check_password_hash(data['loggedUser'].password, data['password']):
            flash("Invalid Email/Password")
            is_valid = False
        return is_valid   
    

    # come undone
