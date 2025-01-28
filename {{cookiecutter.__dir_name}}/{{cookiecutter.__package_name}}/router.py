from flask import Flask, Blueprint, jsonify, request
from flask.views import MethodView

from {{cookiecutter.__package_name}}.{{cookiecutter.__module_name}} import {{cookiecutter.__class_name}}


class BotEndpoint(MethodView):
    def __init__(self, bot: {{cookiecutter.__class_name}}) -> None:
        super().__init__()
        self.bot = bot

    def post(self):
        data = request.get_json()

        # pre-process data here and pass it to bot.predict method
        # bot_result = self.bot.predict(<add_bot_args>)
        bot_result = None

        # return bot_result as JSON
        return jsonify({"<result_name>": bot_result})


class HealthCheck(MethodView):
    def get(self):
        return jsonify({"status": "ok"})


def init(app: Flask, bot: {{cookiecutter.__class_name}}):
    app.url_map.strict_slashes = False

    bot_bp = Blueprint("bot", __name__)
    bot_bp.add_url_rule("/", view_func=BotEndpoint.as_view("predict", bot=bot))
    bot_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
    app.register_blueprint(bot_bp)
