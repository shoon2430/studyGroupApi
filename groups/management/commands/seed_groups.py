import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed

from users.models import User
from groups.models import Group


class Command(BaseCommand):

    """
    Group 가데이터 생성
    """

    help = "This command creates groups"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()

        category = ["Study", "Book", "Game"]
        users = User.objects.all()
        leader = random.choice(users)

        seeder.add_entity(
            Group,
            number,
            {
                "category": lambda x: category[random.randint(0, 2)],
                "title": lambda x: seeder.faker.sentence(),
                "description": lambda x: seeder.faker.text(),
                "leader": leader,
                "time": random.randint(1, 5),
            },
        )

        create_group = seeder.execute()
        create_group_pk = flatten(list(create_group.values()))

        for pk in create_group_pk:
            group = Group.objects.get(pk=pk)
            group.members.add(group.leader)

            for user in users:
                magic_number = random.randint(0, 12)
                if magic_number % 2 == 0 and user not in group.members.all():
                    group.members.add(user)
                    user.attendGroups.add(group)
                    user.save()

            for user in users:
                magic_number = random.randint(0, 12)
                if magic_number % 2 == 0 and user not in group.members.all():
                    group.attends.add(user)

        self.stdout.write(self.style.SUCCESS(f"CREATE Users count : {number}"))
