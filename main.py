import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from blueprints.hubstaff import hubstaff_blueprint


def page_not_found(e):
    return jsonify({"msg": "page not found"})


def create_app(app_config):
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(app_config)

    app.register_error_handler(404, page_not_found)

    app.register_blueprint(hubstaff_blueprint)

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(os.path.join(app.root_path, "static"), "favicon.png")

    return app


if __name__ == "__main__":
    if "FLASK_ENV" in os.environ:
        app = create_app(os.environ["FLASK_ENV"])
    else:
        app = create_app("config.DevelopmentConfig")
    app.run(host=app.config["HOST"], threaded=True)
