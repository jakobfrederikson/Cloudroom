from CloudMain import db, login_manager, app
from CloudMain import bcrypt
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer

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
    papers = db.relationship('Paper', backref='tutor', lazy=True)

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
    owner = db.Column(db.String(length=30), nullable=False)
    description = db.Column(db.String(), nullable = True)
    creationDate = db.Column(db.Date())
    dueDate = db.Column(db.Date())
    isCompleted = db.Column(db.Boolean())
    weight = db.Column(db.Integer())
    picture = db.Column(db.String(length=20), nullable=False)
    isPublished = db.Column(db.Boolean())
    teacher_id = db.Column(db.Integer())
    paper_id = db.Column(db.Integer(), db.ForeignKey('paper.id'), nullable = False)
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable = True)
    questions = db.relationship('AssignmentQuestions', backref='owned_assignment', lazy=True) 

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
                "paper_id": self.paper_id,
                "owner": self.owner}


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

    def serialize(self):
        return {"id" : self.id,
                "owner": self.owner,
                "type": self.type,
                "title": self.title,
                "description": self.description,
                "placeholder_text": self.placeholder_text}


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