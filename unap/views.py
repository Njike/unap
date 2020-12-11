from app import app
from functools import wraps
from flask import Flask, render_template, url_for, request, jsonify, redirect, url_for, make_response, flash, send_from_directory, abort
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FileField, PasswordField, HiddenField, IntegerField, SubmitField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator, ValidationError
from wtforms.widgets import TextArea

from passlib.hash import sha256_crypt

from models.models import *



class RegistrationForm(FlaskForm):
    username = StringField("Userame", validators=[DataRequired(), Length(min=2)])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8), EqualTo("password1", message='Passwords must match')])
    email = StringField("Email", validators=[Email()])
    agree = BooleanField(validators=[DataRequired()])
#     submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("User already exist")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exist, please choose a different one")



class LoginForm(FlaskForm):
    emailorUsername = StringField("Email or Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember me")

#     def validate_email(self, email):

        # email_validator.validate_email(
        #             email.data.strip(),
        #             check_deliverability=False,
        #             allow_smtputf8=True,
        #             allow_empty_local=False,
        #         )

class AccountForm(FlaskForm):
    username = StringField("Username")
    firstname = StringField("Firstname", validators=[DataRequired(), Length(min=2)])
    lastname = StringField("Lastname", validators=[DataRequired(), Length(min=2)])
    email = StringField("Email")
    btc_address = StringField("Bitcoin Address")
    eth_address = StringField("Ethereum Address")
    litecoin_address = StringField("Litecoin Address")
    bch_address = StringField("Bitcoin Cash Address")
    current_password = PasswordField("Current Password", validators=[])
    new_password = PasswordField("New Password")
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("new_password", message='Passwords must match')])

    def validate_current_password(self, password):
        user = User().user()
        print(password.data)
        if password.data and not sha256_crypt.verify(password.data, user.password):
            raise ValidationError("Invalid password, please input the correct passowrd")



class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Invalid email address")

class PasswordResetForm(FlaskForm):
    password1 = PasswordField("New Password", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8), EqualTo("password1", message='Passwords must match')])


@app.context_processor
def g():
#     site_detail = SiteDetails.query.first()
#     user=User().user()
#     if type(User().user()) == str:
#         return {"current_user":None, "site_detail":site_detail, "date":datetime.now()}
#     detail = {"deposits":[],"withdrawals":[],"pendingWithdrawals":[], "pendingDeposits":[]}
#     transactions = Transaction.query.filter_by(wallet=user.wallet).all()
#     for transaction in transactions:
#         if transaction.is_deposit and transaction.is_successful:
#             detail["deposits"].append(transaction.deposit.amount)
#         elif transaction.is_withdrawal and transaction.is_successful:
#             detail["withdrawals"].append(abs(transaction.withdrawal.amount))
#         elif transaction.is_withdrawal and not transaction.is_successful:
#             detail["pendingWithdrawals"].append(abs(transaction.withdrawal.amount))
#         elif transaction.is_deposit and not transaction.is_successful:
#             detail["pendingDeposits"].append(transaction.deposit.amount)



#     return {"detail":detail,"site_detail":site_detail, "current_user":User().user(), "balance":round(Transaction.query.filter_by(wallet=User().user().wallet).first().balance(),6), "date":datetime.now()}
    return {}



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
    judges = Judges.query.all()
    judges_text = BestJudgeWriteUp.query.first()
    nominee_text = RecentNomineeWriteUp.query.first()
    awards = Awards.query.all()
    return render_template(
        'index.html', winner=winner, nominees=nominees, judges=judges, judges_text=judges_text, nominee_text=nominee_text, awards=awards)

@app.route("/about-us/")
def about_us():
    return render_template('about-us/index.html')

@app.route("/terms-of-usage/")
def terms():
    return render_template('terms-of-usage/index.html')

@app.route("/my-account/")
def my_account():
    form_login = LoginForm()
    form_register = RegistrationForm()

    return render_template('my-account/index.html', form_login=form_login, form_register=form_register)

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

@app.route("/winner/")
def winner():
    return render_template("award-winners/index.html")


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



@app.route("/support/")
def support():
    return "support"

@app.route("/forgot_password/", methods=["GET", "POST"])
def forgot_password():
    form = RequestResetForm()
    if User().isAuthenticated():
        return redirect(url_for("index"))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("Invalid email address","warning")
            return redirect(request.url)
        send_reset_email(user)
        flash("A link will be sent sent to your Email","info")
        return redirect(url_for("login"))

    return render_template("forgot-password.html", form=form)

@app.route("/register/")
def register():
#     single_user = User.query.all()
    if User().isAuthenticated():
        return redirect(url_for("dashboard"))
    form = RegistratonForm()
    form.email.data = request.args.get("email")
#     cryptocurrency = CryptoCurrency.query.all()



    if request.method == "POST":

        if not form.validate_on_submit():
            flash("Please fill in the required fields", "warning")
            return redirect(request.url)



        user = User()
        user.first_name = form.firstname.data
        user.last_name = form.lastname.data
        user.super_user = False
        user.username = form.username.data
        user.email = form.email.data
        user.password = sha256_crypt.encrypt(str(form.password1.data))

        if not single_user:
            user.super_user = True
            wallet = Wallet(user=user)


            db.session.add(wallet)
            session["isAuthenticated"] = True
            session["email"] = user.email

            db.session.add(user)
            create_transaction(amount=0.0,wallet=wallet,is_deposit=True, is_withdrawal=True, is_successful=True)
            flash("Welcome Admin, please fill up the necessary records", "success")
            return redirect("/admin")



        wallet = Wallet(user=user)


        db.session.add(wallet)

        db.session.add(user)
        create_transaction(amount=0.0,wallet=wallet,is_deposit=True, is_withdrawal=True, is_successful=True)

        return redirect(url_for("login"))

    return render_template("register.html", form=form)



@app.route("/login/")
def login():
    if User().isAuthenticated():
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password_candidate = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()

        if user:
            password = user.password



            if sha256_crypt.verify(password_candidate, password):
                if remember:
                    session.permanent = True
                session["isAuthenticated"] = True
                session["email"] = email

                session["username"] = user.username

                if request.args and request.args["next"]:
                    return redirect(url_for(request.args["next"]))

                return redirect(url_for("dashboard"))
            else:
                error = "Invalid email or password"
                flash(error, "danger")
                render_template("login.html", form=form)

        else:

            error = "Invalid email or password"
            flash(error, "danger")
            render_template("login.html",form=form)

    return render_template('login.html', form=form)

@app.route("/logout/")
@login_required
def logout():
    User().user().last_seen = datetime.now()
    db.session.commit()
    session.clear()
    return redirect(url_for("login"))
