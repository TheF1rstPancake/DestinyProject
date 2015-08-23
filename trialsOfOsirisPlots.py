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
import combatRating_plots

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))

def classPairings(data):
    data = data[data[['hunters','titans','warlocks']].sum(1) == 3]

    group = data.groupby(['hunters','titans','warlocks'])
    f = pd.DataFrame({s:{"Len":len(g)} for s,g in group}).T

    x_ticks = [(str(val[0]) + " Hunters, " + str(val[1]) + " Titans, " + str(val[2]) + " Warlocks") for val in f.index.values]

    series = {
                "name":"Class Combinations",
                "x": x_ticks,
                "y": f['Len']/float(len(data))
    }
    graph = multiBarChart(
                name="classCombos",
                key= 'classCombos',
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Class Combinations in Trials",
                subtitle="A look at the distribution of class combinations in Trials",
                resize=True,
                plotText="Looking at what class combos are used the most often.  "
                            "For example, we can see the difference in use between (1 Hunter, 1 Titan and 1 Warlock) "+
                            "and (2 Hunters, 1 Titan)."
                )   
    graph.width = None

    graph.add_serie(**series)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Class Combos", extras={"rotateLabels":-10})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url='pages/fullPlots/trialsOfOsiris/{0}'.format(graph.name+'.html'))

def classPairingsVictory(data):
    data = data[data[['hunters','titans','warlocks']].sum(1) == 3]

    group = data.groupby(['hunters','titans','warlocks'])
    f = pd.DataFrame({s:{"VictoryRate":(1.0 - (g['standing'].sum()/float(len(g))))} for s,g in group}).T

    x_ticks = [(str(val[0]) + " Hunters, " + str(val[1]) + " Titans, " + str(val[2]) + " Warlocks") for val in f.index.values]

    series = {
                "name":"Class Combinations",
                "x": x_ticks,
                "y": f['VictoryRate']
    }
    graph = multiBarChart(
                name="classCombosVictoryRate",
                key= 'classCombosVictoryRate',
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Victory Rate for different Class Combinations in Trials",
                subtitle="A look at the how frequently different class combos win games.",
                resize=True,
                #plotText="Looking at what class combos are used the most often.  For example, we can see the difference in use between 1 Hunter, 1 Titan and 1 Hunter "+
                #            "and 2 Hunters and 1 Titan."
                )   
    graph.width = None

    graph.add_serie(**series)
    graph.create_y_axis("yAxis", "Victory Rate", format=".2%")
    graph.create_x_axis("xAxis", "Class Combos", extras={"rotateLabels":-10})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url='pages/fullPlots/trialsOfOsiris/{0}'.format(graph.name+'.html'))    

def classPairingsVictory2(data):
    data = data[data[['hunters','titans','warlocks']].sum(1) == 3]

    group = data.groupby(['hunters','titans','warlocks'])
    victory_sum = data.shape[0] - data['standing'].sum()
    f = pd.DataFrame({s:{"VictoryRate":((len(g) - g['standing'].sum())/float(victory_sum))} for s,g in group}).T

    x_ticks = [(str(val[0]) + " Hunters, " + str(val[1]) + " Titans, " + str(val[2]) + " Warlocks") for val in f.index.values]

    series = {
                "name":"Class Combinations",
                "x": x_ticks,
                "y": f['VictoryRate']
    }
    graph = multiBarChart(
                name="classCombosOverallVictoryRate",
                key= 'classCombosOverallVictoryRate',
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Overall Victory Rate for different Class Combinations in Trials",
                subtitle="A look at the how frequently different class combos win games.",
                resize=True,
                #plotText="Looking at what class combos are used the most often.  For example, we can see the difference in use between 1 Hunter, 1 Titan and 1 Hunter "+
                #            "and 2 Hunters and 1 Titan."
                )   
    graph.width = None

    graph.add_serie(**series)
    graph.create_y_axis("yAxis", "Victory Rate", format=".2%")
    graph.create_x_axis("xAxis", "Class Combos", extras={"rotateLabels":-10})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url='pages/fullPlots/trialsOfOsiris/{0}'.format(graph.name+'.html'))       


if __name__ == "__main__":
    plotutils.FULL_PLOT_HTML_DIRECTORY = os.path.join("blog","content","pages","fullPlots","trialsOfOsiris")
    plotutils.FULL_PLOT_JS_DIRECTORY = os.path.join(plotutils.FULL_PLOT_HTML_DIRECTORY, "javascripts")
    plotutils.FULL_PLOT_JSON_DIRECTORY = os.path.join(plotutils.FULL_PLOT_HTML_DIRECTORY, "datafiles")

    data = pd.read_csv("datafiles/trialsOfOsiris.csv", index_col=0)
    teamData = pd.read_csv('datafiles/trialsOfOsiris_teamData.csv', index_col=0)

    classPairings(teamData)
    combatRating_plots.combatRatingDist(data, pages_dir="pages/fullPlots/trialsOfOsiris/", gamemode="Trials Of Osiris", max_limit=600, num_bins=20)
    classPairingsVictory(teamData)    
    classPairingsVictory2(teamData)
