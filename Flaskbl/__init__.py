import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from Flaskbl.config import Config

db=SQLAlchemy()
bcrypt=Bcrypt()

login_manager=LoginManager()
login_manager.login_view='users.Login'
login_manager.login_message_category='info'


mail=Mail()

def create_app(config_class=Config):
	app=Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	from Flaskbl.users.routes import users
	from Flaskbl.posts.routes import posts
	from Flaskbl.main.routes import main
	from Flaskbl.errors.handlers import errors

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)
	return app