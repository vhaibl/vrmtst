import sys

from django.core.management.commands.makemigrations import \
    Command as BaseCommand


class Command(BaseCommand):
    def handle(self, *app_labels, **options):
        if options["name"] is None:
            print(  # noqa
                "\033[91m",
                "Migrations must have a name: -n/--name is required.",
                "\033[0m",
                file=sys.stderr,
            )
            sys.exit(1)
        super().handle(*app_labels, **options)
