#!/usr/bin/env python3
import sys
from pathlib import Path
import fileinput


MODEL_FILE_TEMPLATE = """from {package_name}.config import Config
# import model libraries

class {model_class}:

    # model_name
    # if using HF_MODEL_INFO=true, make sure that the model_name is equal to
    # the model's base name on Huggingface
    model_name = ""

    def __init__(self):
        # instantiate model here
        self.model = None

    def predict(self):
        # add inference code here
        raise NotImplementedError(
            "The class {model_class} must implement the 'predict' method"
        )
"""


MODEL_CONFIG_LINE_TEMPLATE = '    MODEL: Literal{model_list} = "{default_model}"'
MODEL_BUILD_ARG_LINE_TEMPLATE = 'MODEL=${{MODEL:-"{default_model}"}}'


def to_class_name(s: str) -> str:
    # snake_case -> PascalCase
    return "".join(part.capitalize() for part in s.split("_"))


def git_remote_from_repo_url(repo_url: str) -> str:
    # replicate your string replace chain from the template
    if not repo_url:
        return ""
    transformed = (
        repo_url.replace("http://", "git@")
        .replace("https://", "git@")
        .replace("github.com/", "github.com:")
    )
    return f"{transformed}.git"

def add_model_variants(models: str, package_name: str):
    """
    - create <model>.py for each model
    - generate/append pytest fixtures/tests
    - patch config.py MODEL=...
    - patch build_container.sh, Containerfile
    - patch workflow matrix
    """
    models = [m.strip().lower() for m in models.split(",") if m.strip()]
    if not models:
        print("No models provided, skipping model variant setup.")
        return

    package_path = Path(package_name)

    # 1. Create one .py file per model
    for model in models:
        model_class = to_class_name(model)

        model_file_path = package_path / f"{model}.py"
        model_file_path.write_text(
            MODEL_FILE_TEMPLATE.format(
                package_name=package_name,
                model_class=model_class,
            )
        )

    # 2. tests/conftest.py and tests/test_function.py
    tests_dir = Path("tests")
    tests_dir.mkdir(exist_ok=True)
    conftest_path = tests_dir / "conftest.py"
    test_file_path = tests_dir / "test_function.py"

    # We'll (re)write these files from scratch to keep it idempotent
    imports_block = []
    fixtures_block = []
    tests_block = []

    for model in models:
        cls = to_class_name(model)
        imports_block.append(f"from {package_name}.{model} import {cls}\n")
        fixtures_block.append(
            "@pytest.fixture(scope=\"session\")\n"
            f"def {model}():\n"
            f"    yield {cls}()\n\n"
        )
        tests_block.append(
            f"def test_cybersec_classification_{model}({model}: {cls}):\n"
            f'    assert False, "Add a functional test for your {cls} model"\n'
        )

    conftest_path.write_text(
        "import pytest\n\n" + "".join(imports_block) + "\n" + "".join(fixtures_block)
    )
    test_file_path.write_text(
        "".join(imports_block) + "\n" + "\n".join(tests_block) + "\n"
    )

    # 3. Patch config.py MODEL line
    config_path = package_path / "config.py"
    if config_path.exists():
        model_list_literal = "[" + ", ".join(f'"{m}"' for m in models) + "]"
        default_model = models[0]

        with fileinput.input(config_path, inplace=True) as f:
            for line in f:
                stripped = line.lstrip()
                if stripped.startswith("MODEL"):
                    print(
                        MODEL_CONFIG_LINE_TEMPLATE.format(
                        model_list=model_list_literal,
                        default_model=default_model,
                      )
                    )
                else:
                    print(line, end="")
    else:
        print(f"WARNING: {config_path} not found; skipping MODEL patch")

    # 4. Patch build_container.sh MODEL default
    bc_path = Path("build_container.sh")
    if bc_path.exists():
        default_model = models[0]
        new_lines = []
        with bc_path.open() as f:
            for line in f:
                if line.startswith("MODEL"):
                    new_lines.append(
                        MODEL_BUILD_ARG_LINE_TEMPLATE.format(
                            default_model=default_model
                        )
                        + "\n"
                    )
                else:
                    new_lines.append(line)
        bc_path.write_text("".join(new_lines))
    else:
        print("WARNING: build_container.sh not found; skipping build script patch")

    # 5. Patch Containerfile ARG MODEL
    cont_path = Path("Containerfile")
    if cont_path.exists():
        default_model = models[0]
        new_lines = []
        with cont_path.open() as f:
            for line in f:
                if line.startswith("ARG MODEL"):
                    new_lines.append(f'ARG MODEL="{default_model}"\n')
                else:
                    new_lines.append(line)
        cont_path.write_text("".join(new_lines))
    else:
        print("WARNING: Containerfile not found; skipping Containerfile patch")

    # 6. Patch GitHub workflow placeholders
    wf_path = Path(".github/workflows/build_and_merge.yml")
    if wf_path.exists():
        default_model = models[0]
        text = wf_path.read_text()
        text = text.replace("<models>", "[" + ", ".join(models) + "]")
        text = text.replace("<default_model>", default_model)
        wf_path.write_text(text)
    else:
        print("WARNING: .github/workflows/build_and_merge.yml not found; skipping workflow patch")


def main() -> int:
    # Arguments passed from copier.yml _tasks:
    #   argv[1] = package_name
    #   argv[2] = models
    #   argv[3] = repo_url
    if len(sys.argv) != 4:
        print(
            "Usage: post_create_hook.py <package_name> <models> <repo_url>"
        )
        return 1

    package_name = sys.argv[1]
    models = sys.argv[2].replace("(model_a) ", "")
    repo_url = sys.argv[3]

    print("[post_create_hook] running with:")
    print(f"  package_name={package_name}")
    print(f"  models={models}")
    print(f"  repo_url={repo_url}")

    add_model_variants(models, package_name)

    print("[post_create_hook] done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
