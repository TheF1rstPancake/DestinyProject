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
import plotutils
import scipy.stats

plotutils.FULL_PLOT_HTML_DIRECTORY = os.path.join("blog","content","pages","fullPlots","combatRating")
plotutils.FULL_PLOT_JS_DIRECTORY = os.path.join(plotutils.FULL_PLOT_HTML_DIRECTORY, "javascripts")
plotutils.FULL_PLOT_JSON_DIRECTORY = os.path.join(plotutils.FULL_PLOT_HTML_DIRECTORY, "datafiles")

PLOT_TEMPLATES = "plotTemplates"

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))

def combatRatingDist(data):
    data = pd.DataFrame(data[(data['combatRating'] > 0)])
    CR = data['combatRating']

    #build a histogram of 20 bins from (0,300)
    #The range is set because of a first glance look at the data
    num_bins = 12
    hist = scipy.stats.histogram(CR,numbins=num_bins, defaultlimits=(0,240))

    #add the extra points to the last bin.
    #this will cause there to be a slight increase in the last bin in comparison to the bin before it.
    hist[0][-1] = hist[0][-1]+hist[3]

    #some of the bins barely contain any data.  Add these all to one extended bin

    bins = [c*hist[2] for c in xrange(0,num_bins)]

    #the first bin should be (0, bin_edge) because literal 0 is not included in this data.
    bin_strings = ["(0,{0:.2f})".format(bins[1])]
    bin_strings.extend(["[{0:.2f}, {1:.2f})".format(bins[b], bins[b+1]) for b in xrange(1,num_bins-1)])
    bin_strings.append("[{0:.2f}, Inf)".format(bins[-1]))

    graph = multiBarChart(
                name="combatRatingDist",
                key= 'combatRatingDist',
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Combat Ratings in Control",
                subtitle="A look at the distribution of combat ratings for players in Control",
                resize=True,
                plotText="Shows the distribution of combat ratings in Control.  " + 
                            "Each bar represents a bin extending from it's starting x position to the next in the following fashion [x, x1). "
                )   
    graph.width = None

    graph.add_serie(x=bin_strings, y = hist[0]/len(CR), name='Distribution')
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url='pages/fullPlots/combatRating/{0}'.format(graph.name+'.html'))

if __name__ == "__main__":
    data = pd.read_csv("datafiles/data.csv", index_col=0)

    combatRatingDist(data)
