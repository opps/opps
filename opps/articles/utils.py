#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata


def normalize_tags(tags):
    """ Normalise (normalize) unicode data in Python to remove umlauts,
    accents etc. """

    if not tags:
        return []
    try:
        return [
            unicodedata.normalize(
                'NFKD', tag.lower().strip()
            ).encode('ASCII', 'ignore')
            for tag in tags.split(',')
        ]
    except:
        return [tags]
