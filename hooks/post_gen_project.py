import subprocess


def init_git_repo():
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "remote", "add", "origin", "{{cookiecutter.repo_url}}"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize Git repository: {e}")


if __name__ == "__main__":
    if {{cookiecutter.init_git_repo}}:
        init_git_repo()
