from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import mysql
from utils import get_year, get_random_re_id
import re
record = Blueprint('record', __name__)

LOGGED_IN = 'logged_in'

@record.route('/patient-record/<int:ssn>')
def view_record(ssn):
    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT Patient.Ssn, Patient.Pat_name, Patient.Sex, Patient.DOB, Patient.Age, Patient.Address, Patient.Tel_no, Patient.Email, Insurance_company.InsCo_name, Patient.Start_date, Patient.End_date
    FROM Patient, Insurance_company
    WHERE Patient.Ssn LIKE '%{ssn}%' AND Patient.InsCo_id = Insurance_company.InsCo_id;
    """
    cur.execute(query_input)
    record = cur.fetchone()
    cur.close()
    return render_template('record//patient.html', record=record)

@record.route('/edit-profile/<int:ssn>')
def edit_profile(ssn):
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT Patient.Ssn, Patient.Pat_name, Patient.Sex, Patient.DOB, Patient.Age, Patient.Address, Patient.Tel_no, Patient.Email, Insurance_company.InsCo_name, Patient.Start_date, Patient.End_date
    FROM Patient, Insurance_company
    WHERE Patient.Ssn LIKE '%{ssn}%' AND Patient.InsCo_id = Insurance_company.InsCo_id;
    """
    cur.execute(query_input)
    record = cur.fetchone()
    return render_template('record//edit-profile.html', record=record)

@record.route('/edit-profile/<int:ssn>', methods=['POST'])
def edit_profile_post(ssn):
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    new_name = request.form['name']
    new_email = request.form['email']
    new_phone = request.form['phone']
    new_DOB = request.form['DOB']
    new_address = request.form['address']
    new_start_date = request.form['start_date']
    new_end_date = request.form['end_date']
    cur = mysql.connection.cursor()
    cur.execute(f"UPDATE Patient SET Pat_name = '{new_name}', Email = '{new_email}', Tel_no = '{new_phone}', DOB = '{new_DOB}', Address = '{new_address}', Start_date = '{new_start_date}', End_date = '{new_end_date}' WHERE Ssn = {ssn}")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('record.view_record', ssn=ssn))

@record.route('/delete-profile/<int:ssn>')
def delete_profile(ssn):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Patient WHERE Ssn = {ssn}")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('main.index'))

@record.route('/add-record')
def add_profile():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Insurance_company")
    ins_companies = cur.fetchall()
    cur.close()
    return render_template('record//add-profile.html', ins_companies=ins_companies)

@record.route('/add-record', methods=['POST'])
def add_profile_post():
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    new_ssn = request.form['ssn']
    new_name = request.form['name']
    new_sex = request.form['sex']
    new_email = request.form['email']
    new_phone = request.form['phone']
    new_DOB = request.form['DOB']
    new_age = get_year() - int(new_DOB[:4])
    new_address = request.form['address']
    new_InsCo_id = request.form['ins_co']
    new_start_date = request.form['start_date']
    new_end_date = request.form['end_date']
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO Patient (Ssn, Pat_name, Sex, Email, Tel_no, DOB, Age, Address, InsCo_id, Start_date, End_date) VALUES ('{new_ssn}', '{new_name}', '{new_sex}', '{new_email}', '{new_phone}', '{new_DOB}', '{new_age}', '{new_address}', {new_InsCo_id}, '{new_start_date}', '{new_end_date}')")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('record.patient_record'))


@record.route('/patient-record')
def patient_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Patient")
    patients = list(cur.fetchall())
    cur.close()
    return render_template('dashboard//patient.html', patients=patients)

