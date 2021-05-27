#!/usr/bin/env python
import os
import sys

from django.conf import settings


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "arttherapy.settings.settings")
    # This is to provide debugability into the docker container on port 3000.
    # Launch.json has settings to allow the debug to attach to this endpoint.
    if settings.DEBUG:
        if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
            import ptvsd

            ptvsd.enable_attach(address=('0.0.0.0', 3000))
            print('Attached!')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
