# coding: utf-8

import celery
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()


@celery.task
def notify(message, type='text',
           action='message', container=None, user=None):
    if not user:
        user = User.objects.all()[0]
    notification = Notification.objects.create(
        message=message,
        type=type,
        action=action,
        container=container,
        user=user
    )
    return notification
