from flask import Flask, render_template
app = Flask(__name__)

# App Routes

# Home page
@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

# Dashboard Page - Shows all classrooms that the user is currently apart of
@app.route('/dashboard/<user>')
def dashboard_page(user):
    return render_template('dashboard.html')

# Classroom Main Page - You are taken here after clicking on a classroom in the dashboard
@app.route('/classroom/<class_id>')
def classroom_main_page(class_id):
    return render_template('classroom_main_page.html')

# Classroom Assignments - Displays all assignments
@app.route('/classroom/<class_id>/assignments')
def classroom_assignments(class_id):
    return render_template('classroom_assignments.html')

# Assignment Page - You are taken here after clicking on an assignment in the assignment list
@app.route('/classroom/<class_id>/<assignment_id>')
def assignment_page(class_id, assignment_id):
    return render_template('assignment_page.html')

# User Profile - Display the users information here
@app.route('/profile/<user>')
def user_profile(user):
    return render_template('user-profile.html', name=user)


if __name__ == '__main__':
    app.debug = True
    app.run(debug = True)