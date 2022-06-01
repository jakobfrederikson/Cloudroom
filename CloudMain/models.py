from CloudMain import db, login_manager
from CloudMain import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


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
    items = db.relationship('Upload_File', backref='owned_user', lazy=True)#Lazy gets all items from Upload_file

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

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
    # id_teacher = db.Column(db.Integer(), db.ForeignKey('account.id'))


# Jakob
# PaperStudent - holds information about what student is apart of what paper.
class PaperStudent(db.Model):
    __tablename__ = 'PaperStudent'
    id = db.Column(db.Integer(), primary_key=True)
    id_paper = db.Column(db.Integer(), db.ForeignKey('paper.id'), nullable=False)
    id_student = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable=False)


# Jakob
# ClassroomStudent - holds information about what student is apart of what classroom.
class ClassroomStudent(db.Model):
    __tablename__= 'ClassroomStudent'
    id = db.Column(db.Integer(), primary_key=True)
    id_classroom = db.Column(db.Integer(), db.ForeignKey('classroom.id'), nullable=False)
    id_student = db.Column(db.Integer(), db.ForeignKey('account.id'), nullable=False)


# Jakob
# Assignment Model - This is here for future use.
# class Assignment(db.Model):
#     __tablename__ = 'assignmnet'
#     id = db.Column(db.Integer(), primary_key=True, nullable=False)
#     paper_parent = db.Column(db.Integer(), db.ForeignKey('paper.id'))
#     assignment_name = db.Column(db.String(length=30), nullable=False)


class Upload_File(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String, nullable=False)
    data = db.Column(db.LargeBinary(length=(2 ** 32) - 1), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    owner = db.Column(db.Integer(), db.ForeignKey('account.id'))