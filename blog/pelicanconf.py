#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Giovanni Briggs'
AUTHORS =[AUTHOR]
SITENAME = u'Destiny Project'
SITEURL = '/DestinyProject/blog/output/'

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
         ('Linkedin', "https://www.linkedin.com/in/giovannibriggs"),
         ('Bungie','http://www.bungie.net'),
         ('BungieNetPlatform', 'https://www.bungie.net/en/Clan/Forum/39966/0/1/0')
         )

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

STATIC_PATHS=['images', 'static/css/', 'crucibleDataAnalysisJS', 'javascripts', "fullPlots"]
FAVICON = 'images/favicon.png'

#don't process HTML files
#these are leftovers or Sphinx Doc pages that we don't need to try and process
READERS = {'html':None}

BS3_THEME = "https://bootswatch.com/yeti/bootstrap.min.css"

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['pelican_plugins']
PLUGINS = ['pelican_javascript', 'html_rst_directive']

#BOOTSTRAP_FLUID = True
BOOTSTRAP_NAVBAR_INVERSE = True
BOOTSTRAP_THEME = "yeti"

#Add extra javascript and css files
PROJECT_NAME = 'DestinyProject'
EXTRA_JAVASCRIPT_FILES = [
                        "https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.2/d3.min.js",
                        "https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.1/nv.d3.js",
                        'https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js'
                        ]
EXTRA_CSS_FILES = [
                   '{0}static/css/plots.css'.format(SITEURL),                            
                   'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.1/nv.d3.css',
                    'https://cdnjs.cloudflare.com/ajax/libs/nvd3/1.8.1/nv.d3.css',

                ]
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True