from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField,RadioField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


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


class LoginForm(FlaskForm):
    email = StringField(label="Email Address:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

# Create_Classroom - by Jakob
# This is the form used by a teacher/admin to create a classroom. The subject and room_number are not mandatory options for now.
class Create_Classroom(FlaskForm):
    classroom_name = StringField(label="Classroom Name", validators=[Length(max=40), DataRequired()])
    classroom_subject = StringField(label="Classroom Subject", vlaidators=[Length(max=40)])
    classroom_room_number = StringField(label="Room Number", vlaidators=[Length(max=10)])
    classroom_picture = RadioField(label="Classroom Picture",
    choices=[('imgaes/classroom_pic1.jpg', 'Technology')], validators=[DataRequired()])
    submit = SubmitField(label='Create Classroom')