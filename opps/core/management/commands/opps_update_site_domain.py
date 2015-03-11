from django.contrib.sites.models import Site

from django.core.management.base import BaseCommand
from opps.channels.models import Channel
from opps.containers.models import Container


class Command(BaseCommand):
    args = "<site_id> <domain>"
    help = "Updates site id domain and then updates channels and containers."

    def handle(self, *args, **options):
        if len(args) < 2:
            print "Usage: opps_update_site_domain %s" % self.args
            return

        pk, domain = args[:2]
        s = Site.objects.get(pk=pk)
        s.domain = domain
        s.save(update_fields=['domain'])
        print "Site updated."
        print Channel.objects.filter(site_id=pk).update(site_domain=domain),
        print "Channels updated."
        print Container.objects.filter(site_id=pk).update(site_domain=domain),
        print "Containers updated."
