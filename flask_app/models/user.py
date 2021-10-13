from logging import NullHandler
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models import painting

class User:
    def __init__(self, data) -> None:
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.purchased = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        user_id = connectToMySQL("art").query_db(query, data)
        return user_id

    @staticmethod
    def validate_reg(data):
        email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
        password_regex = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$')
        # requires 8-20 chars, 1 upper, 1 lower, 1 number.
        is_valid = True
        
        if len(data["first_name"]) < 2:
            flash("A first name is required.")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("A last name is required.")
        if not email_regex.match(data["email"]):
            flash("Invalid email address.")
            is_valid = False  
        if data["password"] != data["confirm_pass"]:
            flash("Passwords don't match.")
            is_valid = False
        if not password_regex.match(data["password"]):                  
            flash("Password doesn't meet criteria.")
            is_valid = False
        
        return is_valid

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        user_db = connectToMySQL("art").query_db(query, data)
        if len(user_db) < 1:
            return False
        return (User(user_db[0]))

    @classmethod
    def get_users_purchased(cls, data):
        query = "SELECT * FROM users LEFT JOIN purchases on purchases.user_id = users.id LEFT JOIN paintings ON purchases.painting_id = paintings.id LEFT JOIN users AS users2 ON paintedby_id = users2.id WHERE users.id = %(id)s"
        users_purchased_db = connectToMySQL("art").query_db(query, data)
        if len(users_purchased_db) < 1:
            return False
        user =  User(users_purchased_db[0])
        for row in users_purchased_db:
            painting_data = {
                "id": row["paintings.id"],
                "title": row["title"],
                "description": row["description"],
                "price": row["price"],
                "quantity": row["quantity"],
                "paintedby_id": row["paintedby_id"],
                "created_at": row["paintings.created_at"],
                "updated_at": row["paintings.updated_at"]
            }
            purchased_painting = painting.Painting(painting_data)
            print(row["users2.first_name"])
            if row["users2.first_name"]:
                purchased_painting.paintedby = row["users2.first_name"]+ row["users2.last_name"]
            else:
                purchased_painting.paintedby = False
            print(purchased_painting.paintedby)
            if not purchased_painting.paintedby == False:
                user.purchased.append(purchased_painting)
        return user

    @classmethod
    def buy_painting(cls, data):
        query = "INSERT INTO purchases (user_id, painting_id) VALUES (%(user_id)s, %(painting_id)s)"
        return connectToMySQL("art").query_db(query, data)
        