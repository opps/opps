# coding: utf-8

from django.db.models import get_models


def get_app_model(appname, suffix=None):
    app_label = appname.split('.')[-1]
    models = [model for model in get_models()
              if (model.__name__.endswith(suffix) or not suffix)
              and model._meta.app_label == app_label]
    return models and models[0]
