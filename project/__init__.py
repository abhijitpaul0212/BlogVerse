# from dotenv import load_dotenv

# from flask import Flask
# from config import DevelopmentConfig

# from project.routes.main import bp as main_bp
# from project.routes.users import bp as users_bp
# from project.routes.blogs import bp as blogs_bp
# from project.extensions import db, login_manager, mail
# from project.models.blog import Category

# from project.routes.blogs.routes import get_all_categories

# from flask import Flask, render_template, url_for, redirect, request, flash
# from flask_login import login_required, current_user, login_user, logout_user
# from flask_user import (
#     login_required,
#     UserManager,
#     UserMixin,
#     current_user,
#     roles_required,
# )
# from flask_mongoengine import (
#     MongoEngine,
#     MongoEngineSession,
#     MongoEngineSessionInterface,
# )

# from flask_wtf.csrf import CSRFProtect, CSRFError

# load_dotenv()

# """Application-Factory pattern

# Args:
#     config_class (Config): Config 
# """
# # Create flask instance
# app = Flask(__name__, static_folder="static", template_folder="templates")
# app.secret_key = 'zjHUlXmuO85d2LOHqbzpd8_Qvv0XhUYxDr0ZRg2UG04'
# app.config.from_object(__name__ + ".DevelopmentConfig")

# csrf = CSRFProtect(app)
# csrf.init_app(app)

# # extensions
# # db.init_app(app)  
# # login_manager.init_app(app)
# # mail.init_app(app)
# # Use Flask Sessions with Mongoengine
# app.session_interface = MongoEngineSessionInterface(db)
    
# # login_manager.login_view = 'users.login'

# # Register blueprints here
# app.register_blueprint(main_bp)
# app.register_blueprint(users_bp)
# app.register_blueprint(blogs_bp)

# # push context manually to app
# # with app.app_context():
# #     pass
#     # print(db.connection())
#     # db.create_all()  # Handling prerequisite of creating all tables 
#     # get_all_categories()


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)
