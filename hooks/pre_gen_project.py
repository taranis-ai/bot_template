import sys

models = "{{ cookiecutter.models }}"
try:
    models.split(",")
except AttributeError:
    print("Please give a comma-separated list of models!")
    sys.exit(1)
except ValueError as e:
    print(e)
    sys.exit(1)
