from pathlib import Path
import shutil
import subprocess

SUCCESS = "\x1b[1;32m [SUCCESS]: "
TERMINATOR = "\x1b[0m"
INFO = "\x1b[1;33m [INFO]: "


def remove_files_and_folders(*args: str):
    for path in args:
        p = Path(path)
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()


def main():
    if "{{ cookiecutter.render_html }}" == "n":
        remove_files_and_folders("app/static", "app/frontend", "app/templates")

    if "{{ cookiecutter.mail_service }}" == "Amazon SES":
        remove_files_and_folders("app/services/email/smtp.py")

    if "{{ cookiecutter.mail_service }}" == "Other SMTP":
        remove_files_and_folders("app/services/email/ses.py")

    if "{{ cookiecutter.use_heroku }}" == "n":
        remove_files_and_folders("runtime.txt", "Procfile")

    if "{{ cookiecutter.use_docker }}" != "y":
        remove_files_and_folders("Dockerfile")

    if "{{ cookiecutter.database }}" == "Beanie":
        remove_files_and_folders("app/db/models.py")

    # try to format the code
    try:
        print(INFO + "Formatting with black" + TERMINATOR)
        subprocess.run(("black", "app"), stdout=subprocess.DEVNULL)
        print(INFO + "Formatting with isort" + TERMINATOR)
        subprocess.run(("isort", "app"), stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        pass

    print(SUCCESS + "Project initialized, keep up the good work!" + TERMINATOR)
    print(
        INFO
        + "If you like the project consider dropping a star at https://github.com/Tobi-De/cookiecutter-fastapi"
        + TERMINATOR
    )


if __name__ == "__main__":
    main()
