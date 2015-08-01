#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Giovanni Briggs'
AUTHORS =[AUTHOR]
SITENAME = u'Destiny Project'
SITEURL = '/blog/output/'

PATH = 'content'

ARTICLE_URL = '{category}/{slug}.html'
ARTICLE_SAVE_AS = '{category}/{slug}.html'


TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('Github Repo', "https://github.com/Jalepeno112/DestinyProject"),
         )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

STATIC_PATHS=['images', 'static/css/', 'crucibleDataAnalysisJS', 'javascripts', "fullPlots"]

#don't process HTML files
#these are leftovers or Sphinx Doc pages that we don't need to try and process
READERS = {'html':None}

BS3_THEME = "https://bootswatch.com/yeti/bootstrap.min.css"

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['pelican_plugins']
PLUGINS = ['pelican_javascript', 'html_rst_directive']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True