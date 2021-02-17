from flask import Flask
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_login import LoginManager

from recipe_book.config import Config
from recipe_book.routes import routes


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config.from_object(config_obj)

    from recipe_book.db import db_engine
    from recipe_book.models import User

    app.db_session = scoped_session(sessionmaker(autoflush=False,
                                                 autocommit=False,
                                                 bind=db_engine))

    for route in routes:
        app.add_url_rule(route[0], view_func=route[1])

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return app.db_session.query(User).get(int(user_id))

    @app.teardown_appcontext
    def remove_db_session(exc=None):
        app.db_session.remove()

    return app
