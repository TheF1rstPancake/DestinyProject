import pandas as pd 
import destinyPlatform as destiny 
import json
import os
import time
import numpy as np
import jinja2
import logging
import sys
from nvd3py import *

FULL_PLOT_HTML_DIRECTORY = os.path.join("blog","content","pages","fullPlots","characterData")
FULL_PLOT_JS_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "javascripts")
FULL_PLOT_JSON_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "datafiles")

PLOT_TEMPLATES = "plotTemplates"

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))

def _makeDirectories(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def writeGraph(graph, htmlTemplate="htmlTemplate.html", author="Giovanni Briggs", 
                date=None, category='Full Plots', tags=None, extension=".html", url=None):

    print(FULL_PLOT_HTML_DIRECTORY)

    #make sure all directories are created and ready to go
    _makeDirectories(FULL_PLOT_HTML_DIRECTORY)
    _makeDirectories(FULL_PLOT_JS_DIRECTORY)
    _makeDirectories(FULL_PLOT_JSON_DIRECTORY)


    if date is None:
        date = time.strftime("%Y-%m-%d")

    #write to javascript file
    graph.buildcontent()
    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join(htmlTemplate))
    template_values = {
        'destinyGraph': graph.__dict__,
        'date': date,
        'category': category,
        'author':author,
        'tags': tags,
        'url':url
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + extension)), 'w') as f:
        f.write(output)