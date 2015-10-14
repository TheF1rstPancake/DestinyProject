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

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))


def combatRatingDist(data, pages_dir="pages/fullPlots/combatRating/", gamemode="Control", max_limit=240, num_bins=12,key="combatRatingDist"):
    data = pd.DataFrame(data[(data['combatRating'] > 0)])
    CR = data['combatRating']

    #build a histogram of 20 bins from (0,300)
    #The range is set because of a first glance look at the data
    #num_bins = 12
    hist = scipy.stats.histogram(CR,numbins=num_bins, defaultlimits=(0,max_limit))

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
                name=key,
                key= key,
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Combat Ratings in {0}".format(gamemode),
                subtitle="A look at the distribution of combat ratings for players in {0}".format(gamemode),
                resize=True,
                plotText="Shows the distribution of combat ratings in {0}.  ".format(gamemode) + 
                            "Each bar represents a bin extending from it's starting x position to the next in the following fashion [x, x1). "
                )   
    graph.width = None

    graph.add_serie(x=bin_strings, y = hist[0]/len(CR), name='Distribution')
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url=pages_dir+ graph.name+'.html')


def combatRatingDiffDist(data, num_bins=10, gamemode="Control",pages_dir="pages/fullPlots/combatRating/"):
    groupByGame = data.groupby("gameId")
    diff= pd.DataFrame({s:{"combatRatingDiff":abs(g.combatRating.values[0]- g.combatRating.values[1])} for s,g in groupByGame if len(g) == 2}).T
    CR_Diff = diff.combatRatingDiff

    hist = scipy.stats.histogram(CR_Diff,numbins=num_bins)

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
                name="combatRatingDiff",
                key= "combatRatingDiff",
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Difference in Combat Rating between Teams",
                subtitle="A look at the distribution of combat ratings for teams in {0}".format(gamemode),
                resize=True,
                plotText="Shows the distribution of combat ratings between teams in {0}.  ".format(gamemode) + 
                            "Each bar represents a bin extending from it's starting x position to the next in the following fashion [x, x1). "
                )   
    graph.width = None

    graph.add_serie(x=bin_strings, y = hist[0]/len(CR_Diff), name='Distribution')
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Combat Rating Difference", extras={"rotateLabels":-25})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url=pages_dir+ graph.name+'.html')    



def scoreDifference(data, num_bins=10, max_limit=None, gamemode="Control", pages_dir="pages/fullPlots/combatRating/"):
    groupByGame = data.groupby("gameId")
    diff= pd.DataFrame({s:{"scoreDiff":abs(g.teamScore.values[0]- g.teamScore.values[1])} for s,g in groupByGame if len(g) == 2  if (g.teamScore != [0,0]).all()}).T
    hist = _makeHistogram(diff['scoreDiff'], max_limit=max_limit, num_bins=num_bins)
    graph = multiBarChart( 
                name="scoreDiff",
                key= "scoreDiff",
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Difference in Score between Teams",
                subtitle="A look at the distribution of combat ratings for teams in {0}".format(gamemode),
                resize=True,
                plotText="Shows the distribution of the difference in **score** between teams in {0}.  ".format(gamemode) + 
                            "Each bar represents a bin extending from it's starting x position to the next in the following fashion [x, x1). "
                )   
    graph.width = None

    graph.add_serie(x=hist["bin_strings"], y = hist["hist"][0]/len(diff), name='Distribution')
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Score Difference", extras={"rotateLabels":-15})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url=pages_dir+ graph.name+'.html') 

def scoreDifferenceByMap(data, num_bins = 10, max_limit=None, gamemode='Control', pages_dir="pages/fullPlots/combatRating/"):
    mapDict = {h:destiny.getMapName(h) for h in data.refrencedId.unique()}

    graph = multiBarChart( 
                name="scoreDiffMap",
                key= "scoreDiffMap",
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Difference in Score between Teams on Each Map",
                subtitle="A look at the distribution of combat ratings for teams in {0}".format(gamemode),
                resize=True,
                plotText="Shows the distribution of the difference in **score** between teams in {0}.  ".format(gamemode) + 
                            "Each bar represents a bin extending from it's starting x position to the next in the following fashion [x, x1). "
                )   
    graph.width = None

    #get the histogram bins
    groupByGame = data.groupby("gameId")
    diff= pd.DataFrame({s:{"scoreDiff":abs(g.teamScore.values[0]- g.teamScore.values[1]), "refrencedId":g.refrencedId.values[0]} for s,g in groupByGame if len(g) == 2 if (g.teamScore != [0,0]).all()}).T
    print(diff.head())
    hist = _makeHistogram(diff['scoreDiff'], max_limit=max_limit, num_bins=num_bins)

    #then cut the entire dataset by the histogram bins
    hist['bins'].append(np.inf)


    diff['scoreDiffBin'] = pd.cut(diff['scoreDiff'], hist['bins'], right=False, labels=hist['bin_strings'])
    diff.sort("refrencedId", inplace=True)
    groupByMap = diff.groupby("refrencedId")

    for m, df in groupByMap: 
        df.sort("scoreDiff", inplace=True)
        groupByBin = df.groupby("scoreDiffBin")
        values = np.array([float(len(g))/len(df) for _,g in groupByBin])
        graph.add_serie(x=hist["bin_strings"], y = values, name=mapDict[m])
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Score Difference", extras={"rotateLabels":-15})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url=pages_dir+ graph.name+'.html') 

