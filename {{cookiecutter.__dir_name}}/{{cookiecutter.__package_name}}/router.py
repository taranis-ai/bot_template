from flask import Flask, Blueprint, jsonify, request
from flask.views import MethodView

from {{cookiecutter.__package_name}}.predictor import Predictor
from {{cookiecutter.__package_name}}.predictor_factory import PredictorFactory


class BotEndpoint(MethodView):
    def __init__(self, processor: Predictor) -> None:
        super().__init__()
        self.processor = processor

    def post(self):
        data = request.get_json()

        # pre-process data here and pass it to self.processor.predict method
        # e.g. extracted_data = data.get("key", "")
        #      processor_result = self.processor.predict(extracted_data)
        processor_result = None

        # return processor_result as JSON
        return jsonify({"<result_name>": processor_result})


class HealthCheck(MethodView):
    def get(self):
        return jsonify({"status": "ok"})

class ModelInfo(MethodView):
    def __init__(self, processor: Predictor):
        super().__init__()
        self.processor = processor

    def get(self):
        return jsonify(self.processor.modelinfo)


def init(app: Flask):
    processor = PredictorFactory()
    app.url_map.strict_slashes = False
    bot_bp = Blueprint("bot", __name__)
    bot_bp.add_url_rule("/", view_func=BotEndpoint.as_view("predict", processor=processor))
    bot_bp.add_url_rule("/health", view_func=HealthCheck.as_view("health"))
    app.register_blueprint(bot_bp)
