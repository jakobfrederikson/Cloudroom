# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# # Lets us refresh the web page to reload a template after we've changed the code
# app.config['TEMPLATES_AUTO_RELOAD'] = True
#
# # Home page
# @app.route('/')
# def home_page():
#     return render_template('index.html')
#
# @app.route('/login')
# def login_page():
#     return render_template('login.html')
#
# @app.route('/signup')
# def sign_up():
#     return render_template('signup.html')
#
# # Dashboard Page - Shows all classrooms that the user is currently apart of
# @app.route('/dashboard/<user>')
# def dashboard_page(user):
#     return render_template('dashboard.html')
#
# # Classroom Main Page - You are taken here after clicking on a classroom in the dashboard
# @app.route('/classroom/<class_id>')
# def classroom_main_page(class_id):
#     return render_template('classroom_main_page.html')
#
# # Classroom Assignments - Displays all assignments
# @app.route('/classroom/<class_id>/assignments')
# def classroom_assignments_list(class_id):
#     return render_template('classroom_assignments_list.html')
#
# # Assignment Page - View the details of a specific assignment
# @app.route('/classroom/<class_id>/assignments/<assignment_id>')
# def classroom_assignment_details(class_id, assignment_id):
#     return render_template('classroom_assignment_details.html')
#
# # Assignment Begin - This is when the student has started the assignment.
# @app.route('/classroom/<class_id>/assignments/<assignment_id>/<page_num>')
# def classroom_assignment_content(class_id, assignment_id, page_num):
#     return render_template('classroom_assignment_content.html')
#
# # User Profile - Display the users information here
# @app.route('/profile/<user>')
# def user_profile(user):
#     return render_template('user_profile.html', name=user)
#
# # Student Grades - View the average grades of all their courses so far
# @app.route('/profile/<user>/grades')
# def student_grades(user):
#     return render_template('student_grades.html', name=user)
#
# # Student Drive - View all their saved notes or files
# @app.route('/profile/<user>/drive')
# def user_drive(user):
#     return render_template('user_drive.html', name=user)
#
# # Admin Page - Some pages aren't accessible unless through admin privleges yet
# @app.route('/admin')
# def admin_page():
#     return render_template('admin_page.html')
#
# if __name__ == '__main__':
#     app.run(development = True)