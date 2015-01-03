# -*- coding: utf-8 -*-
def field_template_read(obj):
    """Use replace because the django template can't read variable with "-"
    """
    fields = {}
    for o in obj:
        fields[o.replace("-", "_")] = obj[o]

    return fields
