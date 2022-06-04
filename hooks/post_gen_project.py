from pathlib import Path
import shutil


def remove_render_html_dirs():
    dirs = ["static", "frontend", "templates"]
    for dir in dirs:
        shutil.rmtree(Path().joinpath(f"app/{dir}"))


def main():
    if "{{ cookiecutter.render_html }}" == "n":
        remove_render_html_dirs()


if __name__ == "__main__":
    main()
