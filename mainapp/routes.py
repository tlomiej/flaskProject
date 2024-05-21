import bcrypt
import os
from flask import render_template, url_for, flash, redirect, request, abort
from mainapp import app, db, bcrypt, mail
from mainapp.models import User, Collection
from mainapp.forms import (RegistrationForm,
                           LoginForm,
                           UpdateAccountForm,
                           NewDataForm,
                           RequestResetForm,
                           ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image
from flask_mail import Message




@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    data = Collection.query.order_by(Collection.date_created.desc()).paginate(page=page, per_page=5)

    #data = Collection.query.paginate(page=page, per_page=5)
    return render_template('home.html', posts=data)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check emil and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_foto', picture_fn)
    form_picture.save(picture_path)

    if f_ext != '.svg':
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
    return picture_fn


@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_foto/' + current_user.image_file)
    return render_template(
        'account.html', title='Account', image_file=image_file, form=form)

@app.route("/data/new", methods=['GET', 'POST'])
@login_required
def new_data():
    form = NewDataForm()
    if form.validate_on_submit():
        collections = Collection(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(collections)
        db.session.commit()

        flash('Add data', 'success')
        return redirect(url_for('home'))


    return render_template('create_data.html', title="New data", form=form, legend="New data")


@app.route("/data/<data_id>")
def data(data_id):
    data = Collection.query.get_or_404(data_id)
    return render_template('data.html', title=data.title, data=data)


@app.route("/data/<data_id>/update", methods=['GET', 'POST'])
@login_required
def updatedata(data_id):
    data = Collection.query.get_or_404(data_id)
    if(data.author != current_user):
        abort(403)
    form = NewDataForm()
    if form.validate_on_submit():
        data.title = form.title.data
        data.content = form.content.data
        db.session.commit()
        flash('Data updated!', 'success')
        return redirect(url_for('data', data_id=data.id))

    elif request.method == 'GET':

        form.title.data =  data.title
        form.content.data = data.content
    return render_template('create_data.html', title="Update data", form=form, legend="Update data")


@app.route("/data/<data_id>/delete", methods=['GET', 'POST'])
@login_required
def deletedata(data_id):
    data = Collection.query.get_or_404(data_id)
    if(data.author != current_user):
        abort(403)
    db.session.delete(data)
    db.session.commit()
    flash('Data has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def userdata(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    data = Collection.query.filter_by(author=user).order_by(Collection.date_created.desc()).paginate(page=page, per_page=5)

    #data = Collection.query.paginate(page=page, per_page=5)
    return render_template('userdata.html', posts=data, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender="noreplay@demo.com",
                  recipients=[user.email])
    msg.body = f'''
    To reset your password, visit the following link
{url_for('reset_token', token=token, _external=True)}
    
If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form  = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password", form=form)