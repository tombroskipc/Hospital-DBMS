from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import mysql
from utils import get_year, get_random_re_id, get_today, get_7_days_ago
import re
import graph
record = Blueprint('record', __name__)

LOGGED_IN = 'logged_in'

@record.route('/patient-record/<int:ssn>')
def view_record(ssn):
    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT Patient.Ssn, Patient.Pat_name, Patient.Sex, Patient.DOB, Patient.Age, Patient.Address, Patient.Tel_no, Patient.Email, Patient.InsCo_id, Patient.Start_date, Patient.End_date
    FROM Patient
    WHERE Patient.Ssn LIKE '%{ssn}%';
    """
    cur.execute(query_input)
    record = cur.fetchone()
    ins_name = f"""
    SELECT *
    FROM Insurance_company
    WHERE Insurance_company.InsCo_id LIKE '%{record[8]}%';
    """
    cur.execute(ins_name)
    ins_name = cur.fetchone()
    if ins_name is None:
        ins_name = "None"
    else:
        ins_name = ins_name[1]
    print(record)
        # query by report id
    reports = []
    num_reports = 0
    try:
        query_input = f"""
        SELECT Report.Re_id, Pat_name, Doc_name, Category, Description, Date
        FROM Report, Doctor, Patient
        WHERE Patient.Ssn = {record[0]} AND Report.Ssn = Patient.Ssn AND Report.Doc_id = Doctor.Doc_id;
        """
        cur.execute(query_input)
        reports += list(cur.fetchall())
        num_reports += len(reports)
    except:
        pass
    cur.close()
    return render_template('record//patient.html', record=record, ins_name=ins_name, reports=reports, num_reports=num_reports)

@record.route('/edit-profile/<int:ssn>')
def edit_profile(ssn):
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT Patient.Ssn, Patient.Pat_name, Patient.Sex, Patient.DOB, Patient.Age, Patient.Address, Patient.Tel_no, Patient.Email, Patient.InsCo_id, Patient.Start_date, Patient.End_date
    FROM Patient
    WHERE Patient.Ssn LIKE '%{ssn}%';
    """
    cur.execute(query_input)
    record = cur.fetchone()
    ins_name = f"""
    SELECT *
    FROM Insurance_company
    WHERE Insurance_company.InsCo_id LIKE '%{record[8]}%';
    """
    cur.execute(ins_name)
    ins_name = cur.fetchone()
    if ins_name is None:
        ins_name = "None"
    else:
        ins_name = ins_name[1]

    return render_template('record//edit-profile.html', record=record, ins_name=ins_name)

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
    if new_start_date == "None" or new_end_date == "None":
        cur.execute(f"UPDATE Patient SET Pat_name = '{new_name}', Email = '{new_email}', Tel_no = '{new_phone}', DOB = '{new_DOB}', Address = '{new_address}' WHERE Ssn = {ssn}")
    else:
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
    return redirect(url_for('record.patient_record'))

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
    print(new_InsCo_id)
    cur = mysql.connection.cursor()
    if new_InsCo_id != "Choose Insurance Co":
        new_start_date = request.form['start_date']
        new_end_date = request.form['end_date']
        cur.execute(f"""INSERT INTO Patient 
        (Ssn, Pat_name, Sex, Email, Tel_no, DOB, Age, Address, InsCo_id, Start_date, End_date) VALUES 
        ('{new_ssn}', '{new_name}', '{new_sex}', '{new_email}', '{new_phone}', 
        '{new_DOB}', '{new_age}', '{new_address}', 
        {new_InsCo_id}, 
        '{new_start_date}', '
        {new_end_date}')""")
    else:
        cur.execute(f"""INSERT INTO Patient 
        (Ssn, Pat_name, Sex, Email, Tel_no, DOB, Age, Address) VALUES 
        ('{new_ssn}', '{new_name}', '{new_sex}', '{new_email}', '{new_phone}', 
        '{new_DOB}', '{new_age}', '{new_address}')""")
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
    cur.execute(f"SELECT COUNT(Ssn) FROM Patient")
    count = cur.fetchone()
    num_patients = int(count[0])
    cur.close()
    return render_template('dashboard//patient.html', patients=patients, num_patients=num_patients)

