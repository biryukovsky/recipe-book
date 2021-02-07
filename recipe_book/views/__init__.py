from flask.views import MethodView
from flask import render_template


class IndexView(MethodView):
    def get(self):
        return render_template('index.html')


# Auth

class LoginView(MethodView):
    def get(self):
        return render_template('login.html')


class SignupView(MethodView):
    def get(self):
        return render_template('signup.html')


class LogoutView(MethodView):
    def get(self):
        return 'Logout'
