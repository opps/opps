from django.core.management.base import BaseCommand, CommandError
from opps.channels.models import Channel
from opps.containers.models import ContainerBox
from opps.articles.models import Post


class Command(BaseCommand):

    def handle(self, *args, **options):
        models = [Channel, Post, ContainerBox]
        for m in models:
            [p.save() for p in m.objects.all()]
