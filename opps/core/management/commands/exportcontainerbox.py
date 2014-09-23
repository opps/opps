from django.core.management.base import BaseCommand
from django.core import serializers

from opps.boxes.models import QuerySet
from opps.channels.models import Channel
from opps.containers.models import ContainerBox


class Command(BaseCommand):

    def handle(self, *args, **options):
        models = [Channel, ContainerBox, QuerySet]
        for m in models:
            data = serializers.serialize("json", m.objects.all())
            out = open("opps_{0}.json".format(m.__name__), "w")
            out.write(data)
            out.close()