@record.route('/patient-record', methods=['POST'])
def patient_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # filter search
    search_input = (str(request.form.get('search_input')).lower()).strip()
    input_date = str(request.form.get('input_date'))
    search_input = re.sub(' +', ' ', search_input)
    num_patients = 0
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
        cur.execute(f"SELECT COUNT(Ssn) FROM Patient WHERE LOWER(Pat_name) LIKE CONCAT('%', '{search_input}', '%');")
        num_patients += int(cur.fetchone()[0])
        # query by gender
        if search_input == 'men' or search_input == 'male':
            cur.execute(f"SELECT * FROM Patient WHERE Sex='M'")
            search_result += list(cur.fetchall())
            cur.execute(f"SELECT COUNT(Ssn) FROM Patient WHERE Sex = 'M'")
            num_patients += int(cur.fetchone()[0])
        elif search_input == 'woman' or search_input == 'female':
            cur.execute(f"SELECT * FROM Patient WHERE Sex='F'")
            search_result += list(cur.fetchall())
            cur.execute(f"SELECT COUNT(Ssn) FROM Patient WHERE Sex = 'F'")
            num_patients += int(cur.fetchone()[0])
        # query by age
        try:
            search_input = int(search_input)
            cur.execute(f"SELECT * FROM Patient WHERE Age = '{search_input}'")
            search_result = search_result + list(cur.fetchall())
            cur.execute(f"SELECT COUNT(Ssn) FROM Patient WHERE Age = '{search_input}'")
            num_patients += int(cur.fetchone()[0])
        except:
            pass

    # query by DOB, start_date or end_date
    try:
        if len(input_date) > 0:
            cur.execute(f"SELECT * FROM Patient WHERE DOB = '{input_date}'")
            search_result += list(cur.fetchall())
            cur.execute(f"SELECT COUNT(Ssn) FROM Patient WHERE DOB = '{input_date}'")
            num_patients += int(cur.fetchone()[0])
            print(search_result)
    except:
        pass
    cur.close()
    return render_template('dashboard//patient.html', patients=search_result, num_patients=num_patients, current_search=search_input)

@record.route('/medicine-record')
def medicine_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    query_input = """
    SELECT Medicine.Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer, Dis_name
    FROM Medicine, Disease, Cure
    WHERE Medicine.Mdc_id = Cure.Mdc_id AND Cure.Dis_id = Disease.Dis_id;
    """
    num_medicines = 0
    cur.execute(query_input)
    medicines = list(cur.fetchall())
    cur.execute(f"SELECT COUNT(Mdc_id) FROM Medicine")
    num_medicines = int(cur.fetchone()[0])
    cur.close()
    return render_template('dashboard//medicine.html', medicines=medicines, num_medicines=num_medicines)

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
    num_medicines = 0
    search_result = []
    # query by name
    try:
        cur = mysql.connection.cursor()
        query_input = f"""
        SELECT Medicine.Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer, Dis_name
        FROM Medicine, Disease, Cure
        WHERE LOWER(Mdc_name) LIKE '%{search_input}%' AND Medicine.Mdc_id = Cure.Mdc_id AND Cure.Dis_id = Disease.Dis_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
        cur.execute(f"SELECT COUNT(Mdc_id) FROM Medicine WHERE LOWER(Mdc_name) LIKE CONCAT('%', '{search_input}', '%')")
        num_medicines += int(cur.fetchone()[0])
    except:
        pass
    # query by disease name
    try:
        query_input = f"""
        SELECT Medicine.Mdc_id, Mdc_name, Price, MFG, EXP, Quantity, Manufacturer, Disease.Dis_name
        FROM Medicine, Disease, Cure
        WHERE LOWER(Dis_name) LIKE '%{search_input}%' AND Disease.Dis_id = Cure.Dis_id AND Cure.Mdc_id = Medicine.Mdc_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
        cur.execute(f"""
        SELECT COUNT(Medicine.Mdc_id)
        FROM Medicine, Disease, Cure
        WHERE Dis_name LIKE '%{search_input}%' AND Disease.Dis_id = Cure.Dis_id AND Cure.Mdc_id = Medicine.Mdc_id;
        """)
        num_medicines += int(cur.fetchone()[0])
    except:
        pass
    # query by price
    try:
        search_input = int(search_input)
        cur.execute(f"SELECT * FROM Medicine WHERE Price = '{search_input}'")
        search_result = search_result + list(cur.fetchall())
        cur.execute(f"""
        SELECT COUNT(Medicine.Mdc_id)
        FROM Medicine, Disease, Cure
        WHERE Price = '{search_input}' AND Disease.Dis_id = Cure.Dis_id AND Cure.Mdc_id = Medicine.Mdc_id;""")
        num_medicines += int(cur.fetchone()[0])
    except:
        pass
    cur.close()
    return render_template('dashboard//medicine.html', medicines=search_result, num_medicines=num_medicines, current_search=search_input)

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
    cur.execute(f"DELETE FROM Medicine WHERE Mdc_id={id}")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('record.medicine_record'))

