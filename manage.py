#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    
    # --- THIS IS THE LINE YOU MUST CHECK ---
    #
    # The error "No module named 'project_root'" means your
    # project folder (the one containing settings.py) is
    # NOT named 'project_root'.
    #
    # Change 'project_root.settings' to match your project's
    # real folder name.
    #
    # EXAMPLE: If your folder is named 'myproject', change
    # this line to:
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    #
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()