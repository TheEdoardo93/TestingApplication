from flask import Flask
from src.api.blueprint import app_blueprint


class InitFlaskApp(object):
    def __init__(self, host='localhost', port=5000, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

    def create_app(self):
        # Define a Flask application
        app = Flask(__name__, instance_relative_config=False)
        app.config.from_pyfile(filename='flask_config_test.py')

        # Register the blueprint
        app.register_blueprint(app_blueprint)

        return app
