# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


trans_app_label = _('Core')


class OppsCoreConf(AppConf):
    DEFAULT_URLS = ('127.0.0.1', 'localhost',)
    SHORT = 'googl'
    SHORT_URL = 'googl.short.GooglUrlShort'
    CHANNEL_CONF = {}
    CHANNEL_LAYOUT = (('default', _('Default')),)
    VIEWS_LIMIT = None
    PAGINATE_BY = 10
    PAGINATE_SUFFIX = u''
    PAGINATE_NOT_APP = []
    CHECK_MOBILE = False
    DOMAIN_MOBILE = u''
    PROTOCOL_MOBILE = u'http'
    ADMIN_RULES = {}
    RELATED_POSTS_PLACEHOLDER = "---related---"
    CACHE_PREFIX = 'opps'
    CACHE_EXPIRE = 300
    CACHE_EXPIRE_LIST = 300
    CACHE_EXPIRE_DETAIL = 300
    RSS_LINK_TEMPLATE = '<a href="{}" class="ir ico ico-rss">RSS</a>'
    LIST_MODELS = ('Post',)
    RECOMMENDATION_RANGE_DAYS = 180
    SMART_SLUG_ENABLED = True
    MENU = True
    MENU_ONLY_WITH_PUBLISHED_CONTAINERS = False
    MIRROR_CHANNEL = False
    CONTAINERS_BLACKLIST = ['Entry']
    CONTAINERS_SITE_ID = None

    # default settings for tinymce
    EDITOR = {
        'editor': 'tinymce',
        'height': 400,
        'js': ('/static/tinymce/tinymce.min.js',),
        "theme": "modern",
        "plugins": [
            """advlist autolink lists link image charmap print preview hr
        anchor pagebreak """,
            "searchreplace wordcount visualblocks visualchars code fullscreen",
            """insertdatetime media nonbreaking save table contextmenu
        directionality""",
            "template paste textcolor opps"
        ],
        "toolbar1": """insertfile undo redo | styleselect | bold italic |
                alignleft aligncenter alignright alignjustify |
                bullist numlist outdent indent | link image media |
                print preview  | forecolor backcolor | opps""",
        "image_advtab": True,
        "templates": [
            {"title": 'Related', "content": RELATED_POSTS_PLACEHOLDER},
        ],
        "file_browser_callback": 'CustomFileBrowser',
    }

    class Meta:
        prefix = 'opps'


class GrapelliConf(AppConf):

    ADMIN_TITLE = "Opps CMS Admin"
    INDEX_DASHBOARD = 'opps.contrib.admin.dashboard.CustomIndexDashboard'

    class Meta:
        prefix = 'GRAPPELLI'


class AdminConf(AppConf):

    SHORTCUTS = [
        {
            'shortcuts': [
                {
                    'url_name': 'admin:articles_post_add',
                    'title': '+ Notícia',
                    'class': 'file3',
                    'help': 'Clique para adicionar uma nova notícia'
                },
                {
                    'url_name': 'admin:articles_post_changelist',
                    'title': 'Notícias',
                    'count': 'opps.contrib.admin.shortcuts.count_posts',
                    'class': 'file2',
                    'help': 'Clique para visualisar todas as notícias'
                },
                {
                    'url_name': 'admin:images_image_add',
                    'title': '+ Imagem',
                    'class': 'picture',
                    'help': 'Clique para adicionar uma nova imagem'
                },
                {
                    'url_name': 'admin:articles_album_changelist',
                    'title': 'Álbum',
                    'count': 'opps.contrib.admin.shortcuts.count_albums',
                    'class': 'camera',
                    'help': 'Clique para visualisar todos os álbuns'
                },
                {
                    'url': '/',
                    'open_new_window': True,
                    'help': 'Clique para visualizar a home page do site'
                },
            ]
        }
    ]

    SHORTCUTS_SETTINGS = {
        'hide_app_list': True,
        'open_new_window': False,
    }

    SHORTCUTS_CLASS_MAPPINGS_EXTRA = [
        ('blogs_blogpost', 'blog')
    ]

    class Meta:
        prefix = 'ADMIN'


class StaticSiteMapsConf(AppConf):
    ROOT_SITEMAP = 'opps.sitemaps.feed.sitemaps'

    class Meta:
        prefix = 'staticsitemaps'


class HaystackConf(AppConf):
    CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        }
    }

    class Meta:
        prefix = 'haystack'


class ThumborConf(AppConf):
    SERVER = 'http://localhost:8888'
    MEDIA_URL = 'http://localhost:8000/media'
    SECURITY_KEY = ''
    ARGUMENTS = {}
    ENABLED = False

    class Meta:
        prefix = 'thumbor'


class DjangoConf(AppConf):
    CACHES = {'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}}
