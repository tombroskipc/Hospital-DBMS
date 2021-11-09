from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import mysql
main = Blueprint('main', __name__)


PASSWORD = 'password'
LOGGED_IN = 'logged_in'
@main.route('/')
def index():
    if LOGGED_IN not in session:
        return render_template('index.html')
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    if session.get(LOGGED_IN):
        return render_template('dashboard.html')
    flash('Please login!')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['POST'])
def dashboard_post():
    if session.get(LOGGED_IN):
        if request.form['record_choice'] == 'patient_record':
            return redirect(url_for('main.patient_record'))
    flash('Please login!')
    return redirect(url_for('main.index'))


@main.route('/register')
def register():
    if session.get(LOGGED_IN):
        flash('You are already logged in!')
    else:
        flash('Please login!')
    return render_template('register.html')

@main.route('/', methods=['POST'])
def login_post():
    if LOGGED_IN not in session:
        id = int(request.form['id'])
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Doctor WHERE Doc_id={id} AND pass={password}")
        account = cur.fetchone()
        if account:
            session[LOGGED_IN] = True
            session['id'] = id
            return redirect(url_for('main.dashboard'))
    flash('Please check your id or password')
    return redirect(url_for('main.index'))


# @main.route('/register', methods=['POST'])
# def register_post():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     confirm = request.form.get('password_repeat')
#     if password != confirm:
#         flash('Passwords do not match')
#         return redirect(url_for('main.register'))
#     if email not in user_list_test:
#         user_list_test[email] = {'name': name, 'password': password}
#         flash('You have successfully registered!')
#         print(user_list_test)
#         return redirect(url_for('main.index'))
#     else:
#         flash('You have already registered!')
#         return redirect(url_for('main.register'))

@main.route('/logout')
def logout():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    session.pop(LOGGED_IN, None)
    session.pop('email', None)
    flash('You have successfully logged out')
    return redirect(url_for('main.index'))

@main.route('/profile')
def profile():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('user//profile.html')

@main.route('/edit-profile')
def editprofile():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('user//edit-profile.html')

@main.route('/patient_record')
def patient_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Patient")
    patients = list(cur.fetchall())
    return render_template('dashboard//patient.html', patients=patients)

@main.route('/patient_record', methods=['POST'])
def patient_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    search_input = request.form.get('search_input')
    return redirect(url_for('main.index'))

@main.route('/make-appointment')
def make_appointment():
    return render_template('services//appointment.html')

@main.route('/nursing-service')
def nursing_service():
    return render_template('services//nurse.html')

@main.route('/book-test')
def book_test():
    return render_template('services//test.html')

@main.route('/find-doctor')
def find_doctor():
    return render_template('search//doctor.html')

@main.route('/find-medicine')
def find_medicine():
    return render_template('search//medicine.html')