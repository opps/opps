# coding: utf-8
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.db.models import Max, Count
from django.utils import timezone
from django.contrib.auth import get_user_model

from opps.channels.models import Channel
from opps.containers.models import Container

User = get_user_model()


class ChannelListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Channel')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'channel'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """

        qs = model_admin.queryset(request)
        qs = qs.order_by(
            'channel_long_slug'
        ).distinct().values('channel_long_slug')

        if qs:
            channels = set([(item['channel_long_slug'] or 'nochannel',
                             item['channel_long_slug'] or _(u'No channel'))
                           for item in qs])

            long_slug_list = sorted([i[0] for i in channels])
            items = []

            for channel in channels:
                items.append(channel)
                _value = channel[0]
                if self._get_descendant_count(_value, long_slug_list) > 0:
                    value = "{0}/*".format(_value)
                    human_readable = "{0}/*".format(_value)
                    items.append((value, human_readable))

            return sorted(items)

    def _get_descendant_count(self, item, channel_list):
        """
        Search item occurrences on channel_list
        """
        children = []
        item_set = set(item.split('/'))
        for channel in channel_list:
            splt = set(channel.split('/'))
            if item != channel and item_set.issubset(splt):
                children.append(channel)
        return len(children)

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        value = self.value()
        if value == "nochannel":
            queryset = queryset.filter(channel_long_slug__isnull=True)
        elif value and "*" in value:
            site = get_current_site(request)
            long_slug = value.replace('/*', '')
            channel = Channel.objects.filter(site=site, long_slug=long_slug)[0]
            child_channels = channel.get_descendants(include_self=True)
            queryset = queryset.filter(channel__in=child_channels)
        elif value:
            queryset = queryset.filter(channel_long_slug=value)

        return queryset


class ChildClassListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Child class')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'child_class'

    def lookups(self, request, model_admin):
        site = get_current_site(request)
        child_classes = [
            (i['child_class'], _(i['child_class'])) for i in
            Container.objects.values('child_class').filter(
                published=True,
                date_available__lte=timezone.now(),
                site=site).annotate(child=Count('child_class'),
                                    date=Max('date_available')
                                    ).order_by('-date')]
        return child_classes

    def queryset(self, request, queryset):
        child_class = self.value()
        if child_class:
            queryset = queryset.filter(child_class=child_class)
        return queryset


class HasQuerySet(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'Has queryset')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'hasqueryset'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('no', _(u'No')),
            ('yes', _(u'Yes'))
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "no":
            queryset = queryset.filter(queryset__isnull=True)
        elif self.value() == 'yes':
            queryset = queryset.filter(queryset__isnull=False)

        return queryset


class UserListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _(u'User')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = u'user'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # filter only users with images
        qs = User.objects.filter(image__isnull=False).distinct()
        if qs:
            return set([(item.username,
                         u"{0} ({1})".format(item.get_full_name(), item.email))
                       for item in qs])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == u"nouser":
            queryset = queryset.filter(user__isnull=True)
        elif self.value():
            queryset = queryset.filter(user__username=self.value())

        return queryset
