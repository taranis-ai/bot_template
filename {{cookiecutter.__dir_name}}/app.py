from {{cookiecutter.__package_name}}.config import Config
from taranis_base_bot import create_app

app = create_app(Config.PACKAGE_NAME, Config)
