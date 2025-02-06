import fileinput
import subprocess
from pathlib import Path

model_import_str_template = """Config.MODEL == '<model>':
            from {{cookiecutter.__module_name}}.<model> import <model_class>
            return <model_class>(*args, **kwargs)"""

model_file_str = """from {{cookiecutter.__module_name}}.config import Config
from {{cookiecutter.__module_name}}.predictor import Predictor
# import model libraries

class <model_class>(Predictor):

    # add huggingface model name (e.g. facebook/bart-large-cnn)
    # needed for using the modelinfo endpoint
    model_name = None

    def __init__(self):
        # instantiate model here
        self.model = None

    def predict(self):
        # add inference code here
        raise NotImplementedError("The class <model_class> must implement the 'predict' method")
"""

model_config_str = """    MODEL: Literal<model_list> = <default_model>"""

model_build_arg_str = """INCLUDED_MODEL=${INCLUDED_MODEL:-<default_model>}"""


def init_git_repo():
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "{{cookiecutter.repo_url.replace('http://', 'git@').replace('https://', 'git@').replace('github.com/', 'github.com:')}}",
            ]
        )
        print(
            "Added remote origin '{{cookiecutter.repo_url}}'. Please make sure this repository exists."
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize Git repository: {e}")


def add_model_variants():
    model_import_str = ""

    models = "{{ cookiecutter.models }}".split(",")
    models = [model.strip().lower() for model in models]

    for i, model in enumerate(models):
        model_class = "".join(word.capitalize() for word in model.split("_"))
        if i == 0:
            model_import_str += "if " + model_import_str_template.replace(
                "<model>", model
            ).replace("<model_class>", model_class)
        else:
            model_import_str += "\n\n        elif " + model_import_str_template.replace(
                "<model>", model
            ).replace("<model_class>", model_class)

        # create a specific .py file for each model variant
        model_file_path = Path("{{cookiecutter.__package_name}}") / f"{model}.py"
        model_file_path.touch()
        with open(model_file_path, "w") as file:
            file.write(
                model_file_str.replace("<model_class>", model_class).replace(
                    "<model>", model
                )
            )

    model_import_str += (
        '\n\n        raise ValueError(f"Unsupported model: {Config.MODEL}")'
    )

    # add conditional model imports to predictor_factory
    with fileinput.input(
        "./{{cookiecutter.__package_name}}/predictor_factory.py", inplace=True
    ) as file:
        for line in file:
            print(line, end="")
            if line.startswith("    def __new__"):
                print(f"        {model_import_str}")

    # add MODEL config to Settings
    with fileinput.input(
        "./{{cookiecutter.__package_name}}/config.py", inplace=True
    ) as file:
        for line in file:
            if line.startswith("    MODEL"):
                print(
                    model_config_str.replace("<model_list>", str(models)).replace(
                        "<default_model>", f'"{models[0]}"'
                    )
                )
            else:
                print(line, end="")

    # add default MODEL to build_container.sh
    with fileinput.input("./build_container.sh", inplace=True) as file:
        for line in file:
            if line.startswith("INCLUDED_MODEL"):
                print(model_build_arg_str.replace("<default_model>", f'"{models[0]}"'))
            else:
                print(line, end="")


if __name__ == "__main__":
    if {{cookiecutter.init_git_repo}}:
        init_git_repo()
    add_model_variants()
