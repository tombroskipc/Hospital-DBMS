from flask import Blueprint, render_template, request, redirect, url_for, flash, session

main = Blueprint('main', __name__)

user_list_test = {}
user_list_test.clear()

PASSWORD = 'password'

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register')
def register():
    if session.get('logged_in'):
        flash('You are already logged in!')
    else:
        flash('Please login!')
    return render_template('register.html')

@main.route('/', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    if email in user_list_test:
        if password == user_list_test[email][PASSWORD]:
            flash('You have successfully logged in')
            session['logged_in'] = True
            session['email'] = email

            return redirect(url_for('main.index'))
        flash('Wrong password')
        return redirect(url_for('main.index'))
    flash('User does not exist')
    return redirect(url_for('main.profile'))

@main.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('password_repeat')
    if password != confirm:
        flash('Passwords do not match')
        return redirect(url_for('main.register'))
    if email not in user_list_test:
        user_list_test[email] = {'name': name, 'password': password}
        flash('You have successfully registered!')
        print(user_list_test)
        return redirect(url_for('main.index'))
    else:
        flash('You have already registered!')
        return redirect(url_for('main.register'))

@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('You have successfully logged out')
    return redirect(url_for('main.index'))

@main.route('/profile')
def profile():
    return render_template('user//profile.html')

@main.route('/edit-profile')
def editprofile():
    return render_template('user//edit-profile.html')