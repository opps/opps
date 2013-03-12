# -*- coding: utf-8 -*-


def generate_long_slug(channel, slug, domain):
    u""" Generate long slug """
    return "{0}{1}".format("{0}/".format(channel) if channel else "", slug) \
           .replace("{0}/".format(domain), '')
