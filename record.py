from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import mysql
from utils import get_year
record = Blueprint('record', __name__)

@record.route('/patient-record/<int:ssn>')
def view_record(ssn):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Patient WHERE Ssn = {ssn}")
    record = cur.fetchone()
    cur.close()
    return render_template('record//patient.html', record=record)

@record.route('/edit-profile/<int:ssn>')
def edit_profile(ssn):
    if 'logged_in' not in session:
        flash('You are not logged in!')
        return redirect(url_for('main.index'))
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM Patient WHERE Ssn = {ssn}")
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
    return render_template('record//add-profile.html')

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
    new_start_date = request.form['start_date']
    new_end_date = request.form['end_date']
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO Patient (Ssn, Pat_name, Sex, Email, Tel_no, DOB, Age, Address, Start_date, End_date) VALUES ('{new_ssn}', '{new_name}', '{new_sex}', '{new_email}', '{new_phone}', '{new_DOB}', '{new_age}', '{new_address}', '{new_start_date}', '{new_end_date}')")
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('main.patient_record'))