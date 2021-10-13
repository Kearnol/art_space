from flask_app import app
from flask import render_template, redirect, request, session
from flask import flash
from flask_app.models.painting import Painting

@app.route("/addpainting")
def add_painting():
    if "user_id" not in session:
        flash("Must be logged in.")
        return redirect ("/login")
    return render_template("addpainting.html")

@app.route("/savepainting", methods=["POST"])
def save_painting():
    if not Painting.validate_add_edit(request.form):
        return redirect ("/addpainting")
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "quantity": request.form["quantity"],
        "paintedby_id": session["user_id"]
    }
    painting_id = Painting.save_painting(data)
    return redirect("/dashboard")

@app.route("/editpainting/<int:id>")
def edit_painting(id):
    if "user_id" not in session:
        flash("Must be logged in.")
        return redirect ("/login")
    data = {
        "id": id
    }
    painting = Painting.get_painting_by_id(data)
    return render_template("editpainting.html", painting = painting)

@app.route("/updatepainting/<int:id>", methods=["POST"])
def update_painting(id):
    if not Painting.validate_add_edit(request.form):
        return redirect("/editpainting/"+str(id))
    data = {
        "id": id,
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "quantity": request.form["quantity"]
    }
    Painting.update_painting(data)
    return redirect("/editpainting/"+str(id))

@app.route("/viewpainting/<int:id>")
def view_painting(id):
    if "user_id" not in session:
        flash("Must be logged in.")
        return redirect ("/login")
    data = {
        "id":id
    }
    painting = Painting.get_painting_by_id(data)

    purchases = Painting.get_num_purchased(data)
    if purchases < painting.quantity:
        buy = True
    else:
        buy = False

    return render_template("viewpainting.html", painting=painting, purchases=purchases, buy=buy)


@app.route("/deletepainting/<int:id>")
def delete_painting(id):
    if "user_id" not in session:
        flash("Must be logged in.")
        return redirect ("/login")
    data = {
        "id":id
    }
    Painting.delete_painting(data)
    return redirect("/dashboard")