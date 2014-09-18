# coding: utf-8
import csv

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


def export_to_csv(modeladmin, request, queryset):
    """Exporting queryset results and filter into CSV"""
    # limit only staff and super_user accounts
    if request.user.is_staff or request.user.is_superuser:
        if queryset.count() > 0:
            # generate response and filename
            response = HttpResponse(mimetype="text/csv")
            today = timezone.now().strftime("%Y-%M-%d_%H:%M:%S")
            filename = "{0}-{1}.csv".format(queryset.model, today)
            response["Content-Disposition"] = ('attachment; filename="%s"' %
                                               filename)
            writer = csv.writer(response)

            # Get column name
            columns = [field.name for field in queryset[0]._meta.fields]
            writer.writerow(columns)

            # Write data
            for obj in queryset:
                fields = map(lambda x: _generate_value(obj, x), columns)
                writer.writerow(fields)

            return response

export_to_csv.short_description = _(u"Export results in CSV")


def _generate_value(obj, column):
    """Get fields value and convert to ASCIC for string type"""
    row = getattr(obj, column)
    if isinstance(row, basestring):
        row = row.encode('ascii', 'ignore')
    return row
