from app import app
from functools import wraps
from flask import Flask, render_template, url_for, request, jsonify, redirect, url_for, make_response, flash, send_from_directory, abort
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FileField, PasswordField, HiddenField, IntegerField, SubmitField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator, ValidationError
from wtforms.widgets import TextArea

from passlib.hash import sha256_crypt

from models.models import *




@app.context_processor
def g():
    donate = Donate.query.first()
    socials = Social.query.all()
    return {"donate":donate, "socials":socials}



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if User().isAuthenticated():
            return f(*args, **kwargs)
        else:
            # print(str(f).split(' ')[1], "=================")
            # flash("Unauthorized, Please login", "warning")
            n = str(f).split(' ')[1]
            if n == "logout":
                return redirect(url_for("login"))
            return redirect(url_for("login", next=n))
    return wrap



@app.route("/")
def index():
    winner = Nominees.query.filter_by(winner=True).first()
    nominees = Nominees.query.all()
    judges = JudgesReplacement.query.all()
    judges_text = BestJudgeWriteUp.query.first()
    nominee_text = RecentNomineeWriteUp.query.first()
    awards = Awards.query.all()
    award = Awards.query.filter_by(show_on_billboard=True).first()
    return render_template(
        'index.html', award=award, winner=winner, nominees=nominees, judges=judges, judges_text=judges_text, nominee_text=nominee_text, awards=awards)

@app.route("/about-us/")
def about_us():
    return render_template('about-us/index.html')

@app.route("/nominee_category/")
def nominee_category():
    nominees = Nominees.query.all()
    return render_template('nominee_category/index.html', nominees=nominees)

@app.route("/nominee_category/<string:name>/")
def nominee_category_detail(name):
    nominee = Nominees.query.filter_by(name=name).first()
    if nominee:
        return render_template("nominee/papazian-jewelry/index.html", nominee=nominee)
    else:
        abort(404)

@app.route('/award-winners/')
def award_winners():
    winners = Nominees.query.all()
    return render_template('award-winners/index.html', winners=winners)


@app.route("/award/<string:name>/")
def award_category_detail(name):
    nominee = Awards.query.filter_by(name=name).first()
    if nominee:
        return render_template("nominee/papazian-jewelry/index.html", nominee=nominee)
    else:
        abort(404)




@app.route('/organizers/')
def agencies():
    judges = Judges.query.all()
    return render_template('agencies-freelancers/index.html', judges=judges)

@app.route("/organiser/<string:name>/")
def organiser_category_detail(name):
    nominee = Judges.query.filter_by(name=name).first()
    if nominee:
        return render_template("nominee/papazian-jewelry/index.html", nominee=nominee)
    else:
        abort(404)