@record.route('/patient-record', methods=['POST'])
def patient_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # filter search
    search_input = (str(request.form.get('search_input')).lower()).strip()
    input_date = str(request.form.get('input_date'))
    search_input = re.sub(' +', ' ', search_input)

    print(search_input)
    print('input date: ' + input_date)
    search_result = []
    cur = mysql.connection.cursor()
    if len(search_input) == 0 and len(input_date) == 0:
        return redirect(url_for('record.patient_record'))
    if len(search_input) > 0:
        # query by name
        cur.execute(f"SELECT * FROM Patient WHERE LOWER(Pat_name) LIKE '%{search_input}%' ")
        search_result += list(cur.fetchall())
        # query by gender
        if search_input == 'men' or search_input == 'male':
            cur.execute(f"SELECT * FROM Patient WHERE Sex='M'")
            search_result += list(cur.fetchall())
        elif search_input == 'woman' or search_input == 'female':
            cur.execute(f"SELECT * FROM Patient WHERE Sex='F'")
            search_result += list(cur.fetchall())

        # query by age
        try:
            search_input = int(search_input)
            cur.execute(f"SELECT * FROM Patient WHERE Age = '{search_input}'")
            search_result = search_result + list(cur.fetchall())
        except:
            pass

    # query by DOB, start_date or end_date
    try:
        if len(input_date) > 0:
            cur.execute(f"SELECT * FROM Patient WHERE DOB = '{input_date}'")
            search_result += list(cur.fetchall())
            print(search_result)
    except:
        pass
    cur.close()
    return render_template('dashboard//patient.html', patients=search_result)

@record.route('/medicine-record')
def medicine_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    query_input = """
    SELECT Medicine.Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer, Dis_name
    FROM Medicine, Disease, Cure
    WHERE Mdc_name LIKE '%' AND Medicine.Mdc_id = Cure.Mdc_id AND Cure.Dis_id = Disease.Dis_id;
    """
    cur.execute(query_input)
    medicines = list(cur.fetchall())
    cur.close()
    return render_template('dashboard//medicine.html', medicines=medicines)

@record.route('/medicine-record', methods=['POST'])
def medicine_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # filter search
    search_input = (str(request.form.get('search_input')).lower()).strip()
    search_input = re.sub(' +', ' ', search_input)
    print(search_input)
    if len(search_input) == 0:
        return redirect(url_for('record.medicine_record'))

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
    return render_template('dashboard//medicine.html', medicines=search_result) 

@record.route('/add-medicine')
def add_medicine():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Disease")
    diseases = list(cur.fetchall())
    cur.close()
    return render_template('record//add-medicine.html', diseases=diseases)

@record.route('/add-medicine', methods=['POST'])
def add_medicine_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # get input
    mdc_name = str(request.form.get('mdc_name'))
    price = int(request.form.get('price'))
    mfg = str(request.form.get('mfg'))
    print(mfg)
    exp = str(request.form.get('exp'))
    quantity = int(request.form.get('quantity'))
    manufacturer = str(request.form.get('manufacturer'))
    dis_id = str(request.form.get('dis_id'))
    # validate input
    if len(mdc_name) == 0:
        flash('Medicine name cannot be empty!')
        return redirect(url_for('record.add_medicine'))
    if price <= 0:
        flash('Price must be greater than 0!')
        return redirect(url_for('record.add_medicine'))
    if len(mfg) == 0:
        flash('Manufacturer cannot be empty!')
        return redirect(url_for('record.add_medicine'))
    if len(exp) == 0:
        flash('Expiration date cannot be empty!')
        return redirect(url_for('record.add_medicine'))
    if quantity <= 0:
        flash('Quantity must be greater than 0!')
        return redirect(url_for('record.add_medicine'))
    if len(manufacturer) == 0:
        flash('Manufacturer cannot be empty!')
        return redirect(url_for('record.add_medicine'))
    if len(dis_id) == 0 or dis_id == 'Choose...':
        flash('Disease name cannot be empty!')
        return redirect(url_for('record.add_medicine'))
    # insert into database
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT MAX(Mdc_id) FROM Medicine')
    mdc_id = int(cur.fetchone()[0]) + 1
    cur.execute(f"INSERT INTO Medicine (Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer) VALUES ('{mdc_id}', '{mdc_name}', '{price}', '{mfg}', '{exp}', '{quantity}', '{manufacturer}')")
    cur.execute(f"INSERT INTO Cure (Mdc_id, Dis_id) VALUES ('{mdc_id}', '{dis_id}')")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('record.medicine_record'))
    


