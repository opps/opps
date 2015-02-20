
from xml.parsers import expat
from HTMLParser import HTMLParser
from django import template

register = template.Library()
parser = HTMLParser()


def unescape(s):
    want_unicode = False
    if isinstance(s, unicode):
        s = s.encode("utf-8")
        want_unicode = True

    # the rest of this assumes that `s` is UTF-8
    list = []

    # create and initialize a parser object
    p = expat.ParserCreate("utf-8")
    p.buffer_text = True
    p.returns_unicode = want_unicode
    p.CharacterDataHandler = list.append

    # parse the data wrapped in a dummy element
    # (needed so the "document" is well-formed)
    p.Parse("<e>", 0)
    p.Parse(s, 0)
    p.Parse("</e>", 1)

    # join the extracted strings and return
    es = ""
    if want_unicode:
        es = u""
    return es.join(list)


@register.simple_tag
def htmlentitydecode(s):
    try:
        unescaped = unescape(parser.unescape(s))
        return unescaped
    except:
        unescaped = parser.unescape(s)
        return unescaped.encode('utf-8')

register.filter('htmlentitydecode', htmlentitydecode)