def _makeHistogram(data, num_bins=10, max_limit=None):
    hist = None
    if max_limit:
        hist = scipy.stats.histogram(data,numbins=num_bins, defaultlimits=(0,max_limit))
    else:
        hist = scipy.stats.histogram(data,numbins=num_bins)

    #add the extra points to the last bin.
    #this will cause there to be a slight increase in the last bin in comparison to the bin before it.
    hist[0][-1] = hist[0][-1]+hist[3]

    #some of the bins barely contain any data.  Add these all to one extended bin
    bins = [c*hist[2] for c in xrange(0,num_bins)]

    #the first bin should be (0, bin_edge) because literal 0 is not included in this data.
    bin_strings = ["(0,{0:.2f})".format(bins[1])]
    bin_strings.extend(["[{0:.2f}, {1:.2f})".format(bins[b], bins[b+1]) for b in xrange(1,num_bins-1)])
    bin_strings.append("[{0:.2f}, Inf)".format(bins[-1]))    

    return {"hist":hist, "bin_strings":bin_strings, "bins":bins}

def standardScoreDist(data, max_limit=None, num_bins=10, gamemode="Control", pages_dir="pages/fullPlots/combatRating/"):
    hist = _makeHistogram(data['standardScore'], max_limit=max_limit, num_bins=num_bins)
    graph = multiBarChart( 
                name="standardScoreDist",
                key= "standardScoreDist",
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Standarized Score",
                subtitle="A look at the distribution of standardized score",
                resize=True,
                )   
    graph.width = None

    graph.add_serie(x=hist["bin_strings"], y = hist["hist"][0]/float(data.shape[0]), name='Distribution')
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Standardized Score", extras={"rotateLabels":-15})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url=pages_dir+ graph.name+'.html')        

def fireTeamHist(data, max_limit=6, num_bins=12, gamemode="Control", pages_dir="pages/fullPlots/combatRating"):
    hist = _makeHistogram(data['membersInFireTeam'], max_limit=max_limit, num_bins=num_bins,gamemode=gamemode, pages_dir=pages_dir)
    graph = multiBarChart( 
                name="membersInFireTeamDist",
                key= "membersInFireTeamDist",
                js_path = "javascripts",
                html_path = plotutils.FULL_PLOT_HTML_DIRECTORY,
                title="Distribution of Fire Team Size",
                subtitle="A look at the the frequency of different fire team sizes",
                resize=True,
                )   
    graph.width = None

    graph.add_serie(x=hist["bin_strings"], y = hist["hist"][0]/float(data.shape[0]), name='Distribution')
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Fire Team Size", extras={"rotateLabels":-15})
    
    graph.buildcontent()
    plotutils.writeGraph(graph, htmlTemplate="fullPlotTemplate.rst", extension=".rst", url=pages_dir+ graph.name+'.html')


if __name__ == "__main__":
    plotutils.FULL_PLOT_HTML_DIRECTORY = os.path.join("blog","content","pages","fullPlots","combatRating")
    plotutils.FULL_PLOT_JS_DIRECTORY = os.path.join(plotutils.FULL_PLOT_HTML_DIRECTORY, "javascripts")
    plotutils.FULL_PLOT_JSON_DIRECTORY = os.path.join(plotutils.FULL_PLOT_HTML_DIRECTORY, "datafiles")

    PLOT_TEMPLATES = "plotTemplates"
    data = pd.read_csv("datafiles/standard_data2.csv", index_col=0)
    #teamData = pd.read_csv("datafiles/teamData.csv",index_col=0)
    #combatRatingDist(data)
    #combatRatingDist(teamData, gamemode="Control (Team Based)", key="combatRatingDistTeamBased", max_limit=188, num_bins=15)
    #combatRatingDiffDist(teamData, gamemode="Control",num_bins=10)

    #scoreDifference(teamData, num_bins=12, max_limit=17000)
    #scoreDifferenceByMap(teamData, num_bins=12, max_limit=17000)
    fireTeamHist(data)

