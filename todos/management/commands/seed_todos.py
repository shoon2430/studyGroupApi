import random

from django.core.management.base import BaseCommand
from django_seed import Seed

from todos.models import Todo, TodoGroup


class Command(BaseCommand):

    help = "This command creates Todo"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many Todos you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")

        seeder = Seed.seeder()

        todoGroups = TodoGroup.objects.all()
        selected_todoGroup = random.choice(todoGroups)
        writer = random.choice(selected_todoGroup.members.all())

        seeder.add_entity(
            Todo,
            number,
            {
                "todoGroup_id": selected_todoGroup,
                "time": selected_todoGroup.time,
                "title": selected_todoGroup.title + " - " + str(random.randint(1, 100)),
                "progress": selected_todoGroup.progress,
                "writer": writer,
                "start": selected_todoGroup.start,
                "end": selected_todoGroup.end,
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"CREATE Todo count : {number}"))
