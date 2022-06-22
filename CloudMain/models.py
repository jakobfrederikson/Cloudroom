from CloudMain import db, login_manager, app
from CloudMain import bcrypt
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from datetime import datetime, date

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
    poster = db.relationship('Post', backref='poster', lazy=True)  # Lazy gets all items from Upload_file
    papers = db.relationship('Paper', backref='tutor', lazy=True)
    comment = db.relationship('Comments', backref='commenter', lazy=True)
    assignment_submissions = db.relationship('StudentAssignmentSubmission', backref='student', lazy=True)
    question_submissions = db.relationship('StudentQuestionSubmission', backref='student', lazy=True)

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

    #generate token for reseting password
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'], )
        return s.dumps({'user_id': self.id})

    #verify the token
    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, expires_sec)['user_id']
        except:
            return None
        return Account.query.get(user_id)

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
    paper_description = db.Column(db.Text,nullable=False)
    id_classroom = db.Column(db.Integer(), db.ForeignKey('classroom.id'), nullable=False)
    account_id = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable=False)
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
    picture = db.Column(db.String(length=20), nullable=False)
    isPublished = db.Column(db.Boolean())
    teacher_id = db.Column(db.Integer())
    paper_id = db.Column(db.Integer(), db.ForeignKey('paper.id'), nullable = False)
    class_id = db.Column(db.Integer(), db.ForeignKey('classroom.id'), nullable = False)
    questions = db.relationship('Question', backref='owned_assignment', lazy=True) 
    student_assignment_submissions = db.relationship('StudentAssignmentSubmission', backref='assignment', lazy=True)

    def serialize(self):
        return {"id" : self.id,
                "name": self.owner,
                "description": self.description,
                "creationDate": self.creationDate,
                "dueDate": self.dueDate,
                "isCompleted": self.isCompleted,
                "weight": self.weight,
                "picture": self.picture,
                "isPublished": self.isPublished,
                "teacher_id": self.teacher_id,
                "paper_id": self.paper_id}


# Jakob
# Question Model - this is for the questions allocated to the assignment
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer(), primary_key=True)
    owner = db.Column(db.Integer(), db.ForeignKey('assignment.id'), nullable = False)
    type = db.Column(db.String(), nullable = False)
    title = db.Column(db.String(), nullable = False)
    description = db.Column(db.String(), nullable = True)
    placeholder_text = db.Column(db.String(), nullable = True)
    student_question_submission = db.relationship('StudentQuestionSubmission', backref='owned_question', lazy = True)

    def serialize(self):
        return {"id" : self.id,
                "owner": self.owner,
                "type": self.type,
                "title": self.title,
                "description": self.description,
                "placeholder_text": self.placeholder_text}


# Jakob
# StudentAssignmentSubmission - this table shows general information about a students assignment submission
class StudentAssignmentSubmission(db.Model):
    __tablename__ = 'student_assignment_submission'
    id = db.Column(db.Integer(), primary_key = True)
    assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'), nullable = False)
    student_id = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable = False)    
    has_submitted = db.Column(db.Boolean(), nullable = True)
    submission_date = db.Column(db.Date(), default = date.today(), nullable = True)
    grade = db.Column(db.Float(), nullable = True) # the grade can be set later on when the teacher comes to mark it


# Jakob
# StudentQuestionSubmission - this table shows the content of the assignment submission
class StudentQuestionSubmission(db.Model):
    __tablename__ = 'student_question_submission'
    id = db.Column(db.Integer(), primary_key = True)
    assignment_id = db.Column(db.Integer(), db.ForeignKey('assignment.id'), nullable = False)
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id'), nullable = False)
    student_id = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable = False)    
    question_content = db.Column(db.String(), nullable = True) # Incase student wants to submit empty question
    grade = db.Column(db.Float(), nullable = True) # the grade can be set later on when the teacher comes to mark it


#This creates a model in the database for Uploaded files
class Upload_File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'))
#This creates the model for Post details
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer(), db.ForeignKey('paper.id'))
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'))
    comment = db.relationship('Comments', backref='poster', lazy=True)

# This creates the model for Comments details
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))
    comment = db.Column(db.Text(),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'))
