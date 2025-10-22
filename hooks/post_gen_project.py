import fileinput
import subprocess
from pathlib import Path


model_file_str = """from {{cookiecutter.__module_name}}.config import Config
# import model libraries

class <model_class>:

    # model_name
    # if using HF_MODEL_INFO=true, make sure that the model_name is equal to
    # the models base name on Huggingface
    model_name = ""

    def __init__(self):
        # instantiate model here
        self.model = None

    def predict(self):
        # add inference code here
        raise NotImplementedError("The class <model_class> must implement the 'predict' method")
"""

functional_test_str = """
"""

model_config_str = """    MODEL: Literal<model_list> = <default_model>"""
model_build_arg_str = """MODEL=${MODEL:-<default_model>}"""


def init_git_repo():
    try:
        subprocess.run(["git", "init", "-b", "main"], check=True)
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "{{cookiecutter.repo_url.replace('http://', 'git@').replace('https://', 'git@').replace('github.com/', 'github.com:')}}.git",
            ]
        )
        print(
            "Added remote origin '{{cookiecutter.repo_url}}'. Please make sure this repository exists."
        )
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize Git repository: {e}")


def add_model_variants():
    models = "{{ cookiecutter.models }}".split(",")
    models = [model.strip().lower() for model in models]
    models_str = "[" + ", ".join(f'"{m}"' for m in models) + "]"

    for model in models:
        model_class = "".join(word.capitalize() for word in model.split("_"))

        # create a specific .py file for each model variant
        model_file_path = Path("{{cookiecutter.__package_name}}") / f"{model}.py"
        model_file_path.touch()
        with open(model_file_path, "w") as file:
            file.write(
                model_file_str.replace("<model_class>", model_class).replace(
                    "<model>", model
                )
            )

    # add a functional test for each model to tests/test_function.py
    tests_dir = Path("tests")
    conftest_path = tests_dir / "conftest.py"
    test_file_path = tests_dir / "test_function.py"

    with open(conftest_path, "a") as cf, open(test_file_path, "a") as tf:
        cf.write("import pytest\n")
        tf.write("\n")

        for model in models:
            model_class = "".join(word.capitalize() for word in model.split("_"))

            # imports
            import_line = f"from {{cookiecutter.__package_name}}.{model} import {model_class}\n"
            cf.write(import_line)
            tf.write(import_line)

        cf.write("\n")
        tf.write("\n")

        for model in models:
            model_class = "".join(word.capitalize() for word in model.split("_"))
            fixture_name = model

            # fixture in conftest.py
            cf.write(
                f'@pytest.fixture(scope="session")\n'
                f"def {fixture_name}():\n"
                f"    yield {model_class}()\n\n"
            )

            # test in test_function.py
            tf.write(
                f"def test_cybersec_classification_{model}({fixture_name}: {model_class}):\n"
                f'    assert False, "Add a functional test for your {model_class} model"\n'
            )

    # add MODEL config to config.py
    with fileinput.input(
        "./{{cookiecutter.__package_name}}/config.py", inplace=True
    ) as file:
        for line in file:
            if line.startswith("    MODEL"):
                print(
                    model_config_str.replace("<model_list>", models_str).replace(
                        "<default_model>", f'"{models[0]}"'
                    )
                )
            else:
                print(line, end="")

    # add default MODEL to build_container.sh
    with fileinput.input("./build_container.sh", inplace=True) as file:
        for line in file:
            if line.startswith("MODEL"):
                print(model_build_arg_str.replace("<default_model>", f'"{models[0]}"'))
            else:
                print(line, end="")

    # add default MODEL to Containerfile
    with fileinput.input("./Containerfile", inplace=True) as file:
        for line in file:
            if line.startswith("ARG MODEL"):
                print(line.replace("<default_model>", f"{models[0]}"))
            else:
                print(line, end="")

    # add models to github build workflow
    with fileinput.input(".github/workflows/build_and_merge.yml", inplace=True) as file:
        for line in file:
            if "<models>" in line:
                print(line.replace("<models>", "[" + ", ".join(models) + "]"))
            elif "<default_model>" in line:
                print(line.replace("<default_model>", models[0]))
            else:
                print(line, end="")


if __name__ == "__main__":
    if {{cookiecutter.init_git_repo}}:
        init_git_repo()
    add_model_variants()
