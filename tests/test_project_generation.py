import os
import re

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
