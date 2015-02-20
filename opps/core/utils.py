# coding: utf-8

from django.db.models import get_models, get_app
from django.template import loader, TemplateDoesNotExist


def get_app_model(appname, suffix=""):
    app_label = appname.split('.')[-1]
    models = []
    for model in get_models(get_app(app_label)):
        if (model.__name__.endswith(suffix) or not suffix) and\
                model._meta.app_label == app_label:
            models.append(model)
    return models and models[0]


def class_load(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def get_template_path(path):
    try:
        template = loader.find_template(path)
        if template[1]:
            return template[1].name
        for template_loader in loader.template_source_loaders:
            try:
                source, origin = template_loader.load_template_source(path)
                return origin
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(path)
    except TemplateDoesNotExist:
        return None
