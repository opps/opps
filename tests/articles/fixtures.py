# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from opps.channels.models import Channel
from opps.articles.models import Post


def create_post():
    """Create generic post for tests"""
    self.user = User.objects.create(
        username='test@test.com',
        email='test@test.com',
        password=User.objects.make_random_password(),
    )
    self.channel = Channel.objects.create(
        name='test channel',
        user=self.user,
    )
    self.post = Post.objects.create(
        headline=u'a simple headline',
        short_title=u'a simple short title',
        title=u'a simple title',
        hat=u'a simple hat',
        channel=self.channel,
        user=self.user,
    )
