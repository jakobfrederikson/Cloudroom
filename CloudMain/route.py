from CloudMain import app, flash, url_for, redirect
from flask import render_template, request
from CloudMain import models
from CloudMain.models import Account
from CloudMain.models import Classroom
from CloudMain.forms import CreateAccount, LoginForm, Create_Classroom, UpdateProfileInfo
from CloudMain import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Account.query.filter_by(email=form.email.data).first()
        print(attempted_user)
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.first_name} {attempted_user.last_name}',category='success')
            return redirect(url_for('dashboard_page', user = attempted_user.first_name))
        else:
            flash('Username and password are not match! Please try again',category='danger')
    return render_template("login.html", form=form)

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    form = CreateAccount()
    if form.validate_on_submit():
        user_to_create = Account(first_name=form.first_name.data,
                                 last_name=form.last_name.data,
                                 school=form.school.data,
                                 gender=form.gender.data,
                                 password=form.password_hash.data,
                                 email=form.email.data,
                                 nickname=form.nickname.data,
                                 profile_pic=form.profile_pic.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now log in as {user_to_create.first_name} '
              f'{user_to_create.last_name}', category='success')
        return redirect(url_for('dashboard_page', user = user_to_create.first_name))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', err_msg)
    return render_template("signup.html", form=form)

@app.route('/logout')
def log_out():
    logout_user()
    flash(f'You have been logged out!', category='info')
    return  redirect(url_for("home_page"))

# Dashboard Page - Shows all classrooms that the user is currently apart of
@app.route('/dashboard/<user>')
def dashboard_page(user):
    return render_template('dashboard.html')

# Classroom Main Page - You are taken here after clicking on a classroom in the dashboard
@app.route('/classroom/<class_id>')
def classroom_main_page(class_id):
    return render_template('classroom_main_page.html', class_id=class_id)

# Classroom Assignments - Displays all assignments
@app.route('/classroom/<class_id>/assignments')
def classroom_assignments_list(class_id):
    return render_template('classroom_assignments_list.html')

# Assignment Page - View the details of a specific assignment
@app.route('/classroom/<class_id>/assignments/<assignment_id>')
def classroom_assignment_details(class_id, assignment_id):
    return render_template('classroom_assignment_details.html')

# Assignment Begin - This is when the student has started the assignment.
@app.route('/classroom/<class_id>/assignments/<assignment_id>/<page_num>')
def classroom_assignment_content(class_id, assignment_id, page_num):
    return render_template('classroom_assignment_content.html')

# User Profile - Display the users information here
@app.route('/profile/<user>')
def user_profile(user):
    return render_template('user_profile.html',name=user)

# Student Grades - View the average grades of all their courses so far
@app.route('/profile/<user>/grades')
def student_grades(user):
    return render_template('student_grades.html', name=user)

# Student Drive - View all their saved notes or files
@app.route('/profile/<user>/drive')
def user_drive(user):
    return render_template('user_drive.html', name=user)

# Admin Page - Some pages aren't accessible unless through admin privleges yet
@app.route('/admin', methods=['POST', 'GET'])
def admin_page():
    form = Create_Classroom()
    if form.validate_on_submit():
        classroom_to_create = Classroom(classroom_name = form.classroom_name.data,
                                        classroom_subject = form.classroom_subject.data,
                                        classroom_room_number = form.classroom_room_number.data,
                                        classroom_picture = form.classroom_picture.data)
        db.session.add(classroom_to_create)
        db.session.commit()
        flash(f'Classroom created successfully! Clasroom {classroom_to_create.classroom_name} has been created.', category='success')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a classroom: {err_msg}', err_msg)
    return render_template('admin_page.html', form=form)

@app.route('/editprofile', methods=['POST', 'GET'])
def edit_profile():
    form = UpdateProfileInfo()
    if form.validate_on_submit():
        user_info = Account.query.filter_by(email=current_user.email).first()
        user_info.first_name = form.first_name.data
        user_info.last_name = form.last_name.data
        user_info.school = form.school.data
        user_info.gender = form.gender.data
        user_info.nickname = form.nickname.data
        user_info.profile_pic = form.profile_pic.data
        db.session.add(user_info)
        db.session.commit()
        login_user(user_info)
        return redirect(url_for('user_profile', user = current_user.first_name))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error updating user: {err_msg}', err_msg)
    return render_template("editprofile.html", form=form)