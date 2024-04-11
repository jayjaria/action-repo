from flask import Flask

from app.webhook.routes import bp


def run_app():

    app = Flask(__name__)

    app.register_blueprint(bp)

    return app