@record.route('/medical-record')
def medical_record():

    return render_template('dashboard//medical-record.html', num_reports=0)

@record.route('/medical-record', methods=['POST'])
def medical_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    # search by between date
    search_result = []
    num_reports = 0
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
        cur.execute(f"SELECT COUNT(*) FROM Report WHERE Date BETWEEN '{start_date}' AND '{end_date}'")
        num_reports = int(cur.fetchone()[0])
        cur.close()
        print(search_result)
        return render_template('dashboard//medical-record.html', reports=search_result, num_reports=num_reports)
        
    # filter search
    search_input = (str(request.form.get('search_input')).lower()).strip()
    search_input = re.sub(' +', ' ', search_input)
    print(search_input)
    if len(search_input) == 0:
        return redirect(url_for('record.medical_record'))

    # query by report id
    try:
        cur = mysql.connection.cursor()
        query_input = f"""
        SELECT Report.Re_id, Pat_name, Doc_name, Category, Description, Date
        FROM Report, Doctor, Patient
        WHERE re_id = '{search_input}' AND Report.Ssn = Patient.Ssn AND Report.Doc_id = Doctor.Doc_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
        cur.execute(f"SELECT COUNT(*) FROM Report WHERE re_id='{search_input}'")
        num_reports += int(cur.fetchone()[0])
    except:
        pass

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
        cur.execute(f"SELECT COUNT(Report.Re_id) FROM Report, Doctor, Patient WHERE LOWER(Pat_name) LIKE '%{search_input}%' AND Report.Ssn = Patient.Ssn AND Report.Doc_id = Doctor.Doc_id;")
        num_reports += int(cur.fetchone()[0])
    except:
        pass
    cur.close()
    return render_template('dashboard//medical-record.html', reports=search_result, num_reports=num_reports, current_search=search_input)

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
    return redirect(url_for('record.view_record', ssn=ssn))

@record.route('/bill-record')
def bill_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"""
    SELECT Bill_no, Created_date, Pur_date, Service_charge, Discount, Total_fee, Pur_type, Pat_name, Patient.Tel_no, Acct_name, Accountant.Tel_no
    FROM Bill, Patient, Accountant
    WHERE Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """)
    bills = list(cur.fetchall())
    cur.execute(f"SELECT COUNT(*) FROM Bill")
    num_bills = int(cur.fetchone()[0])
    cur.close()
    return render_template('dashboard//bill-record.html', bills=bills, num_bills=num_bills)

@record.route('/bill-record', methods=['POST'])
def bill_record_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))

    # find bill between two dates
    start_date = str(request.form.get('start_date'))
    end_date = str(request.form.get('end_date'))
    print('start date: ' + start_date)
    print('end date: ' + end_date)
    if len(start_date) > 0 and len(end_date) > 0:
        search_result = []
        cur = mysql.connection.cursor()
        query_input = f"""
        SELECT Bill_no, Created_date, Pur_date, Service_charge, Discount, Total_fee, Pur_type, Pat_name, Patient.Tel_no, Acct_name, Accountant.Tel_no
        FROM Bill, Patient, Accountant
        WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
        """
        cur.execute(query_input)
        search_result += list(cur.fetchall())
        cur.execute(f"SELECT COUNT(*) FROM Bill WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}')")
        num_bills = int(cur.fetchone()[0])
        cur.close()
        return render_template('dashboard//bill-record.html', bills=search_result, num_bills=num_bills)

    search_input = (str(request.form.get('search_input')).lower()).strip()
    search_input = re.sub(' +', ' ', search_input)
    search_result = []
    num_bills = 0
    if len(search_input) == 0:
        return redirect(url_for('record.bill_record'))
    # find bills by name
    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT Bill_no, Created_date, Pur_date, Service_charge, Discount, Total_fee, Pur_type, Patient.Pat_name, Patient.Tel_no, Acct_name, Accountant.Tel_no
    FROM Bill, Patient, Accountant
    WHERE LOWER(Patient.Pat_name) LIKE '%{search_input}%' AND Bill.Ssn = Patient.Ssn AND bill.Acct_id=Accountant.Acct_id;
    """
    cur.execute(query_input)
    search_result += list(cur.fetchall())
    cur.execute(f"SELECT COUNT(*) FROM Bill, Patient WHERE LOWER(Patient.Pat_name) LIKE '%{search_input}%' AND Bill.Ssn = Patient.Ssn")
    num_bills += int(cur.fetchone()[0])

    # find bills by bill no
    query_input = f"""
    SELECT Bill_no, Created_date, Pur_date, Service_charge, Discount, Total_fee, Pur_type, Pat_name, Patient.Tel_no, Acct_name, Accountant.Tel_no
    FROM Bill, Patient, Accountant
    WHERE Bill_no='{search_input}' AND Bill.Ssn = Patient.Ssn AND bill.Acct_id=Accountant.Acct_id;
    """
    cur.execute(query_input)
    search_result += list(cur.fetchall())
    cur.execute(f"SELECT COUNT(*) FROM Bill WHERE Bill_no='{search_input}'")
    num_bills += int(cur.fetchone()[0])


    cur.close()
    return render_template('dashboard//bill-record.html', bills=search_result, num_bills=num_bills, current_search=search_input)

