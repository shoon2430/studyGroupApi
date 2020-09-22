import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from todos.models import Subject
from groups.models import Group


class Command(BaseCommand):

    help = "This command creates Subjects"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")

        seeder = Seed.seeder()
        groups = Group.objects.all()

        selected_group = random.choice(groups)
        group_memebers = selected_group.members

        seeder.add_entity(
            Subject,
            number,
            {
                "group_id": selected_group,
                "time": selected_group.time,
                "title": lambda x: seeder.faker.sentence(),
                "description": lambda x: seeder.faker.text(),
                "writer": selected_group.leader,
            },
        )

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE Subejects count : {number}"))
