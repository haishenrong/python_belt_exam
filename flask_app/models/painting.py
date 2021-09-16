from flask_app.config.mysqlconnection import connectToMySQL
from flask.helpers import flash
from flask_app.models import user
import re

PRICE_REGEX = re.compile(r'^(([1-9]\d{0,}(,\d{3})*)|0)?\.\d{2}$')
QUANTITY_REGEX = re.compile(r'^([1-9]\d{0,})$')

class Painting:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data ['quantity']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.author = None

    @classmethod
    def get_all_with_authors(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL('paintings_schema').query_db(query)
        paintings = []
        for row in results:
            painting = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            painting.author = user.User(user_data)
            paintings.append( painting )
        return paintings

    @classmethod
    def save_painting(cls, data):
        query = "INSERT INTO paintings ( title, description, price, quantity, created_at, updated_at, user_id ) VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, NOW(), NOW(), %(user_id)s);"
        insertResult = connectToMySQL('paintings_schema').query_db( query, data )
        return insertResult
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM paintings WHERE id = %(painting_id)s;"
        result = connectToMySQL('paintings_schema').query_db( query, data )
        return cls(result[0])

    @classmethod
    def get_by_id_with_author(cls, data):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id WHERE paintings.id = %(painting_id)s;"
        result = connectToMySQL('paintings_schema').query_db( query, data )
        painting = cls(result[0])
        user_data = {
            "id" : result[0]["users.id"],
            "first_name" : result[0]["first_name"],
            "last_name" : result[0]["last_name"],
            "email" : result[0]["email"],
            "password" : result[0]["password"],
            "created_at" : result[0]["users.created_at"],
            "updated_at" : result[0]["users.updated_at"]
        }
        painting.author = user.User(user_data)
        return painting

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('paintings_schema').query_db( query, data )
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL('paintings_schema').query_db( query, data )
    
    @staticmethod
    def validate_form(data):
        is_valid = True 
        if len(data['title']) < 2:
            flash("Title must be at least 2 characters.")
            is_valid = False
        if len(data['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        if not PRICE_REGEX.match(data['price']):
            flash("Price must be in valid decimal format")
            is_valid = False
        elif float(data['price']) <= 0:
            flash("Price must be positive")
            is_valid = False

        if not QUANTITY_REGEX.match(data['quantity']):
            flash("Quantity must be in valid integer format")
            is_valid = False
        elif float(data['quantity']) <= 0:
            flash("Quantity must be positive")
            is_valid = False
        return is_valid
    
    # Purchase stuff

    @classmethod
    def get_all_from_user(cls, data):
        query = "SELECT * , COUNT(paintings.id) FROM purchases LEFT JOIN paintings ON purchases.painting_id = paintings.id LEFT JOIN users ON paintings.user_id = users.id WHERE purchases.user_id = %(user_id)s GROUP BY paintings.id;"
        results = connectToMySQL('paintings_schema').query_db( query, data)
        paintings = []
        for row in results:
            painting = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            painting.author = user.User(user_data)
            painting.author.count = row['COUNT(paintings.id)']
            paintings.append( painting )
        return paintings

    @classmethod
    def get_paintings_sold(cls, data):
        query = "SELECT COUNT(user_id) FROM purchases WHERE painting_id = %(painting_id)s;"
        results = connectToMySQL('paintings_schema').query_db( query, data )
        return results[0]['COUNT(user_id)']
    
    @classmethod
    def purchase(cls, data):
        query = "INSERT INTO purchases (painting_id, user_id) VALUES (%(painting_id)s, %(user_id)s);"
        return connectToMySQL('paintings_schema').query_db( query, data )
    

    
    # come undone


    