@record.route('/add-bill')
def add_bill_record():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Insurance_company;")
    ins_companies = list(cur.fetchall())
    cur.execute(f"SELECT Acct_id, Acct_name, Tel_no FROM Accountant;")
    accountants = list(cur.fetchall())
    cur.close()
    return render_template('record//add-bill.html', ins_companies=ins_companies, accountants=accountants)



@record.route('/bill-report')
def bill_report():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))

    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT COUNT(Bill_no) AS Total_bill
    FROM Bill, Patient, Accountant
    WHERE Pur_date = CURDATE() AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    total_bill = int(cur.fetchone()[0] or 0)
    query_input = f"""
    SELECT SUM(Total_fee) AS Total_revenue
    FROM Bill, Patient, Accountant
    WHERE Pur_date = CURDATE() AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    total_amount = int(cur.fetchone()[0] or 0)

    query_input = f"""
    SELECT AVG(Total_fee) AS Average_revenue
    FROM Bill, Patient, Accountant
    WHERE Pur_date = CURDATE() AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    average_amount = int(cur.fetchone()[0] or 0)

    query_input = f"""
    SELECT MAX(Total_fee) AS Max_bill_fee
    FROM Bill, Patient, Accountant
    WHERE Pur_date = CURDATE() AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    hightest_amount = int(cur.fetchone()[0] or 0)

    query_input = f"""
    SELECT MIN(Total_fee) AS Min_bill_fee
    FROM Bill, Patient, Accountant
    WHERE Pur_date = CURDATE() AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    lowest_amount = int(cur.fetchone()[0] or 0)
    end_date = get_today()
    start_date = str(get_7_days_ago())
    query_input = f"""
    SELECT Pur_date, SUM(Total_fee)
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id
    GROUP BY Pur_date;
    """
    cur.execute(query_input)
    date_bill_between = cur.fetchall()
    print(date_bill_between)
    graph.bill_report_7_graph(date_bill_between)
    return render_template('dashboard//bill-report.html', total_bill=total_bill, total_amount=total_amount, average_amount=average_amount, hightest_amount=hightest_amount, lowest_amount=lowest_amount)

@record.route('/bill-report', methods=['POST'])
def bill_report_post():
    if LOGGED_IN not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))

    start_date = str(request.form.get('start_date'))
    end_date = str(request.form.get('end_date'))
    if len(start_date) == 0 or len(end_date) == 0:
        flash('Please enter both start date and end date!')
        return redirect(url_for('record.bill_report'))
    cur = mysql.connection.cursor()
    query_input = f"""
    SELECT COUNT(Bill_no) AS Total_bill
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    total_bill_between = int(cur.fetchone()[0] or 0)
    query_input = f"""
    SELECT SUM(Total_fee) AS Total_revenue
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    total_amount_between = int(cur.fetchone()[0] or 0)

    query_input = f"""
    SELECT AVG(Total_fee) AS Average_revenue
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    average_amount_between = int(cur.fetchone()[0] or 0)

    query_input = f"""
    SELECT MAX(Total_fee) AS Max_bill_fee
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    hightest_amount_between = int(cur.fetchone()[0] or 0)

    query_input = f"""
    SELECT MIN(Total_fee) AS Min_bill_fee
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id;
    """
    cur.execute(query_input)
    lowest_amount_between = int(cur.fetchone()[0] or 0)
    query_input = f"""
    SELECT Pur_date, SUM(Total_fee)
    FROM Bill, Patient, Accountant
    WHERE (Pur_date BETWEEN '{start_date}' AND '{end_date}') AND Bill.Ssn = Patient.Ssn AND Bill.Acct_id = Accountant.Acct_id
    GROUP BY Pur_date;
    """
    cur.execute(query_input)
    date_bill_between = cur.fetchall()
    graph.bill_report_graph(date_bill_between, str(start_date), str(end_date))
    return render_template('dashboard//bill-report.html',searching=True , total_bill_between=total_bill_between, total_amount_between=total_amount_between, average_amount_between=average_amount_between, hightest_amount_between=hightest_amount_between, lowest_amount_between=lowest_amount_between)

