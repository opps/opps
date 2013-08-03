from django.contrib import admin

# from opps.core.admin import PublishableAdmin
# from opps.core.admin import apply_opps_rules

from .models import File


admin.site.register(File)