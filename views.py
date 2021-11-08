from flask import Blueprint, render_template, request, redirect, url_for, flash, session

main = Blueprint('main', __name__)

user_list_test = {}
user_list_test.clear()

PASSWORD = 'password'

@main.route('/')
def index():
    if 'logged_in' not in session:
        return render_template('index.html')
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        return render_template('dashboard.html')
    flash('Please login!')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['POST'])
def dashboard_post():
    if session.get('logged_in'):
        if request.form['record_choice'] == 'patient_record':
            return redirect(url_for('main.patient_record'))
    flash('Please login!')
    return redirect(url_for('main.index'))


@main.route('/register')
def register():
    if session.get('logged_in'):
        flash('You are already logged in!')
    else:
        flash('Please login!')
    return render_template('register.html')

@main.route('/', methods=['POST'])
def login_post():
    if 'logged_in' not in session:
        email = request.form['email']
        password = request.form['password']
        if email in user_list_test:
            if password == user_list_test[email][PASSWORD]:
                session['logged_in'] = True
                session['email'] = email
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
        return redirect(url_for('main.index'))
    else:
        flash('You have already registered!')
        return redirect(url_for('main.register'))

@main.route('/logout')
def logout():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    session.pop('logged_in', None)
    session.pop('email', None)
    flash('You have successfully logged out')
    return redirect(url_for('main.index'))

@main.route('/profile')
def profile():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('user//profile.html')

@main.route('/edit-profile')
def editprofile():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('user//edit-profile.html')

@main.route('/patient_record')
def patient_record():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('dashboard//patient.html')

@main.route('/patient_record', methods=['POST'])
def patient_record_post():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    
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