from flask import Flask, redirect

from app.routes.game import game_bp


def create_app(config_object="app.config.DevelopmentConfig"):
    """Crea y configura la aplicación Flask."""

    app = Flask(__name__)

    app.config.from_object(config_object)

    app.register_blueprint(game_bp, url_prefix="/game")

    @app.route("/", methods=["GET"])
    def home():
        return redirect(app.config.get("MAIN_REDIRECT_URL", "/game"))

    return app
