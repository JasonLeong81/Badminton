from Intro import app, db, bcrypt, mail
from Intro.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort
from Intro.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
import secrets as  s
import os
from PIL import Image
from flask_mail import Message



p = [
    {'author':'Jason Leong',
     'title':'Blog Post 1',
     'content':'First post content',
     'date_posted':'April 20, 2020'
    },
    {'author':'Yean Chee',
     'title':'Blog Post 2',
     'content':'Second post content',
     'date_posted':'April 21, 2020'
    }
]

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page',1,type=int) # url above
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html',posts=post)

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit(): # nothing is wrong or no errors
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # password = bcrypt.check_password_hash(h,'')
        flash('You account has been created! You are now able to login.',category='success')
        return redirect(url_for('users.login')) # function not route, remember!
    return render_template('register.html',title='Register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data) # a True False value
            next_page = request.args.get('next') # args is a dictionary and we don't use ['next'] becaue this throws an error # get returns None if theres no next
            if next_page:
                return redirect(users.next_page.strip('/'))
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check email and password.','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user() # no need inputs because it knows what user is logged in
    return redirect(url_for('main.home'))

def save_picture(form_picture):
    # saving random values into static so that we don't have the same name
    random_hex = s.token_hex(8) # 8 bytes
    f_name,f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            print(dir(form.picture.data))
            picture_file = save_picture(form.picture.data) # taking the file from profile_pics (which is saved as random hex)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='New Post',form=form,legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) # if id doesnt exist, then return 404 error page
    return render_template('post.html',title=post.title,post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403) # http response for a forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit() # no need to session.add because post.title and post.content is already in the database
        flash('Your post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='Update Post',form=form,legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',1,type=int) # url above
    user = User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user).\
        order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts=post,user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='leongjason822@gmail.com',recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link: 
{url_for('users.reset_token',token=token,_external=True)}
If you did not make this request, please ignore this email.
'''
    mail.send(msg)

@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_requests.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None: # or if not user
        flash('That is an invalid or expired token.','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to login.',category='success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',form=form,title='Reset Password')






# set FLASK_APP=run.py # no spaces remember
# set FLASK_DEBUG=1 # changes reload automatically
# flask run




