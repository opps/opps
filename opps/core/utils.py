# coding: utf-8

from django.db.models import get_models, get_app


def get_app_model(appname, suffix=""):
    app_label = appname.split('.')[-1]
    models = [model for model in get_models(get_app(app_label))
              if (model.__name__.endswith(suffix) or not suffix)
              and model._meta.app_label == app_label]
    return models and models[0]


def class_load(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
