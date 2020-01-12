from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
import json

from user import User
from comment import Comment
from sale import Sale
from category import Category

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/sales')
def list_sales():
    return render_template('sales.html', sales = Sale.all())

@app.route('/sales/<int:id>')
def show_sale(id):
    sale = Sale.find(id)

    return render_template('sale.html', sale = sale)

@app.route('/sales/new', methods=['GET', 'POST'])
def new_sale():
    if request.method == 'GET':
        return render_template('new_sale.html', categories = Category.all())
    elif request.method == 'POST':
        category = Category.find(request.form['category_id'])
        values = (
            None,
            request.form['name'],
            request.form['model'],
            request.form['horsepower'],
            request.form['price'],
            request.form['year'],
            request.form['condition'],
            request.form['mileage'],
            category
        )
        Sale(*values).create()

        return redirect('/sales')

@app.route('/sales/<int:id>/delete', methods=['POST'])
def delete_sale(id):
    sale = Sale.find(id)
    sale.delete()

    return redirect('/sales')

@app.route('/sales/<int:id>/edit', methods=['GET', 'POST'])
def edit_sale(id):
    sale = Sale.find(id)
    if request.method == 'GET':
        return render_template('edit_sale.html', sale = sale, categories = Category.all())
    elif request.method == 'POST':
        sale.name = request.form['name']
        sale.model = request.form['model']
        sale.condition = request.form['condition']
        sale.price = request.form['price']
        sale.mileage = request.form['mileage']
        sale.year = request.form['year']
        sale.horsepower = request.form['horsepower']
        sale.category = Category.find(request.form['category_id'])
        sale.save()
        return redirect(url_for('show_sale', id = sale.id))

@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=Category.all())


@app.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    if request.method == "GET":
        return render_template("new_category.html")
    elif request.method == "POST":
        category = Category(None, request.form["name"])
        category.create()
        return redirect("/categories")


@app.route('/categories/<int:id>')
def get_category(id):
    return render_template("category.html", category=Category.find(id))


@app.route('/categories/<int:id>/delete')
def delete_category(id):
    Category.find(id).delete()
    return redirect("/categories")

@app.route('/comments/new', methods=['POST'])
def new_comment():
    if request.method == 'POST':
        sale = Sale.find(request.form['sale_id'])
        values = (None, sale, request.form['message'])
        Comment(*values).create()

        return redirect(url_for('show_sale', id=sale.id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password'])
        )
        User(*values).create()

        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return redirect('login')

if __name__ == '__main__':
    app.run()