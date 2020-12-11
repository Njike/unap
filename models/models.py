from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



db = SQLAlchemy()




# create a users table
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    super_user = db.Column(db.Boolean)
    email = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(30), nullable=True)
    username = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_seen = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.now)
    # wallet = db.relationship("Wallet", backref="user", lazy=True, uselist=False)

    # password is to be restricted to only staffs

    def isAuthenticated(self):
        return "email" in session and User.query.filter_by(email=session["email"]).first()

    def user(self):
        if self.isAuthenticated():

            return User.query.filter_by(email=session["email"]).first()
        else:
            return "Anonymous"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id":self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)
    def __str__(self):
        return f"{self.last_name.capitalize()} {self.first_name.capitalize()}"

class Nominees(db.Model):
    __tablename__ = "nominees"
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(47), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    award_category = db.Column(db.Integer, db.ForeignKey('award_category.id') )
    winner = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.name

class AwardCategory(db.Model):
    __tablename__ = "award_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    nominees = db.relationship("Nominees", backref="category")
    award = db.relationship("Awards", backref="category")


    def __str__(self):
        return self.name

class Judges(db.Model):
    __tablename__ = "judges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    image_url = db.Column(db.String(225), nullable=False)
    description = db.Column(db.Text)

    def __str__(self):
        return self.name

class BestJudgeWriteUp(db.Model):
    __tablename__ = "bestJudgeWriteUp"
    id = db.Column(db.Integer, primary_key=True)
    header_text = db.Column(db.Text, nullable=False, default="Meet our best organisers")
    text = db.Column(db.Text)


class RecentNomineeWriteUp(db.Model):
    __tablename__ = "recentNomineeWritup"
    id = db.Column(db.Integer, primary_key=True)
    header_text = db.Column(db.Text, nullable=False, default="Our Nomimees are")
    text = db.Column(db.Text)

class Awards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    award_category = db.Column(db.Integer, db.ForeignKey('award_category.id'))
    description = db.Column(db.Text)
    show_on_billboard = db.Column(db.Boolean)
    image_url = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.name} ({self.category})"
