from ast import Delete
from xmlrpc.client import DateTime
from flask import Flask
from flask_wtf import FlaskForm
from sqlalchemy import delete
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField, SelectField,RadioField, TextAreaField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from CloudMain.models import Account
from flask_ckeditor import CKEditorField

#Creating accounts form
class CreateAccount(FlaskForm):
    # Checks if email already exists
    def validate_email(self, check_email):
        email = Account.query.filter_by(email=check_email.data).first()
        if email:
            raise ValidationError('Email already exists! Please try again..')

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
    account_type = RadioField(label="Account Type",
                             choices=[('images/Student Button.png', 'Student'), ('images/Teacher Button.png', 'Teacher')],
                             validators=[DataRequired()])
    submit = SubmitField(label='Create Account')

#Login form
class LoginForm(FlaskForm):
    email = StringField(label="Email Address:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


# Create_Classroom - Jakob
# This is the form used by a teacher/admin to create a classroom.
class Create_Classroom(FlaskForm):
    classroom_name = StringField(label="Classroom Name", validators=[Length(max=40), DataRequired()])
    submit_classroom = SubmitField('Create Classroom')


# Create_Paper - Jakob
# This is the form used by a teacher/admin to create a paper.
class Create_Paper(FlaskForm):
    paper_name = StringField(label="Paper Name", validators=[Length(max=40), DataRequired()])
    paper_room_number = StringField(label="Paper Room Number", validators=[Length(max=5), DataRequired()])
    paper_picture = RadioField(label="Profile Picture",
        choices=[('images/tech.jpg','Tech image'),('images/python_201_image.jpg','Python image'),
        ('images/laptops.jpg','Laptop image'),('images/home4.jpg','Phone image')],validators=[DataRequired()])
    submit_paper = SubmitField('Create Paper')


# Jakob
# Add a user to a paper through admin page
class Student_To_Paper(FlaskForm):
    paper_id = IntegerField(label="Paper ID")
    student_id = IntegerField(label="Student ID")
    submit = SubmitField('Add Student To Paper')


# Jakob
# Create an assignment for a paper
class Create_Assignment(FlaskForm):
    name = StringField(label="Assignment name", validators=[Length(max=80), DataRequired()])
    description = TextAreaField(label="Assignment description")
    weight = IntegerField(label="Assignment weight", validators=[DataRequired()])
    picture = RadioField(label="Assignment Picture",
        choices=[('images/classroom_pic1.png','Computer Screen'),('images/python_201_image.jpg','Double Monitor'),
        ('images/laptops.jpg','Laptops'),('images/tech.jpg','Old Tech')],validators=[DataRequired()])
    isPublished = BooleanField("Publish assignment on submit?", default="checked")
    submit = SubmitField()


# Jakob
# Assignment questions
class Create_Assignment_Questions(FlaskForm):
    title = StringField('Title')
    type = SelectField(u'Question Type', choices=[('code', 'Python'), ('text', 'Plain Text')], validators=[DataRequired()])
    description = CKEditorField('Question Description')
    placeholder_text = TextAreaField('Placeholder Content')
    submit = SubmitField()


# Jakob
# Delete an assignment
class Delete_Assignment(FlaskForm):
    submit = SubmitField('Delete')


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
    submit = SubmitField(label='Reset Password')

#delete the file
class Delete_File(FlaskForm):
    submit = SubmitField(label='Delete')

#join a classroom
class Join_Cloudroom(FlaskForm):
    code = StringField(label="Enter Code:", validators=[Length(min=2,max=30), DataRequired()])
    submit = SubmitField(label='Join')

#Posting content in Classroom page
class PostForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    submit = SubmitField(label='Post')

class RequestResetPasswordForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField(label='Reset Password')