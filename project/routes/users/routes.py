from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user
from flask_user import (
    login_required,
    UserManager,
    UserMixin,
    current_user,
    roles_required,
)

from project.extensions import db

from project.routes.users import bp
from project.models.user import User
from flask import current_app

from project.tokens import generate_confirmation_token, confirm_token
from project.emails import send_email

# User Manager
# Setup Flask-User and specify the User data-model
user_manager = UserManager(current_app, db, User)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    print("Current user authenticated?", current_user.is_authenticated)
    # print("Current user confirmed?",current_user.confirmed)
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for('blogs.list_all_blogs'))
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.objects(email=email):
            flash('Email Already Registered!', 'success')
            return redirect("unconfirmed")

        user = User(email=email,
                    username=username,
                    password=user_manager.hash_password(password=password),
                    confirmed=False,
                    registered_on=datetime.datetime.now(),
                    admin=False,
                    confirmed_on=None)
        
        user.save()
        print(user.id)
        
        # db.session.add(user)
        # db.session.commit()
        
        # Generate verification token and send email to user
        # token = generate_confirmation_token(user.email)
        # confirm_url = url_for('users.confirm_email', token=token, _external=True)
        # html = render_template('users/activate.html', confirm_url=confirm_url)
        # subject = "Please confirm your email"
        # send_email(user.email, subject, html)
        # flash("Confirmation link has been sent to the registered email. Kindly confirm it!", 'success')
        return redirect("unconfirmed")
    
    return render_template("users/register.html")

@bp.route("/", methods=['GET', 'POST'])
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.confirmed:
        return redirect(url_for('blogs.list_all_blogs'))
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.find_record(key=email)
        print("I am in Login, ", user)
        if user is not None and user.check_password(password=password):
            login_user(user)
            flash('Welcome.', 'success')
            return redirect('unconfirmed')
        return redirect("register")
    return render_template("users/login.html")

@bp.route("/logout")
def logout():
    logout_user()
    return redirect('login')

@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.objects(email=email)
    
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        user.save()
        # db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('blogs.blogs'))

@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('blogs.list_all_blogs'))
    flash('Please confirm your account!', 'warning')
    return render_template('users/unconfirmed.html')


@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('users/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('users.unconfirmed'))
