#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'session_demo.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    # Default to port 8001 for runserver
    if len(sys.argv) == 2 and sys.argv[1] == 'runserver':
        sys.argv.append('8001')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
