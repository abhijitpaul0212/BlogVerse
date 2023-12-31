import datetime
from flask import redirect, url_for, flash, current_app
from flask_user import UserManager
from src.routes.main import bp
from src.extensions import db
from src.models.user import User


user_manager = UserManager(current_app, db, User)


def password_hashing(password):
    return user_manager.hash_password(password)


@bp.route("/")
@bp.route("/index")
@bp.route("/index.htm")
@bp.route("/index.html")
def home_page():
    """
    Landing/Home Page, accessible before sign in/login. If logged in, user is redirected to the Main Page.
    At first access/touch the user 'admin' is created using environment variables for the password and email address.
    The admin user creation is here as it will be created twice on Heroku if placed in the main code.
    """

    # Create admin user as first/default user, if admin does not exist.
    # Password and e-mail are set using environment variables.
    all_users = [all_user.username for all_user in User.objects.all()]

    if 'admin' not in all_users:
        try:
            user = User(
                username="admin",
                first_name="Administrator",
                last_name="Administrator",
                email='ad@min.com',
                email_confirmed_at=datetime.datetime.utcnow(),
                password=password_hashing('admin'),
            )
            user.roles.append("Admin")
            user.save()

            flash("'admin' account created.", "success")
            bp.logger.info(
                "'admin' account is created at startup if the user doesn't exist: [SUCCESS] - (index.html)."
            )
        except Exception:
            flash("'admin' account not created.", "danger")
            bp.logger.critical(
                "'admin' account is created at startup if the user doesn't exist: [FAILURE] - (index.html)."
            )
    return redirect(url_for('blogs.list_all_blogs'))
