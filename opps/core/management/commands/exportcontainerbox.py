from django.core.management.base import BaseCommand, CommandError

from django.core import serializers
from opps.channels.models import Channel
from opps.containers.models import ContainerBox
from opps.boxes.models import QuerySet

class Command(BaseCommand):
    def handle(self, *args, **options):
        models = [Channels, ContainerBox, QuerySet]
        for m in models:
            data = serializers.serialize("json", m.objects.all())
            out = open("opps_{}.json".format(m.__name__), "w")
            out.write(data)
            out.close()
