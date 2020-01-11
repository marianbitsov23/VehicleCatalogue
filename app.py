from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
import json

from user import User

app = Flask(__name__)

@app.route('/')
def main_page():
    print('idvam')
    return render_template('main_page.html')

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

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        print('nachaloto na elifa')
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return redirect('login')
if __name__ == '__main__':
    app.run()