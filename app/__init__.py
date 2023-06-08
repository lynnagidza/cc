"""Initializes the application and sets up any necessary configurations."""
import os
from flask import Flask
from . import db,main,user


def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='anya',
        DATABASE=os.path.join(app.instance_path, 'cardcraft.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello/')
    def hello():
        return 'Hello, The earth says Hello!'

    # import and register the database commands
    db.init_app(app)

    # import and register blueprints
    app.register_blueprint(main.main_bp)
    app.register_blueprint(user.user_bp)

    return app
