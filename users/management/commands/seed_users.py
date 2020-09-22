from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


# python manage.py hoon --times 50


class Command(BaseCommand):

    """
    User 가데이터 생성
    """

    help = "This command creates users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        # password는 1234
        seeder.add_entity(
            User,
            number,
            {
                "password": "pbkdf2_sha256$180000$fy0OzCwZz5Wl$RfHqhEHoHAK5YBZpJb2tEmEhPmghdMowoRtA0VtD1AQ=",
                "is_staff": False,
                "is_superuser": False,
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE Users count : {number}"))