@record.route('/add-report/<int:ssn>')
def add_medical_record_id(ssn):
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('record//add-record.html', pat_ssn=ssn)

@record.route('/add-report')
def add_medical_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    return render_template('record//add-record.html')

@record.route('/medicine-record-delete/<int:id>')
def medicine_record_delete(id):
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM Medicine WHERE Med_id={id}")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('record.medicine_record'))

@record.route('/medical-record')
def medical_record():
    return render_template('dashboard//medical-record.html')

@record.route('/medical-record', methods=['POST'])
def medical_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))

    # search by between date
    search_result = []
    start_date = str(request.form.get('start_date'))
    end_date = str(request.form.get('end_date'))
    print('Start date: ' + start_date)
    print('End date: ' + end_date)
    if len(start_date) != 0 and len(end_date) != 0:
        cur = mysql.connection.cursor()
        query_input = f"""
        SELECT Report.Re_id, Pat_name, Doc_name, Category, Description, Date
        FROM Report, Doctor, Patient
        WHERE (Date BETWEEN '{start_date}' AND '{end_date}') AND Report.Ssn = Patient.Ssn AND Report.Doc_id = Doctor.Doc_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
        cur.close()
        print(search_result)
        return render_template('dashboard//medical-record.html', reports=search_result)
        
    # filter search
    search_input = (str(request.form.get('search_input')).lower()).strip()
    search_input = re.sub(' +', ' ', search_input)
    print(search_input)
    if len(search_input) == 0:
        return redirect(url_for('record.medical_record'))
    # query by patient name
    try:
        cur = mysql.connection.cursor()
        query_input = f"""
        SELECT Report.Re_id, Pat_name, Doc_name, Category, Description, Date
        FROM Report, Doctor, Patient
        WHERE LOWER(Pat_name) LIKE '%{search_input}%' AND Report.Ssn = Patient.Ssn AND Report.Doc_id = Doctor.Doc_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
    except:
        pass
    cur.close()
    return render_template('dashboard//medical-record.html', reports=search_result)

@record.route('/add-report', methods=['POST'])
def add_medical_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # get patient information
    cur = mysql.connection.cursor()
    ssn = request.form.get('ssn')
    cur.execute(f"SELECT EXISTS(SELECT * FROM Patient WHERE Ssn = '{ssn}');")
    check_ssn = cur.fetchone()[0]
    if check_ssn == 0:
        flash('Patient does not exist!')
        return redirect(url_for('record.add_medical_record'))
    doc_id = request.form.get('doc_id')
    cur.execute(f"SELECT EXISTS(SELECT * FROM Doctor WHERE Doc_id = '{doc_id}');")
    check_doc_id = cur.fetchone()[0]
    print(check_doc_id)
    if check_doc_id == 0:
        flash('Doctor does not exist!')
        return redirect(url_for('record.add_medical_record'))
    category = str(request.form.get('category'))
    description = str(request.form.get('description'))
    date = str(request.form.get('date'))
    check_re = 1
    while check_re != 0:
        re_id = get_random_re_id()
        cur.execute(f"SELECT EXISTS(SELECT * FROM Report WHERE Re_id = {re_id});")
        check_re = cur.fetchone()[0]
        print('checking re_id: ' + str(get_random_re_id())  + '    '+ str(check_re))
    cur.execute(f"INSERT INTO Report VALUES('{re_id}', '{category}', '{description}', '{date}', '{doc_id}', '{ssn}');")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('record.medical_record'))