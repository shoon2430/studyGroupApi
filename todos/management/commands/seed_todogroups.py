import random
import datetime
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from todos.models import Subject, TodoGroup
from groups.models import Group


class Command(BaseCommand):

    help = "This command creates TodoGroups"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        progress_list = ["CREATE", "DOING", "COMPLETED"]

        subjects = Subject.objects.all()
        selected_subject = random.choice(subjects)

        group = selected_subject.group_id
        group_memebers = group.members

        seeder.add_entity(
            TodoGroup,
            number,
            {
                "subject_id": selected_subject,
                "time": selected_subject.time,
                "title": lambda x: seeder.faker.sentence(),
                "progress": progress_list[random.randint(0, 2)],
                "leader": selected_subject.writer,
                "start": datetime.datetime.now(),
                "end": datetime.datetime.now() + datetime.timedelta(days=1),
            },
        )

        create_todoGroups = seeder.execute()
        create_todoGroups_pk = flatten(list(create_todoGroups.values()))
        for pk in create_todoGroups_pk:
            todoGroup = TodoGroup.objects.get(pk=pk)

            for member in group_memebers.all():
                magic_number = random.randint(0, 12)
                if magic_number % 2 == 0:
                    todoGroup.members.add(member)

        self.stdout.write(self.style.SUCCESS(f"CREATE TodoGroup count : {number}"))
