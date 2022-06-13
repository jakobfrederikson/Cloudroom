from CloudMain import db, login_manager
from CloudMain import bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

#This class will create the model for accounts
class Account(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)
    gender = db.Column(db.String(length=20), nullable=False)
    school = db.Column(db.String(length=50), nullable=False)
    nickname = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=20), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=12), nullable=False)
    profile_pic = db.Column(db.String(length=20), nullable=False)
    account_type = db.Column(db.String(length=20), nullable=False)
    items = db.relationship('Upload_File', backref='owned_user', lazy=True)#Lazy gets all items from Upload_file
    assignments = db.relationship('Assignment', backref='owned_student', lazy=True)
    poster = db.relationship('Post', backref='poster', lazy=True)  # Lazy gets all items from Upload_file

    #returns the password
    @property
    def password(self):
        return self.password
    #this will decrypt the password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    #checks if password is valid
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


# Jakob
# Classroom model - holds papers (e.g. Classroom: Software Engineering, Paper: Python 203, Paper: C++ 101)
class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = db.Column(db.Integer(), primary_key=True)
    classroom_name = db.Column(db.String(length=30), nullable=False)
    id_paper = db.Column(db.Integer(), db.ForeignKey('paper.id'), nullable=True)


# Jakob
# Paper model - holds data about itself and the Classroom it's attatched to.
class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer(), primary_key=True)
    paper_name = db.Column(db.String(length=30), nullable=False)
    paper_picture = db.Column(db.String(length=20), nullable=False)
    paper_room_number = db.Column(db.String(length=20), nullable=False)
    id_classroom = db.Column(db.Integer(), db.ForeignKey('classroom.id'), nullable=False)
    owner = db.relationship('Post', backref='post_owner', lazy=True)

# Jakob
# paper_members - holds information about what user is apart of what paper.
class paper_members(db.Model):
    __tablename__ = 'paper_members'
    id = db.Column(db.Integer(), primary_key=True)
    id_paper = db.Column(db.Integer(), db.ForeignKey('paper.id'), nullable = False)
    id_user = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable = False)
    account_type = db.Column(db.String(), db.ForeignKey('account.account_type'), nullable = False)


# Jakob
# classroom_members - holds information about what user is apart of what classroom.
class classroom_members(db.Model):
    __tablename__= 'classroom_members'
    id = db.Column(db.Integer(), primary_key=True)
    id_classroom = db.Column(db.Integer(), db.ForeignKey('classroom.id'), nullable = False)
    id_user = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable = False)
    account_type = db.Column(db.String(), db.ForeignKey('account.account_type'), nullable = False)


# Jakob
# Assignment Model - This is here for future use.
class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(), nullable = True)
    creationDate = db.Column(db.Date())
    dueDate = db.Column(db.Date())
    isCompleted = db.Column(db.Boolean())
    weight = db.Column(db.Integer())
    picture = db.Column(db.String(length=20), nullable=False)
    teacher_id = db.Column(db.Integer())
    paper_id = db.Column(db.Integer(), db.ForeignKey('paper.id'), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable = True)
    questions = db.relationship('AssignmentQuestions', backref='parent_assignment', lazy=True) 


# Jakob
# AssignmentQuestions Model - this is for the questions allocated to the assignment
class AssignmentQuestions(db.Model):
    __tablename__ = 'assignment_questions'
    id = db.Column(db.Integer(), primary_key=True)
    owner = db.Column(db.Integer(), db.ForeignKey('assignment.id'), nullable = False)
    type = db.Column(db.String(), nullable = False)
    title = db.Column(db.String(), nullable = False)
    description = db.Column(db.String(), nullable = True)
    placeholder_text = db.Column(db.String(), nullable = True)


#This creates a model in the database for Uploaded files
class Upload_File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer(), db.ForeignKey('paper.id'))
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'))