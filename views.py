from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import mysql
import re
main = Blueprint('main', __name__)
import utils

PASSWORD = 'password'
LOGGED_IN = 'logged_in'
@main.route('/')
def index():
    session['today_choice'] = utils.get_today_web_choice()
    print(session['today_choice'])
    if LOGGED_IN not in session:
        return render_template('index.html')
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard')
def dashboard():
    if session.get(LOGGED_IN):
        return render_template('dashboard.html')
    return redirect(url_for('main.index'))

@main.route('/dashboard', methods=['POST'])
def dashboard_post():
    if session.get(LOGGED_IN):
        if request.form['record_choice'] == 'patient_record':
            return redirect(url_for('record.patient_record'))
        elif request.form['record_choice'] == 'medical_record':
            return redirect(url_for('record.medical_record'))
        elif request.form['record_choice'] == 'medicine_record':
            return redirect(url_for('record.medicine_record'))
        elif request.form['record_choice'] == 'bill_record':
            return redirect(url_for('record.bill_record'))
        elif request.form['record_choice'] == 'bill_report':
            return redirect(url_for('record.bill_report'))
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
        cur.close()
        if account:
            session[LOGGED_IN] = True
            session['doc_id'] = id
            session['type'] = 'doctor'
            session['name'] = account[1]
            return redirect(url_for('main.dashboard'))
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Nurse WHERE Nur_id={id} AND pass={password}")
        account = cur.fetchone()
        cur.close()
        if account:
            session[LOGGED_IN] = True
            session['nur_id'] = id
            session['type'] = 'nurse'
            session['name'] = account[1]
            return redirect(url_for('main.dashboard'))
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * FROM Accountant WHERE Acct_id={id} AND pass={password}")
        account = cur.fetchone()
        cur.close()
        if account:
            session[LOGGED_IN] = True
            session['acct_id'] = id
            session['type'] = 'Accountant'
            session['name'] = account[1]
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
    session.pop('id', None)
    flash('You have successfully logged out')
    return redirect(url_for('main.index'))

@main.route('/profile')
def profile():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    
    return render_template('user//profile.html')


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
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Doctor")
    doctors = list(cur.fetchall())
    cur.close()
    return render_template('search//doctor.html', doctors=doctors)

@main.route('/find-medicine')
def find_medicine():
    cur = mysql.connection.cursor()
    query_input = """
    SELECT Medicine.Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer, Dis_name
    FROM Medicine, Disease, Cure
    WHERE Mdc_name LIKE '%' AND Medicine.Mdc_id = Cure.Mdc_id AND Cure.Dis_id = Disease.Dis_id;
    """
    cur.execute(query_input)
    medicines = list(cur.fetchall())
    cur.close()
    return render_template('search//medicine.html', medicines=medicines)

@main.route('/find-medicine', methods=['POST'])
def find_medicine_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # filter search
    search_input = (str(request.form.get('search_input')).lower()).strip()
    search_input = re.sub(' +', ' ', search_input)
    print(search_input)
    if len(search_input) == 0:
        return redirect(url_for('main.find_medicine'))

    search_result = []
    # query by name
    try:
        cur = mysql.connection.cursor()
        query_input = f"""
        SELECT Medicine.Mdc_id, Mdc_name, Dis_name, Price, MFG, EXP, Quantity, Manufacturer
        FROM Medicine, Disease, Cure
        WHERE LOWER(Mdc_name) LIKE '%{search_input}%' AND Medicine.Mdc_id = Cure.Mdc_id AND Cure.Dis_id = Disease.Dis_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
    except:
        pass
    # query by disease name
    try:
        query_input = f"""
        SELECT Medicine.Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer, Disease.Dis_name
        FROM Medicine, Disease, Cure
        WHERE Dis_name LIKE '%{search_input}%' AND Disease.Dis_id = Cure.Dis_id AND Cure.Mdc_id = Medicine.Mdc_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
    except:
        pass
    # query by price
    try:
        search_input = int(search_input)
        cur.execute(f"SELECT * FROM Medicine WHERE Price = '{search_input}'")
        search_result = search_result + list(cur.fetchall())
    except:
        pass
    cur.close()
    return render_template('search//medicine.html', medicines=search_result)