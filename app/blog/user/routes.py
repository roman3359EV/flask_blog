from flask import render_template, request, redirect, url_for, Response, flash
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from . import user_routes
from ..models import User, Role, db


@user_routes.route('/login', methods=['GET', 'POST'])
def login() -> str|Response:
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    if request.method == 'POST':
        user_name = request.form.get('login')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember_me') else False

        user = User.query.filter_by(login=user_name).filter_by(active=True).first()

        if not user or not user.check_password(password):
            flash('Please check your login or password and try again.')
            return render_template('login.html', hide_header=True)
        else:
            login_user(user, remember=remember_me)
            return redirect(url_for('users.profile'))

    return render_template('login.html', hide_header=True)


@user_routes.route('/registration', methods=['GET', 'POST'])
def registration() -> str|Response:
    if current_user.is_authenticated:
        return redirect(url_for('users.profile'))

    if request.method == 'POST':
        name = request.form.get('name')
        user_login = request.form.get('login')
        password = request.form.get('password')

        user = User.query.filter_by(login=user_login).first()
        if user:
            flash('Please check your login or password and try again.')
            return render_template('registration.html', hide_header=True)

        new_user = User(
            name=name,
            login=user_login,
            password=generate_password_hash(password),
            # role_id=Role.ROLE_USER,
            # active=True
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('registration.html', hide_header=True)


@user_routes.route('/logout', methods=['GET'])
def logout() -> Response:
    logout_user()
    return redirect(url_for('users.login'))


@user_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile() -> str|Response:
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

    if request.method == 'POST':
        fields = request.form.to_dict()
        fields_save = {key: value for key, value in fields.items()
                       if key in ('name', 'login', 'password', 'confirm_password')}

        if fields_save.get('password') == '':
            del fields_save['password']
            del fields_save['confirm_password']
        elif fields_save['password'] != fields_save['confirm_password']:
            flash('Password and Confirm Password do not match')

            dict_user = {
                'name': current_user.name,
                'login': current_user.login,
                'balance': current_user.get_balance()
            }

            return render_template('profile.html', user=dict_user)

        current_user.name = fields_save['name']
        current_user.login = fields_save['login']
        if fields_save.get('password') is not None \
                and fields_save['password'] == fields_save['confirm_password']:
            current_user.password = generate_password_hash(fields_save['password'])
        db.session.commit()

    dict_user = {
        'name': current_user.name,
        'login': current_user.login,
        'balance': User.get_balance(current_user)
    }

    return render_template('profile.html', user=dict_user)


@user_routes.route('/delete', methods=['POST'])
@login_required
def delete() -> Response:
    current_user.active = False
    db.session.commit()

    logout_user()

    return redirect(url_for('users.login'))