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


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


# Classroom model, added by Jakob
class Classroom(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    classroom_name = db.Column(db.String(length=30), nullable=False)
    classroom_subject = db.Column(db.String(length=40), nullable=True)
    classroom_room_number= db.Column(db.String(length=5), nullable=True)
    classroom_picture = db.Column(db.String(length=20), nullable=False)