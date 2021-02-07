from flask import Flask

from recipe_book.config import Config
from recipe_book.routes import routes


def create_app(config_obj=Config):
    app = Flask(__name__)

    app.config.from_object(config_obj)

    for route in routes:
        app.add_url_rule(route[0], view_func=route[1])
    return app
