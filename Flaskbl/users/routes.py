from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Flaskbl import db, bcrypt
from Flaskbl.models import User, Post
from Flaskbl.users.forms import (RegistrationForm, LoginForm, UpdateForm,
                                   RequestResetForm, ResetPasswordForm)
from Flaskbl.users.utils import save_image, send_reset_token
users=Blueprint('users',__name__)


@users.route("/register",methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user=User(username=form.username.data,email=form.email.data,password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created for {form.username.data}','success')
		return redirect(url_for('users.Login'))
	return render_template('register.html',title='Register',form=form)

@users.route("/Login",methods=["GET","POST"])
def  Login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()

		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user,remember=form.remember.data)
			flash(f'you have logged in','success')
			next_page=request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash(f'incorrect info please check your email and password','danger')
	return render_template('login.html',title='Login',form=form)

@users.route("/Logout")
def  Logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route("/account",methods=["GET","POST"])
@login_required
def account():
	form=UpdateForm()
	if form.validate_on_submit():
		current_user.username=form.username.data
		current_user.email=form.email.data
		if form.profile_pic.data:
			picture=save_image(form.profile_pic.data)
			current_user.image_file=picture
		db.session.commit()	
		flash(f'You have updated your account','success')
		return redirect(url_for('users.account'))
	elif request.method=='GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
	return render_template('account.html',title='account',image_file=image_file,form=form)
@users.route("/user/<string:username>")
def user_posts(username):
	page=request.args.get('page',1,type=int)
	user=User.query.filter_by(username=username).first_or_404()
	posts=Post.query.filter_by(author=user)\
	.order_by(Post.date.desc())\
	.paginate(page=page,per_page=5)
	return render_template('user_post.html',posts=posts,user=user)

@users.route("/resetpassword",methods=["GET","POST"])
def reset_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form =RequestResetForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		send_reset_token(user)
		flash(f'message sent to your email','info')
		return redirect(url_for('users.Login'))
	return render_template('request_reset.html',title='Request Reset',form=form)
@users.route("/resetpassword<token>",methods=["GET","POST"])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user=User.verify_reset_token(token)
	if user is None:
		flash(f'the token is invalid or expired','warning')
		return redirect(url_for('users.reset_password'))
	form =ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password=hashed_pw

		
		db.session.commit()
		flash(f'Your password has been updated','success')
		return redirect(url_for('users.Login'))
	return render_template('reset_token.html',title='Reset Password',form =form)