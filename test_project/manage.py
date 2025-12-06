"""
Backward compatibility wrapper for manage.py.

This file is kept for backward compatibility. All CLI logic has been moved to test_project/__main__.py.
You can now run commands using either:
  - python manage.py <command>  (old way, still works)
  - python -m test_project <command>     (new way, recommended)
"""
from test_project.__main__ import cli

if __name__ == "__main__":
    cli()
