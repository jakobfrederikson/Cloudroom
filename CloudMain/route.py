from msilib.schema import Class
from sqlalchemy import delete, null
from CloudMain import app, flash, url_for, redirect, db, functions, mail, session
from flask import render_template, request, send_file
from CloudMain.models import Account, AssignmentQuestions,Classroom, Paper, paper_members, Upload_File, Assignment,Post
from CloudMain.forms import Create_Assignment_Questions, Create_Paper, CreateAccount, GeneralSubmitForm, LoginForm, Create_Classroom, Student_To_Paper,UpdateNickname,\
    UpdateName, UpdateGender, UpdateSchool,UpdateProfilePic,UpdatePassword,Delete_File, Student_To_Paper,Join_Cloudroom,\
        Create_Assignment, PostForm, RequestResetPasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from io import BytesIO
from datetime import datetime

#homepage
@app.route('/')
@app.route('/index')
def home_page():
    return render_template('index.html')

#request for reset password
@app.route('/reset_password_request', methods=['POST', 'GET'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(email=form.email.data).first()
        if user:
            functions.send_reset_email(user)
            flash('An email has been sent to reset your password',category="info")
            return redirect(url_for('login_page'))
        else:
            flash('Invalid email please try again.',category="danger")

    return render_template('forgot_password.html',form=form)

#resets password
@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    user = Account.verify_reset_token(token)

    if user is None:
        flash('Token is invalid or token has expired',category='warning')
        return redirect(url_for('forgot_password'))
    form_password = UpdatePassword()

    if form_password.validate_on_submit():
        new_pass = form_password.password_hash.data
        user.password = new_pass
        db.session.commit()
        flash('Password has been reset', category='info')
        return redirect(url_for('login_page'))
    return render_template('reset_password.html',form_password=form_password)

#login page
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

@app.route('/about')
def about_page():
    return render_template("about.html")

#sign up page
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    form = CreateAccount()
    if form.validate_on_submit():
        value = form.account_type.data
        choices = dict(form.account_type.choices)
        label = choices[value]
        user_to_create = Account(first_name=form.first_name.data,
                                 last_name=form.last_name.data,
                                 school=form.school.data,
                                 gender=form.gender.data,
                                 password=form.password_hash.data,
                                 email=form.email.data,
                                 nickname=form.nickname.data,
                                 profile_pic=form.profile_pic.data,
                                 account_type=label)
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

#this will logout the user and return them to home page
@app.route('/logout')
def log_out():
    logout_user()
    flash(f'You have been logged out!', category='info')
    return  redirect(url_for("home_page"))

# Dashboard Page - Shows all classrooms that the user is currently apart of
@app.route('/dashboard/<user>', methods=['POST', 'GET'])
@login_required
def dashboard_page(user):
    join_room = Join_Cloudroom()
    classroom_form = Create_Classroom()
    paper_form = Create_Paper()
    classrooms = Classroom.query.all()

    # Join Cloudroom
    if join_room.validate_on_submit():
        student_enrolled_already = False
        paper = Paper.query.filter_by(paper_name=join_room.code.data).first()
        if paper is None:
            flash(f'Code in invalid.',
                  category='danger')
        else:
            paper_student_to_create = paper_members(id_paper=paper.id,
                                                   id_user=current_user.id,
                                                   account_type=current_user.account_type)
            # Check if student is already in that paper
            if paper_members.query.all():
                for entry in paper_members.query.all():
                    if entry.id_paper == paper_student_to_create.id_paper:
                        if entry.id_user == paper_student_to_create.id_user:
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

    # CREATE PAPER
    if paper_form.submit_paper.data and paper_form.validate():
        paper_to_create = Paper(paper_name=paper_form.paper_name.data,
                                paper_room_number=paper_form.paper_room_number.data,
                                paper_picture=paper_form.paper_picture.data,
                                id_classroom=request.form.get('classroom_select'))

        db.session.add(paper_to_create)
        db.session.commit()

        paper_teacher_to_create = paper_members(id_paper=paper_to_create.id,
                                                id_user=current_user.id,
                                                account_type=current_user.account_type)

        db.session.add(paper_teacher_to_create)
        db.session.commit()

        flash(f'Paper created successfully! Paper "{paper_to_create.paper_name}" has been created.', category='success')
        return redirect(url_for('dashboard_page',user=current_user))

    # CREATE CLASSROOM
    if classroom_form.validate():
        classroom_to_create = Classroom(classroom_name=classroom_form.classroom_name.data)
        db.session.add(classroom_to_create)
        db.session.commit()
        flash(f'Classroom created successfully! Classroom "{classroom_to_create.classroom_name}" has been created.',
              category='success')
        return redirect(url_for('dashboard_page',user=current_user))


    user_papers = []
    for entry in paper_members.query.all():
        if entry.id_user == current_user.id:
            user_papers.append(Paper.query.filter_by(id=entry.id_paper).first())

    # papers = Paper.query.all()
    classroom = Classroom.query.all()
    return render_template('dashboard.html',user_papers=user_papers,classroom=classroom,join_room=join_room,
                           classroom_form=classroom_form,paper_form=paper_form,classrooms=classrooms)

# This will update the post of the user
@app.route('/classroom/update_post/<class_id>/<paper_id>/<post_id>', methods=['POST', 'GET'])
@login_required
def update_post(class_id, paper_id,post_id):
    paper = Paper.query.filter_by(id=paper_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()
    edit_post = PostForm()
    post_form = PostForm()
    posts = Post.query.filter_by(paper_id=paper_id)
    del_post = Delete_File()

    if edit_post.validate_on_submit():
        post_file_obj = Post().query.filter_by(id=post_id).first()
        if post_file_obj:
            if edit_post.title.data:
                post_file_obj.title = edit_post.title.data
            else:
                post_file_obj.title = "No Title"

            if edit_post.content.data:
                post_file_obj.content = edit_post.content.data
            else:
                post_file_obj.content = "No Description"
            db.session.add(post_file_obj)
            db.session.commit()
            return redirect(url_for('classroom_main_page', class_id=class_id, paper_id=paper_id, postform=post_form,
                                   posts=posts, del_post=del_post, edit_post=edit_post))

    member_list = functions.get_all_members(paper_id)
    to_update = Post().query.filter_by(id=post_id).first()
    edit_post.title.data = to_update.title
    edit_post.content.data = to_update.content
    return render_template('edit_post.html', edit_post=edit_post,postform=post_form,classroom=classroom,paper=paper,
                           members=member_list)

# This will update the post of the user
@app.route('/classroom/create_post/<class_id>/<paper_id>', methods=['POST', 'GET'])
@login_required
def create_post(class_id, paper_id):
    paper = Paper.query.filter_by(id=paper_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()
    edit_post = PostForm()
    post_form = PostForm()
    posts = Post.query.filter_by(paper_id=paper_id)
    del_post = Delete_File()

    # create a post
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data,
                    paper_id=paper.id,
                    content=post_form.content.data,
                    owner=current_user.id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('classroom_main_page', class_id=class_id, paper_id=paper_id, postform=post_form,
                               posts=posts, del_post=del_post, edit_post=edit_post))

    member_list = functions.get_all_members(paper_id)
    return render_template('create_post.html',postform=post_form,classroom=classroom,paper=paper,
                           members=member_list)

# Classroom Main Page - You are taken here after clicking on a classroom in the dashboard
@app.route('/classroom/<class_id>/<paper_id>', methods=['POST', 'GET'])
@login_required
def classroom_main_page(class_id, paper_id):
    # Get the paper and classroom using the url
    paper = Paper.query.filter_by(id=paper_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()
    posts = Post.query.filter_by(paper_id=paper.id)
    del_post = Delete_File()
    postform = PostForm()

    if request.method == "POST":
        delete_item = request.form.get('remove_item')
        d_file_obj = Post().query.filter_by(title=delete_item).first()
        #handles delete post
        if d_file_obj:
            Post().query.filter_by(id = d_file_obj.id).delete()
            flash(f'{d_file_obj.title} has been deleted')
            db.session.commit()
            return redirect(url_for('classroom_main_page', class_id=classroom.id, paper_id=paper.id, postform=postform,
                                    posts=posts, del_post=del_post))

        #handles remove student
        remove_student = request.form.get('remove_student')
        std_file_obj = paper_members().query.filter_by(id_user=remove_student).first()
        print(remove_student,"hellos")
        if std_file_obj:
            paper_members().query.filter_by(id = std_file_obj.id).delete()
            db.session.commit()
            return redirect(url_for('classroom_main_page', class_id=classroom.id, paper_id=paper.id, postform=postform,
                                    posts=posts, del_post=del_post))

    #create a post
    if postform.validate_on_submit():
        post = Post(title=postform.title.data,
                    paper_id=paper.id,
                    content=postform.content.data,
                    owner=current_user.id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('classroom_main_page',class_id=classroom.id,paper_id=paper.id,postform=postform,
                                posts=posts,del_post=del_post))

    # Gathering all members in this paper.
    member_list = functions.get_all_members(paper_id)
    return render_template('classroom_main_page.html', classroom=classroom,paper=paper,members=member_list,
                           postform=postform,posts=posts,del_post=del_post)

# Classroom Assignments - Displays all assignments
@app.route('/classroom/<class_id>/<paper_id>/assignments', methods=['GET','POST'])
@login_required
def classroom_assignments_list(class_id, paper_id):

    # Only get assignments apart of this paper
    assignments = []
    for entry in Assignment.query.all():
        if str(entry.paper_id) == str(paper_id):
            assignments.append(entry)

    # Get the paper and classroom using the url
    paper = Paper.query.filter_by(id=paper_id).first()
    classroom = Classroom.query.filter_by(id=class_id).first()
    member_list = functions.get_all_members(paper_id)

    return render_template('classroom_assignments_list.html', classroom=classroom,
                                                            paper=paper,
                                                            assignments=assignments,
                                                            class_id = class_id,
                                                            paper_id = paper_id,
                                                            members=member_list)

# Create Assignment - Teacher can create an assignment here for a paper here
@app.route('/classroom/<class_id>/<paper_id>/create_assignment', methods=['POST', 'GET'])
@login_required
def create_assignment(class_id, paper_id):
    classrooms = Classroom.query.all()
    paper = Paper.query.filter_by(id=int(paper_id)).first()
    assignment_form = Create_Assignment()

    if assignment_form.validate_on_submit():
        selected_paper = int(paper_id)
        students_of_paper = []
        if paper_members.query.all():
            for entry in paper_members.query.all():
                if entry.id_paper == selected_paper:
                    if entry.account_type == "Student":
                        students_of_paper.append(Account.query.filter_by(id=entry.id_user).first())

        if students_of_paper:
            for student in students_of_paper:
                assignment_to_create = Assignment(name = request.form.get("name"),
                                                description = request.form.get("description"),
                                                creationDate = assignment_form.creationDate.data,
                                                dueDate = assignment_form.dueDate.data,
                                                isCompleted = False,
                                                weight = int(request.form.get("weight")),                                                
                                                picture = assignment_form.picture.data,
                                                isPublished = assignment_form.isPublished.data,
                                                teacher_id = int(current_user.id),
                                                paper_id = int(selected_paper),
                                                owner = int(student.id))                         
                db.session.add(assignment_to_create)
                db.session.commit()
        else: # If there are no students in the paper yet
            assignment_to_create = Assignment(name = request.form.get("name"),
                                                description = request.form.get("description"),
                                                creationDate = assignment_form.creationDate.data,
                                                dueDate = assignment_form.dueDate.data,
                                                isCompleted = False,
                                                weight = int(request.form.get("weight")),
                                                picture = assignment_form.picture.data,    
                                                isPublished = assignment_form.isPublished.data,                                            
                                                teacher_id = int(current_user.id),
                                                paper_id = int(selected_paper),
                                                owner = current_user.id)     
            db.session.add(assignment_to_create)
            db.session.commit()

        assignment_id = 0
        # Get the last entry into the assignment table
        assignment_id = Assignment.query.order_by(-Assignment.id).first()
        return redirect(url_for('create_classroom_questions', class_id = class_id, paper_id = paper_id, assignment_id = assignment_id.id))

    if assignment_form.errors != {}:
        for err_msg in assignment_form.errors.values():     
            flash(f'There was an error with creating an Assignment: {err_msg}', err_msg)

    return render_template('create_assignment.html', classrooms=classrooms,
                                                    paper=paper,
                                                    assignment_form=assignment_form)

# Create the questions for the assignment
@app.route('/classroom/<class_id>/<paper_id>/create_assignment/<assignment_id>/', methods=['POST', 'GET'])
@login_required
def create_classroom_questions(class_id, paper_id, assignment_id):
    paper = Paper.query.filter_by(id=int(paper_id)).first()
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    questions_form = Create_Assignment_Questions()

    # Start the user session to store multiple questions for an assignment
    questions_list = []    
    if 'questions' not in session:
        session['questions'] = []
    questions_list = session['questions']  

    if questions_form.validate_on_submit():
        if request.form['submit'] == "Submit":
            # Check if the creator is submitting an empty question
            if session['questions'] != []: # if user is creating multiple questions
                for q in questions_list:
                    question = AssignmentQuestions(title = q['title'],
                                                    owner = int(q['owner']),
                                                    type = q['type'],
                                                    description = q['description'],
                                                    placeholder_text = q['placeholder_text'])
                    db.session.add(question)
                print("\n\nCommiting multiple questions\n\n")
                db.session.commit()
            elif questions_form.type.data and questions_form.title.data \
                and questions_form.submit.data: # if user is only creating one question
                question = AssignmentQuestions(title = request.form.get("title"),
                                                    owner = int(assignment_id),
                                                    type = request.form.get("type"),
                                                    description= questions_form.description.data,
                                                    placeholder_text = questions_form.placeholder_text.data)
                print("\n\nCommiting ONE questions\n\n")
                db.session.commit()
            else: # if user is creating no questions
                print(f"\n\n {current_user.first_name} is creating NO QUESTIONS\n\n")            

            # clear the session cache of our questions
            session.pop('questions')
            flash(f'Questions successfully created for {assignment.name}')
            return redirect(url_for('classroom_assignments_list', class_id = class_id, paper_id = paper_id))
        
        # Append the created question to the questions list
        if request.form['submit'] == "Create another question":
            question = AssignmentQuestions(title = request.form.get("title"),
                                        owner = int(assignment_id),
                                        type = request.form.get("type"),
                                        description= questions_form.description.data,
                                        placeholder_text = questions_form.placeholder_text.data)
            questions_list.append(question.serialize())
            session['questions'] = questions_list      
        
    if questions_form.errors != {}:
        for err_msg in questions_form.errors.values():     
            flash(f'There was an error with creating an Assignment: {err_msg}', err_msg)

    return render_template('create_assignment_questions.html', class_id = class_id, 
                                                                paper_id = paper_id,
                                                                paper = paper,
                                                                questions_form = questions_form,
                                                                questions_list = questions_list,
                                                                assignment = assignment)

# Assignment Begin - This is when the student has started the assignment.
@app.route('/classroom/<class_id>/<paper_id>/assignments/<assignment_id>')
@login_required
def classroom_assignment_content(class_id, paper_id, assignment_id):
    classroom = Classroom.query.filter_by(id=int(class_id)).first()
    paper = Paper.query.filter_by(id=int(paper_id)).first()
    assignment = Assignment.query.filter_by(id=int(assignment_id)).first()
    questions = []
    for question in AssignmentQuestions.query.all():
        if int(question.owner) == int(assignment_id):
            questions.append(question)
    return render_template('classroom_assignment_content.html', classroom=classroom,
                                                                paper=paper,
                                                                assignment=assignment,
                                                                questions=questions)

# Edit an assignment
@app.route('/classroom/<class_id>/<paper_id>/assignments/edit/<assignment_id>', methods=['POST', 'GET'])
@login_required
def edit_assignment(class_id, paper_id, assignment_id):
    classroom = Assignment.query.filter_by(id=class_id).first()
    paper = Paper.query.filter_by(id=paper_id).first()
    assignment = Assignment.query.filter_by(id=assignment_id).first()
    edit_form = Create_Assignment()

    if edit_form.validate_on_submit():
        selected_paper = int(paper_id)
        students_of_paper = []
        if paper_members.query.all():
            for entry in paper_members.query.all():
                if entry.id_paper == selected_paper:
                    if entry.account_type == "Student":
                        students_of_paper.append(Account.query.filter_by(id=entry.id_user).first())

        if students_of_paper:
            for student in students_of_paper:
                assignment.name = edit_form.name.data
                assignment.description = edit_form.description.data
                assignment.creationDate = edit_form.creationDate.data
                assignment.dueDate = edit_form.dueDate.data
                assignment.weight = edit_form.weight.data
                assignment.picture = edit_form.picture.data
                assignment.isPublished = edit_form.isPublished.data
                db.session.add(assignment)
                
        else:
            assignment.name = edit_form.name.data
            assignment.description = edit_form.description.data
            assignment.creationDate = edit_form.creationDate.data
            assignment.dueDate = edit_form.dueDate.data
            assignment.weight = edit_form.weight.data
            assignment.picture = edit_form.picture.data
            assignment.isPublished = edit_form.isPublished.data
            db.session.add(assignment)

        db.session.commit()
        flash(f'Successfully updated {assignment.name}')
        return redirect(url_for('classroom_assignments_list', class_id = class_id, paper_id = paper_id))

    edit_form.name.data = assignment.name
    edit_form.description.data = assignment.description
    edit_form.creationDate.data = assignment.creationDate
    edit_form.dueDate.data = assignment.dueDate
    edit_form.weight.data = assignment.weight
    edit_form.picture.data = assignment.picture
    return render_template('edit_assignment.html', assignment = assignment, edit_form = edit_form, classroom = classroom, paper = paper)

# Delete an assignment
@app.route('/classroom/<class_id>/<paper_id>/assignments/delete/<assignment_id>', methods=['POST', 'GET'])
def delete_assignment(class_id, paper_id, assignment_id):
    classroom = Classroom.query.filter_by(id=int(class_id)).first()
    paper = Paper.query.filter_by(id=int(paper_id)).first()
    assignment = Assignment.query.filter_by(id=int(assignment_id)).first()
    delete_form = GeneralSubmitForm()

    if request.method == "POST":
        assignment_to_delete = Assignment.query.filter_by(id = assignment_id).first()
        if assignment_to_delete:
            # Delete Assignment
            Assignment.query.filter_by(id=assignment_to_delete.id).delete()

            # Delete all questions related to the assignment
            for question in AssignmentQuestions.query.all():
                if question.owner == assignment_to_delete.id:
                    AssignmentQuestions.query.filter_by(id = question.id).delete()
            
            flash(f'{assignment_to_delete.name} has been successfully deleted.')
            db.session.commit()
            return redirect(url_for('classroom_assignments_list', class_id = classroom.id, paper_id = paper.id))

    return render_template('delete_assignment.html', assignment = assignment, delete_form = delete_form, classroom = classroom, paper = paper)

# Publish an assignment
@app.route('/classroom/<class_id>/<paper_id>/assignments/publish/<assignment_id>', methods=['POST', 'GET'])
def publish_assignment(class_id, paper_id, assignment_id):
    classroom = Classroom.query.filter_by(id=int(class_id)).first()
    paper = Paper.query.filter_by(id=int(paper_id)).first()
    assignment = Assignment.query.filter_by(id=int(assignment_id)).first()
    publish_form = GeneralSubmitForm()

    if request.method == "POST":
        assignment_to_publish = Assignment.query.filter_by(id = assignment_id).first()
        if assignment_to_publish:
            assignment_to_publish.isPublished = True
            db.session.add(assignment_to_publish)

            flash(f'{assignment_to_publish.name} has been successfully published.')
            db.session.commit()
            return redirect(url_for('classroom_assignments_list', class_id = classroom.id, paper_id = paper.id))

    return render_template('publish_assignment.html', assignment = assignment, publish_form = publish_form, classroom = classroom, paper = paper)

# User Profile - Display the users information here
@app.route('/profile/<user>', methods=['POST', 'GET'])
@login_required
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
@login_required
def student_grades(user):

    # Getting every paper the student is enrolled in.
    student = Account.query.filter_by(id=current_user.id).first()
    user_papers = []
    for entry in paper_members.query.all():
        if entry.id_user == current_user.id:
            user_papers.append(Paper.query.filter_by(id=entry.id_paper).first())

    return render_template('student_grades.html', name=user, papers=user_papers, student=student)

# Student Drive - View all their saved notes or files
@app.route('/profile/<user>/<id>/drive', methods=['POST', 'GET'])
@login_required
def user_drive(user, id):
    files = Upload_File().query.filter_by(owner=current_user.id)
    delete_form = Delete_File()

    if request.method == "POST":
        delete_item = request.form.get('remove_item')
        d_file_obj = Upload_File().query.filter_by(filename=delete_item).first()
        if d_file_obj:
            Upload_File().query.filter_by(id = d_file_obj.id).delete()
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

# Admin Page - Some functions (adding papers, classrooms)
@app.route('/admin', methods=['POST', 'GET'])
def admin_page():
    # Forms - used to gather information to create each entity
    classroom_form = Create_Classroom()
    paper_form = Create_Paper()
    s_to_p_form = Student_To_Paper()

    # Creating an entry for classroom/paper if one doesn't exist already.
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
                                paper_picture = "images/python_201_image.jpg",
                                paper_room_number = "203",
                                id_classroom = "1")
        db.session.add(paper_to_create)
        db.session.commit()
        papers = Paper.query.all()
        test_paper = Paper.query.filter_by(id=1).first()
    
    accounts = Account.query.all()

    # Form submissions - gathering data from the forms and then submitting into the database
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

        user = Account.query.filter_by(id=int(request.form.get('student2_select'))).first()
        s_to_p_form.id_user = user.id
        s_to_p_form.account_type = user.account_type

        paper_student_to_create = paper_members(id_paper=s_to_p_form.paper_id,
                                               id_user=s_to_p_form.id_user,
                                               account_type=s_to_p_form.account_type)
        
        # Check if student is already in that paper
        if paper_members.query.all():
            for entry in paper_members.query.all():
                if entry.id_paper == paper_student_to_create.id_paper:
                     if entry.id_user == paper_student_to_create.id_user:
                        student_enrolled_already = True  
            
        if student_enrolled_already:
            flash(f'User already exists in this paper.')
            return redirect(url_for('home_page'))
        else:
            db.session.add(paper_student_to_create)
            db.session.commit()      
            flash(f'User added successfully! User "{paper_student_to_create.id_user}" has been added.', category='success')
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

@app.route('/cloudroom_tools')
def cloudroom_tools():
    return render_template('cloudroom_tools.html')
