from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField, SelectField,RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

#Creating accounts form
class CreateAccount(FlaskForm):
    first_name = StringField(label="First name", validators=[Length(min=2,max=30), DataRequired()])
    last_name = StringField(label="Last name", validators=[Length(min=2,max=30), DataRequired()])
    gender = SelectField(label="Select your Gender", choices=[('Male'), ('Female'), ('Other')])
    school = SelectField(label="Select your School",
                         choices=[('Yoobee College'), ('Victoria University'), ('Massey University')])
    nickname = StringField(label="Nickname", validators=[Length(min=2,max=30), DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    confirm_email = StringField(label="Confirm Email",validators=[EqualTo('email')])
    password_hash = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    verify_password = PasswordField(label="Confirm Password",validators=[EqualTo('password_hash'),DataRequired()])
    profile_pic = RadioField(label="Profile Picture",
        choices=[('images/profile1.jpg','Ghost'),('images/profile2.jpg','Zombie'),
        ('images/profile3.jpg','Squid Game'),('images/profile4.jpg','Astro Cat')],validators=[DataRequired()])
    submit = SubmitField(label='Create Account')

#Login form
class LoginForm(FlaskForm):
    email = StringField(label="Email Address:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# Create_Classroom - by Jakob
# This is the form used by a teacher/admin to create a classroom.
class Create_Classroom(FlaskForm):
    classroom_name = StringField(label="Classroom Name", validators=[Length(max=40), DataRequired()])
    submit_classroom = SubmitField('Create Classroom')

# Create_Classroom - by Jakob
# This is the form used by a teacher/admin to create a classroom.
class Create_Paper(FlaskForm):
    paper_name = StringField(label="Paper Name", validators=[Length(max=40), DataRequired()])
    paper_room_number = StringField(label="Paper Room Number", validators=[Length(max=5), DataRequired()])
    paper_picture = RadioField(label="Profile Picture",
        choices=[('images/profile1.jpg','Ghost'),('images/profile2.jpg','Zombie'),
        ('images/profile3.jpg','Squid Game'),('images/profile4.jpg','Astro Cat')],validators=[DataRequired()])
    submit_paper = SubmitField('Create Paper')

# Add a user to a paper
class Student_To_Paper(FlaskForm):
    paper_id = IntegerField(label="Paper ID")
    student_id = IntegerField(label="Student ID")
    submit = SubmitField('Add Student To Paper')

# Update user details forms
class UpdateNickname(FlaskForm):
    nickname = StringField(label="Nickname", validators=[Length(min=2,max=30), DataRequired()])
    submit = SubmitField(label='Save Changes')
#update first name and last name
class UpdateName(FlaskForm):
    first_name = StringField(label="First name", validators=[Length(min=2,max=30), DataRequired()])
    last_name = StringField(label="Last name", validators=[Length(min=2,max=30), DataRequired()])
    submit = SubmitField(label='Save Changes')
#updates gender
class UpdateGender(FlaskForm):
    gender = SelectField(label="Select your Gender", choices=[('Male'), ('Female'), ('Other')])
    submit = SubmitField(label='Save Changes')
#updates school
class UpdateSchool(FlaskForm):
    school = SelectField(label="Select your School",
                         choices=[('Yoobee College'), ('Victoria University'), ('Massey University')])
    submit = SubmitField(label='Save Changes')
#updates profile picture
class UpdateProfilePic(FlaskForm):
    profile_pic = RadioField(label="Profile Picture",
        choices=[('images/profile1.jpg','Ghost'),('images/profile2.jpg','Zombie'),
        ('images/profile3.jpg','Squid Game'),('images/profile4.jpg','Astro Cat')],validators=[DataRequired()])
    submit = SubmitField(label='Save Changes')
#updates password
class UpdatePassword(FlaskForm):
    password_hash = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    verify_password = PasswordField(label="Confirm Password", validators=[EqualTo('password_hash'), DataRequired()])
    submit = SubmitField(label='Save Changes')
#delete the file
class Delete_File(FlaskForm):
    submit = SubmitField(label='Delete File')
#join a classroom
class Join_Cloudroom(FlaskForm):
    code = StringField(label="Enter Code:", validators=[Length(min=2,max=30), DataRequired()])
    submit = SubmitField(label='Join')
