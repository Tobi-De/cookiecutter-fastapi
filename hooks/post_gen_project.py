from pathlib import Path
import shutil

SUCCESS = "\x1b[1;32m [SUCCESS]: "
TERMINATOR = "\x1b[0m"
INFO = "\x1b[1;33m [INFO]: "


def remove_render_html_dirs():
    dirs = ("static", "frontend", "templates")
    for dir in dirs:
        shutil.rmtree(Path().joinpath(f"app/{dir}"))


def remove_heroku_files():
    files = ("runtime.txt", "Procfile")
    for file in files:
        Path().joinpath(f"app/{file}").unlink()


def remove_docker_files():
    files = ("Dockerfile",)
    for file in files:
        Path().joinpath(f"app/{file}").unlink()


def main():
    if "{{ cookiecutter.render_html }}" == "n":
        remove_render_html_dirs()
    if "{{ cookiecutter.mail_service }}" == "Amazon SES":
        Path().joinpath("app/services/email/smtp.py").unlink()
    if "{{ cookiecutter.mail_service }}" == "Other SMTP":
        Path().joinpath("app/services/email/ses.py").unlink()
    if "{{ cookiecutter.use_heroku }}" == "n":
        remove_heroku_files()
    # if "{{ cookiecutter.use_docker }}" != "y":
    #     remove_heroku_files()

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)
    print(
        INFO
        + "If you like the project consider dropping a star at https://github.com/Tobi-De/cookiecutter-fastapi"
        + TERMINATOR
    )


if __name__ == "__main__":
    main()
