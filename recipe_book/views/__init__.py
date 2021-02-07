from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user

from recipe_book.models import User


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')


# Auth

class LoginView(MethodView):
    def get(self):
        return render_template('login.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = current_app.db_session.query(User).filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            print('incorrect data')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('index'))


class SignupView(MethodView):
    def get(self):
        return render_template('signup.html')

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        user = current_app.db_session.query(User).filter_by(username=username).first()
        if user:
            return redirect(url_for('signup'))

        new_user = User(username=username,
                        password=generate_password_hash(password))
        current_app.db_session.add(new_user)
        current_app.db_session.commit()

        return redirect(url_for('index'))


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        return redirect(url_for('index'))
