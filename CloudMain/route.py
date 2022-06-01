from ast import AsyncFunctionDef
from CloudMain import app, flash, url_for, redirect
from flask import render_template, request, send_file
from CloudMain.models import Account,Classroom, Paper, PaperStudent, Upload_File
from CloudMain.forms import Create_Paper, CreateAccount, LoginForm, Create_Classroom, Student_To_Paper, UpdateProfileInfo,UpdateNickname,\
    UpdateName, UpdateGender, UpdateSchool,UpdateProfilePic,UpdatePassword,Delete_File, Student_To_Paper,Join_Cloudroom
from CloudMain import db
from flask_login import login_user, logout_user, login_required, current_user
from io import BytesIO


@app.route('/')
@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Account.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):
            login_user(attempted_user)
            # flash(f'Success! You are logged in as: {attempted_user.first_name} {attempted_user.last_name}',category='success')
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
@app.route('/dashboard/<user>', methods=['POST', 'GET'])
def dashboard_page(user):
    join_room = Join_Cloudroom()
    if join_room.validate_on_submit():

        student_enrolled_already = False
        paper = Paper.query.filter_by(paper_name=join_room.code.data).first()
        paper_student_to_create = PaperStudent(id_paper=paper.id,
                                               id_student=current_user.id)
        print("hello", join_room.code.data,paper.id)
        # Check if student is already in that paper
        if PaperStudent.query.all():
            for entry in PaperStudent.query.all():
                if entry.id_student == paper_student_to_create.id_student:
                    student_enrolled_already = True

        if student_enrolled_already:
            flash(f'You have already joined this paper.')
            return redirect(url_for('dashboard_page',user=current_user.id))
        else:
            db.session.add(paper_student_to_create)
            db.session.commit()
            flash(f'Student added successfully! You have joined "{paper.paper_name}".',
                  category='success')
            return redirect(url_for('dashboard_page',user=current_user.id))

    user_papers = []
    for entry in PaperStudent.query.all():
        if entry.id_student == current_user.id:
            user_papers.append(Paper.query.filter_by(id=entry.id_paper).first())

    # papers = Paper.query.all()
    classroom = Classroom.query.all()
    return render_template('dashboard.html',user_papers=user_papers,classroom=classroom,join_room=join_room)

