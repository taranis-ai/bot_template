from flask import Flask
from {{cookiecutter.__package_name}} import router


def create_app():
    app = Flask(__name__)
    app.config.from_object("{{cookiecutter.__package_name}}.config.Config")

    with app.app_context():
        init(app)

    return app


def init(app: Flask):
    router.init(app)


if __name__ == "__main__":
    create_app().run()
