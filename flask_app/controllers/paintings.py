from flask import request, redirect, render_template, session
from flask_app.models.painting import Painting
from flask_app.models.user import User
from datetime import date
from flask_app import app
from flask.helpers import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

@app.route("/paintings/<int:id>")
def one_painting(id):
    if 'user_id' not in session: 
        flash('Please register or login')
        return redirect('/')
    data = {
        "user_id": session['user_id'],
        "painting_id": id
    }
    purchased = Painting.get_paintings_sold(data)
    painting = Painting.get_by_id_with_author(data)
    return render_template("painting.html", painting=painting, purchased = purchased)

@app.route("/paintings/new", methods = ['GET', 'POST'])
def new_painting():
    if request.method == 'GET':
        if 'user_id' not in session: 
            flash('Please register or login')
            return redirect('/')
        return render_template("new_painting.html")
    else: 
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "price": request.form['price'],
            "quantity": request.form['quantity'],
            "user_id": session['user_id']
        }
        if Painting.validate_form(data):
            data['price'] = float(data['price'])
            data['quantity'] = int(data['quantity'])
            Painting.save_painting(data)
            return redirect('/paintings')
        return redirect('/paintings/new')

@app.route("/paintings/edit/<int:id>", methods = ['GET', 'POST'])
def edit_painting(id):
    if request.method == 'GET':
        if 'user_id' not in session: 
            flash('Please register or login')
            return redirect('/')
        data = {
            "painting_id": id
        }
        painting = Painting.get_by_id(data)
        return render_template("edit_painting.html", painting = painting)
    else:
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "price": request.form['price'],
            "quantity": request.form['quantity'],
            "id": id
        }
        if Painting.validate_form(data):
            data['price'] = float(data['price'])
            data['quantity'] = int(data['quantity'])
            Painting.update(data)
            return redirect('/paintings')
        return redirect('/paintings/edit/'+str(id))

@app.route("/paintings/delete/<int:id>")
def delete(id):
    data = {
        "id": id
    }
    Painting.delete(data)
    return redirect("/paintings")

@app.route("/paintings/buy/<int:id>")
def buy(id):
    data = {
        "painting_id": id,
        "user_id": session['user_id']
    }
    Painting.purchase(data)
    return redirect("/paintings")