# coding: utf-8

from opps.articles.models import Post, Album


def count_posts(request):
    return Post.objects.count()


def count_albums(request):
    return Album.objects.count()
