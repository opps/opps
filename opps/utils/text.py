# coding: utf-8

"""
Text parsing, analysing and searching utilities
"""

import re
import htmlentitydefs
from collections import OrderedDict


def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.

    @param text The HTML (or XML) source text.
    @return The plain text, as a Unicode string, if necessary.
    """

    if not text:
        return text

    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1: -1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def split_tags(tags, separator=','):
    """
    Splits string tag list using comma or another separator char, maintain
    order and removes duplicate items.

    @param tags List of tags separated by attribute separator (default: ,)
    @param separator Separator char.
    @return Ordered list of tags.
    """

    if not tags:
        return []

    tags = re.sub('\s*{0}+\s*'.format(re.escape(separator)), separator, tags)
    tags = re.sub('[\n\t\r]', '', tags)
    tags = tags.strip().split(separator)
    tags = filter(None, tags)

    return OrderedDict.fromkeys(tags).keys()  # Removes repeated items
