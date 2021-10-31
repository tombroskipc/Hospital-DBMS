from flask import Blueprint, render_template, request, redirect, url_for, flash

main = Blueprint('main', __name__)

user_list_test = {}
user_list_test.clear()

PASSWORD = 'password'

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    if email in user_list_test:
        if password == user_list_test[email][PASSWORD]:
            flash('You have successfully logged in')
            return redirect(url_for('main.index'))
        flash('Wrong password')
        return redirect(url_for('main.index'))
    flash('User does not exist')
    return redirect(url_for('main.index'))

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
        return redirect(url_for('main.register'))
    else:
        flash('You have already registered!')
        return redirect(url_for('main.register'))