from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import redirect
from flask import flash

class Painting:
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.price = data["price"]
        self.quantity = data["quantity"]
        self.paintedby_id = data["paintedby_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = []

    @classmethod
    def validate_add_edit(cls,data):
        is_valid = True
        if len(data["title"]) < 2:
            flash("Title required")
            is_valid = False
        if len(data["description"]) < 10:
            flash("Description is too short. It must be a minimum of 10 characters long.")
            is_valid = False
        if not data["price"]:
            flash("Error. You entered no price value")
            is_valid = False
            return is_valid
        if not data["quantity"]:
            flash("Error. You entered no quantity value")
            is_valid = False
            return is_valid
        if float(data["price"]) <= 0:
            flash("Price cannot be $0.00. ")
            is_valid = False
        if int(data["quantity"]) <= 0:
            flash("Quantity cannot be 0.")
            is_valid = False
        return is_valid

    @classmethod
    def save_painting(cls, data):
        query = "INSERT INTO paintings (title, description, price, quantity, paintedby_id) VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, %(paintedby_id)s)"
        flash("Painting added!")
        return connectToMySQL("art").query_db(query, data)

    @classmethod
    def get_all_paintings(cls):
        query = "SELECT * FROM paintings JOIN users on paintedby_id = users.id"
        all_db_paintings = connectToMySQL("art").query_db(query)
        all_paintings = []
        for row in all_db_paintings:
            painting = Painting(row)
            user_data = {
                "id":row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            painting.paintedby = User(user_data)
            all_paintings.append(painting)
        return all_paintings

    @classmethod
    def get_painting_by_id(cls, data):
        query = "SELECT * FROM paintings JOIN users on users.id = paintedby_id WHERE paintings.id = %(id)s"
        painting_db = connectToMySQL("art").query_db(query, data)
        painting = Painting(painting_db[0])
        for row in painting_db:
            user_data = {
                    "id":row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"],
                }
        painting.paintedby = User(user_data)
        return painting
        #returns the instance of the painting

    @classmethod
    def update_painting(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, quantity=%(quantity)s WHERE id = %(id)s"
        flash("Success - painting updated!")
        return connectToMySQL("art").query_db(query,data)

    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(id)s"
        return connectToMySQL("art").query_db(query,data)

    @classmethod
    def get_num_purchased(cls, data):
        query = "SELECT COUNT(user_id) AS purchases FROM purchases WHERE painting_id = %(id)s GROUP BY painting_id"
        purchases_db = connectToMySQL("art").query_db(query, data)
        print(purchases_db)
        if len(purchases_db)< 1:
            purchases = 0
        else:
            purchases = purchases_db[0]["purchases"]
        print(purchases)
        return purchases