import os
import re
import tomllib

import pytest
from binaryornot.check import is_binary

PATTERN = r"{{(\s?cookiecutter)[.](.*?)}}"
RE_OBJ = re.compile(PATTERN)

SUPPORTED_COMBINATIONS = (
    {"use_docker": "y"},
    {"use_docker": "n"},
    {"use_heroku": "y"},
    {"use_heroku": "n"},
    {"use_sentry": "y"},
    {"use_sentry": "n"},
    {"render_html": "y"},
    {"render_html": "n"},
    {"license": "MIT"},
    {"license": "Apache-2.0"},
    {"license": "Proprietary"},
    {"mail_service": "Amazon SES"},
    {"mail_service": "Other SMTP"},
    {"database": "Tortoise"},
    {"database": "Beanie"},
)


@pytest.fixture
def context():
    return {
        "project_name": "My Test Project",
        "project_slug": "my_test_project",
        "project_description": "A short description of the project.",
        "author": "Test Author <test@author.com>",
    }


def _fixture_id(ctx):
    """Helper to get a user-friendly test name from the parametrized context."""
    return "-".join(f"{key}:{value}" for key, value in ctx.items())


def check_paths(paths):
    """Method to check all paths have correct substitutions."""
    # Assert that no match is found in any of the files
    for path in paths:
        if is_binary(path):
            continue

        for line in open(path):
            match = RE_OBJ.search(line)
            assert match is None, f"cookiecutter variable not replaced in {path}"


def build_files_list(root_dir):
    """Build a list containing absolute paths to the generated files."""
    return [
        os.path.join(dirpath, file_path)
        for dirpath, subdirs, files in os.walk(root_dir)
        for file_path in files
    ]


@pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
def test_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""

    result = cookies.bake(extra_context={**context, **context_override})
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project_path.name == context["project_slug"]
    assert result.project_path.is_dir()

    paths = build_files_list(result.project_path)
    assert paths
    check_paths(paths)


def test_justfile_is_generated(cookies, context):
    """Test that justfile is generated in the project."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    
    justfile_path = result.project_path / "justfile"
    assert justfile_path.exists(), "justfile should be generated"
    
    # Verify it contains expected commands with uv
    content = justfile_path.read_text()
    assert "bootstrap" in content
    assert "setup" in content
    assert "update" in content
    assert "server" in content
    assert "test" in content
    assert "console" in content
    
    # Verify it uses uv instead of pip/python directly
    assert "uv sync" in content
    assert "uv run" in content
    assert "pip install" not in content
    
    # Verify it uses grouping
    assert "[group(" in content
    assert "[group('setup')]" in content
    assert "[group('dev')]" in content
    assert "[group('utils')]" in content


def test_justfile_tortoise_commands(cookies, context):
    """Test that justfile contains Tortoise-specific commands when database is Tortoise."""
    result = cookies.bake(extra_context={**context, "database": "Tortoise"})
    assert result.exit_code == 0
    
    justfile_path = result.project_path / "justfile"
    content = justfile_path.read_text()
    
    assert "migrate" in content
    assert "makemigrations" in content
    assert "aerich" in content
    
    # Verify database commands use uv run
    assert "uv run aerich" in content
    assert "[group('database')]" in content


def test_justfile_beanie_no_migrations(cookies, context):
    """Test that justfile doesn't contain migration commands when database is Beanie."""
    result = cookies.bake(extra_context={**context, "database": "Beanie"})
    assert result.exit_code == 0
    
    justfile_path = result.project_path / "justfile"
    content = justfile_path.read_text()
    
    # Beanie projects shouldn't have these commands
    assert "aerich" not in content
    assert "makemigrations" not in content


def test_pyproject_toml_is_valid_toml(cookies, context):
    """Test that the generated pyproject.toml is valid TOML and can be parsed."""
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    
    pyproject_path = result.project_path / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml should be generated"
    
    # Verify it can be parsed as valid TOML
    with open(pyproject_path, 'rb') as f:
        data = tomllib.load(f)
    
    # Verify basic structure
    assert "project" in data
    assert "name" in data["project"]
    assert "version" in data["project"]
    assert "authors" in data["project"]
    assert "dependencies" in data["project"]
    
    # Verify authors and dependencies are lists
    assert isinstance(data["project"]["authors"], list)
    assert isinstance(data["project"]["dependencies"], list)
    assert len(data["project"]["authors"]) > 0
    assert len(data["project"]["dependencies"]) > 0

