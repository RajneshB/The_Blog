from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from Flaskbl import db
from Flaskbl.models import Post
from Flaskbl.posts.forms import PostForm
 
posts=Blueprint('posts',__name__)



@posts.route("/Post/new",methods=['GET','POST'])
@login_required
def new_post():
	form=PostForm();
	if form.validate_on_submit():
		post=Post(Title=form.title.data,Content=form.content.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash(f'Your content have been posted',"success")
		return redirect(url_for('main.home'))
	return render_template('Post_new.html',title='New Post',legend='New Post',form=form)
@posts.route("/post/<int:post_id>")
def post(post_id):
	post=Post.query.get_or_404(post_id)
	return render_template("Post.html",title=post.Title,post=post)

@posts.route("/post/<int:post_id>/update",methods=["GET","POST"])
@login_required
def update_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author.id != current_user.id:
		abort(403)
	form=PostForm()
	if form.validate_on_submit():
		post.Title=form.title.data
		post.Content=form.content.data
		db.session.commit()
		flash(f'You have updated your post',"success")
		return redirect(url_for('posts.post',post_id=post.id))
	if request.method=="GET":
		form.title.data=post.Title
		form.content.data=post.Content


	return render_template('Post_new.html',title='New Post',legend='Update Form',form=form)

@posts.route("/post/<int:post_id>/delete",methods=["POST"])
@login_required
def delete_post(post_id):
	post=Post.query.get_or_404(post_id)
	if post.author.id != current_user.id:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash(f'Your post have been deleted',"success")
	return redirect(url_for('main.home'))
@posts.route("/user/<string:username>")
def user_posts(username):
	page=request.args.get('page',1,type=int)
	user=User.query.filter_by(username=username).first_or_404()
	posts=Post.query.filter_by(author=user)\
	.order_by(Post.date.desc())\
	.paginate(page=page,per_page=5)
	return render_template('user_post.html',posts=posts,user=user)
