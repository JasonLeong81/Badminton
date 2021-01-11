from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import *
from flask_login import LoginManager
from flask_mail import Mail
import os # for environmental variable
from Intro.config import Config


# app = Flask(__name__)
# app.config.from_object(Config)
# app.config['SECRET_KEY'] = 'jason'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # three slashes mean current directory

# db = SQLAlchemy(app)
# bcrypt = Bcrypt()
# login_manager = LoginManager(app)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # for login required # users.login, where users is the blueprint
login_manager.login_message_category = 'info'

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'leongjason822@gmail.com' # what we use to send emails
# app.config['MAIL_PASSWORD'] = '378100Yc'

# mail = Mail(app)
mail = Mail()





# from Intro import routes

# from Intro.users.routes import users
# app.register_blueprint(users)
#
# from Intro.posts.routes import posts
# app.register_blueprint(posts)
#
# from Intro.main.routes import main
# app.register_blueprint(main)

def create_app(config_class=Config):
    # one problem with this function is that we now do not have app that other modules are importing from
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from Intro.users.routes import users
    app.register_blueprint(users)

    from Intro.posts.routes import posts
    app.register_blueprint(posts)

    from Intro.main.routes import main
    app.register_blueprint(main)

    from Intro.errors.handlers import errors
    app.register_blueprint(errors)

    return app







