from app import app, db, bcrypt
from flask import render_template, request, redirect, session, url_for
from models import User

@app.route('/')
def index():
    return 'Backend Running'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect('/dashboard')
        return 'Invalid credentials'
    return 'Login Page'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return 'Register Page'

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f'Welcome User {session["user_id"]}'
    return redirect('/login')