from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from Flaskbl.models import User

class RegistrationForm(FlaskForm):
	username=StringField("Username",validators=[DataRequired(),Length(min=2,max=50)])
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
	submit=SubmitField("Sign up")
	def validate_username(self,username):
		user=User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError("That Username is already taken please choose another")
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()

		if user:
			raise ValidationError("That email is already taken please choose another")

class LoginForm(FlaskForm):
	#username=StringField("Username",validators=[DataRequired(),Length(min=2,max=50)])
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	remember=BooleanField("Remember Me")
	#confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")])
	submit=SubmitField("Login ")
class UpdateForm(FlaskForm):
	username=StringField("Username",validators=[DataRequired(),Length(min=2,max=50)])
	email=StringField("Email",validators=[DataRequired(),Email()])
	profile_pic=FileField("Update your profile picture",validators=[FileAllowed(['jpg','png','jpeg'])])
	submit=SubmitField("Update")
	def validate_username(self,username):

		if username.data!=current_user.username:
			user=User.query.filter_by(username=username.data).first()

			if user:
				raise ValidationError("That Username is already taken please choose another")
	def validate_email(self,email):
		if email.data!=current_user.email:
			user=User.query.filter_by(email=email.data).first()

			if user:
				raise ValidationError("That email is already taken please choose another")
class RequestResetForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired(),Email()])
	submit=SubmitField("Request password reset")
	def validate_email(self,email):
		user=User.query.filter_by(email=email.data).first()

		if user is None:
			raise ValidationError("There is no account registered in email")

class ResetPasswordForm(FlaskForm):
	password=PasswordField("Password",validators=[DataRequired()])
	confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo('password')])
	submit=SubmitField("Reset Password")