# Classroom Main Page - You are taken here after clicking on a classroom in the dashboard
@app.route('/classroom/<class_id>/<paper_id>')
def classroom_main_page(class_id, paper_id):
    paper = Paper.query.filter_by(id=paper_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()


    # Gathering all members in this paper.
    papers = PaperStudent.query.all()
    accounts = Account.query.all()
    members_list = []
    for p in papers:
        for a in accounts:
            if int(p.id_paper) == int(paper_id):
                if int(p.id_student) == int(a.id):
                    members_list.append(a)

    return render_template('classroom_main_page.html', classroom=classroom,
                                                     paper=paper,
                                                     members=members_list)

# Classroom Assignments - Displays all assignments
@app.route('/classroom/<class_id>/<paper_id>/assignments')
def classroom_assignments_list(class_id):
    return render_template('classroom_assignments_list.html')

# Assignment Page - View the details of a specific assignment
@app.route('/classroom/<class_id>/<paper_id>/assignments/<assignment_id>')
def classroom_assignment_details(class_id, assignment_id):
    return render_template('classroom_assignment_details.html')

# Assignment Begin - This is when the student has started the assignment.
@app.route('/classroom/<class_id>/<paper_id>/assignments/<assignment_id>/<page_num>')
def classroom_assignment_content(class_id, assignment_id, page_num):
    return render_template('classroom_assignment_content.html')

# User Profile - Display the users information here
@app.route('/profile/<user>', methods=['POST', 'GET'])
def user_profile(user):
    form_nickname = UpdateNickname()
    form_name = UpdateName()
    form_school = UpdateSchool()
    form_gender = UpdateGender()
    form_profile_pic = UpdateProfilePic()
    form_password = UpdatePassword()

    user_info = Account.query.filter_by(email=current_user.email).first()

    if form_nickname.validate_on_submit():
        user_info.nickname = form_nickname.nickname.data
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_profile', user = current_user.first_name))

    if form_name.validate_on_submit():
        user_info.first_name = form_name.first_name.data
        user_info.last_name = form_name.last_name.data
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_profile', user=current_user.first_name))

    if form_school.validate_on_submit():
        user_info.school = form_school.school.data
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_profile', user=current_user.first_name))

    if form_gender.validate_on_submit():
        user_info.gender = form_gender.gender.data
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_profile', user=current_user.first_name))

    if form_profile_pic.validate_on_submit():
        user_info.profile_pic = form_profile_pic.profile_pic.data
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_profile', user=current_user.first_name))

    if form_password.validate_on_submit():
        new_pass = form_password.password_hash.data
        user_info.password = new_pass
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_profile', user=current_user.first_name))
    if form_password.errors != {}:
        for err_msg in form_password.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', err_msg)
    return render_template('user_profile.html', name=user, form_nickname=form_nickname, form_fname_lname=form_name,
                           form_school=form_school, form_gender=form_gender, form_profile_pic=form_profile_pic,
                           form_password=form_password)

# Student Grades - View the average grades of all their courses so far
@app.route('/profile/<user>/grades', methods=['GET'])
def student_grades(user):
    # Get every paper the student is apart of
    student = Account.query.filter_by(id=current_user.id).first()
    user_papers = []

    for entry in PaperStudent.query.all():
        if entry.id_student == current_user.id:
            user_papers.append(Paper.query.filter_by(id=entry.id_paper).first())
    return render_template('student_grades.html', name=user, papers=user_papers, student=student)

# Student Drive - View all their saved notes or files
@app.route('/profile/<user>/<id>/drive', methods=['POST', 'GET'])
def user_drive(user, id):
    files = Upload_File().query.filter_by(owner=current_user.id)
    delete_form = Delete_File()

    if request.method == "POST":
        delete_item = request.form.get('remove_item')
        d_file_obj = Upload_File().query.filter_by(filename=delete_item).first()
        if d_file_obj:
            Upload_File().query.filter_by(id = d_file_obj.id).delete()
            print(redirect(request.path),"hello from jay")
            flash(f'{d_file_obj.filename} has been deleted')
            db.session.commit()
            return redirect(url_for('user_drive', user=current_user.first_name, id='000'))

        if request.files['file'].filename == '':
            flash(f'Error you must select a file',category='danger')
            delete_file = request.form.get('delete_file')


        else:
            file = request.files['file']
            upload = Upload_File(filename=file.filename, data=file.read(), owner=current_user.id)
            db.session.add(upload)
            db.session.commit()
            flash(f'File(s) has been successfully uploaded!')
            return redirect(url_for('user_drive', user=current_user.first_name, id='000'))

    elif request.method == "GET" and id != '000':
        files = Upload_File().query.filter_by(id=id).first()
        return send_file(BytesIO(files.data), as_attachment=True, attachment_filename=files.filename)

    return render_template('user_drive.html', name=user, files=files, delete_form=delete_form)

# Admin Page - Some pages aren't accessible unless through admin privleges yet
@app.route('/admin', methods=['POST', 'GET'])
def admin_page():
    # Forms
    classroom_form = Create_Classroom()
    paper_form = Create_Paper()
    s_to_p_form = Student_To_Paper()

    # Data
    if Classroom.query.all():
        classrooms = Classroom.query.all()
        test_class = Classroom.query.filter_by(id=1).first()
    else:
        classroom_to_create = Classroom(classroom_name = "Software Engineering")
        db.session.add(classroom_to_create)
        db.session.commit()
        classrooms = Classroom.query.all()
        test_class = Classroom.query.filter_by(id=1).first()

    if Paper.query.all():
        papers = Paper.query.all()
        test_paper = Paper.query.filter_by(id=1).first()
    else:
        paper_to_create = Paper(paper_name = "Python 203",
                                paper_picture = "images/python_203_image.avif",
                                paper_room_number = "203",
                                id_classroom = "1")
        db.session.add(paper_to_create)
        db.session.commit()
        papers = Paper.query.all()
        test_paper = Paper.query.filter_by(id=1).first()
    
    accounts = Account.query.all()

    # Form submissions
    # CREATE PAPER
    if paper_form.submit_paper.data and paper_form.validate():
        paper_to_create = Paper(paper_name = paper_form.paper_name.data,
                                paper_room_number = paper_form.paper_room_number.data,
                                paper_picture = paper_form.paper_picture.data,
                                id_classroom = request.form.get('classroom_select'))
        db.session.add(paper_to_create)
        db.session.commit()      
        flash(f'Paper created successfully! Paper "{paper_to_create.paper_name}" has been created.', category='success')
        return redirect(url_for('home_page'))
    if paper_form.errors != {}:
        for err in paper_form.errors:
            print(f"ERROR: {err}")
        for err_msg in paper_form.errors.values():     
            flash(f'There was an error with creating a Paper: {err_msg}', err_msg)
            return redirect(url_for('home_page'))

    # CREATE CLASSROOM
    if classroom_form.submit_classroom.data and classroom_form.validate():
        classroom_to_create = Classroom(classroom_name = classroom_form.classroom_name.data)
        db.session.add(classroom_to_create)
        db.session.commit()
        flash(f'Classroom created successfully! Clasroom "{classroom_to_create.classroom_name}" has been created.', category='success')
        return redirect(url_for('home_page'))
    if classroom_form.errors != {}:
        for err_msg in classroom_form.errors.values():
            flash(f'There was an error with creating a classroom: {err_msg}', err_msg)
            return redirect(url_for('home_page'))     

    # ADD USER TO PAPER
    if request.method == 'POST' and request.form['submit'] == "Add Student To Paper":
        student_enrolled_already = False
        s_to_p_form.paper_id = int(request.form.get('paper_select'))
        s_to_p_form.student_id = int(request.form.get('student2_select'))
        paper_student_to_create = PaperStudent(id_paper=s_to_p_form.paper_id,
                                               id_student=s_to_p_form.student_id)
        
        # Check if student is already in that paper
        if PaperStudent.query.all():
            for entry in PaperStudent.query.all():
                if entry.id_student == paper_student_to_create.id_student:
                    student_enrolled_already = True  
            
        if student_enrolled_already:
            flash(f'Student already exists in this paper.')
            return redirect(url_for('home_page'))
        else:
            db.session.add(paper_student_to_create)
            db.session.commit()      
            flash(f'Student added successfully! Student "{paper_student_to_create.id_student}" has been added.', category='success')
            return redirect(url_for('home_page'))  

    if s_to_p_form.errors != {}:
        for err in paper_form.errors:
            print(f"ERROR: {err}")
        for err_msg in paper_form.errors.values():     
            flash(f'There was an error with adding a student: {err_msg}', err_msg)
            return redirect(url_for('home_page'))  

    return render_template('admin_page.html', classroom_form=classroom_form, 
                                            paper_form=paper_form,
                                            s_to_p_form=s_to_p_form,
                                            classrooms=classrooms,
                                            accounts=accounts,
                                            papers=papers,
                                            test_class=test_class,
                                            test_paper=test_paper)


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