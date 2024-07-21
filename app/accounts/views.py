import os
import secrets
from datetime import datetime
from os.path import isfile
import random
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from config import app_root_path
from . import accounts
from .forms import ChangePasswordForm, UpdateAccountForm, LoginForm, SignUpForm
from .image_config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, MAX_IMAGE_SIZE
from .. import db, bcrypt
from .models import Users


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_and_save_image(file, destination_folder, target_size):
    img = Image.open(file)
    img.thumbnail(target_size)

    random_string = secrets.token_hex(10)
    original_filename, file_extension = os.path.splitext(secure_filename(file.filename))
    new_filename = f"{random_string}{file_extension}"
    image_path = os.path.join(destination_folder, new_filename)

    try:
        img.save(image_path)
        return image_path
    except Exception as e:
        flash(f"Error saving image: {e}", category="flash-error")
        return None

@accounts.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('account'))

    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        image_file = form.image_file.data

        if image_file and allowed_file(image_file.filename):
            image_path = resize_and_save_image(image_file, UPLOAD_FOLDER, MAX_IMAGE_SIZE)
            image_path = os.path.basename(image_path)
        else:
            image_path = None

        new_user = Users(username=username, email=email, password=password, image_file=image_path)
        db.session.add(new_user)
        db.session.commit()

        flash("You have successfully signed up.", category="flash-success")
        return redirect(url_for("accounts.login"))

    return render_template("signup.html", form=form)


@accounts.after_request
def after_request(response):
    if request.endpoint != 'signup' and current_user.is_authenticated:
        current_user.last_seen = datetime.now().replace(microsecond=0)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Error while updating last_seen: {str(e)}', 'flash-error')

    return response



@accounts.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accounts.account'))
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and user.validate_password(form.password.data):
            if form.remember.data == True:
                login_user(user, form.remember.data)
                flash("You have logged in.", category="flash-success")
                return redirect(url_for("accounts.account"))
            flash("You didn't remember yourself in the site. Please, check your input again.", category="flash-error")
            return redirect(url_for("accounts.login"))
        flash("You didn't put correct user credentials. Please, check them again.", category="flash-error")
        return redirect(url_for("accounts.login"))
    return render_template("login.html", form=form)

@accounts.route('/logout')
def logout():
    logout_user()
    flash("You have logged out.", category="flash-success")
    return redirect(url_for('accounts.login'))

@accounts.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html')

@accounts.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    user_image_file = current_user.image_file

    form = UpdateAccountForm(
        username=current_user.username,
        email=current_user.email,
    )

    change_password_form = ChangePasswordForm()

    if form.validate_on_submit():
        old_image_path = current_user.image_file
        old_file_name = os.path.basename(old_image_path)
        app_static_folder = os.path.join(app_root_path, 'static')
        full_old_image_path = os.path.join(app_static_folder, 'profile_images', old_file_name)
        new_image_file = form.image.data
        if new_image_file:
            image_path = resize_and_save_image(new_image_file, UPLOAD_FOLDER, MAX_IMAGE_SIZE)
            if image_path:
                current_user.image_file = os.path.basename(image_path)
                if full_old_image_path and os.path.isfile(full_old_image_path) and user_image_file != 'default.jpg':
                    os.remove(full_old_image_path)

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash("Account information updated successfully!", category='flash-success')
        return redirect(url_for('accounts.account', form=form))

    form.username.data = current_user.username
    form.email.data = current_user.email
    form.bio.data = current_user.bio
    return render_template('update_account.html', update_account_form=form)

@accounts.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        confirm_new_password = form.confirm_new_password.data
        if new_password != '':
            if new_password == confirm_new_password:
                current_user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                db.session.commit()
                flash("Password has been changed successfully", category='flash-success')
                return redirect(url_for('accounts.change_password'))

            flash("Error changing your password", category='flash-error')
            return redirect(url_for('accounts.change_password'))

    return render_template('change_password.html', form=form)
