import pandas as pd 
import destinyPlatform as destiny 
import json
import os
import numpy as np
import jinja2
import logging
import sys
from nvd3py import *

FULL_PLOT_HTML_DIRECTORY = os.path.join("blog","content","fullPlots","characterData")
FULL_PLOT_JS_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "javascripts")
FULL_PLOT_JSON_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "datafiles")

PLOT_TEMPLATES = "plotTemplates"

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))


def _writeGraph(graph):
    graph.buildcontent()

    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
    template_values = {
        'destinyGraph': graph.__dict__,
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + ".html")), 'w') as f:
        f.write(output)


def shipBreakdownAbove20(data):
    data = data[data['level'] >= 20]
    shipBreakdown(data, key="AboveLevel20")

def shipBreakdownBelow20(data):
    data = data[data['level'] < 20]
    shipBreakdown(data, key="BelowLevel20")


def shipBreakdown(data, key="Overall"):
    groupByShip = data.groupby("Ships")
    shipFreq = pd.DataFrame({s:{"Frequency":len(g)/float(len(data)), "Tier":data[data['Ships'] == s]['Ships Tier'].values[0]} for s, g in groupByShip}).T

    #first, make 2 plots.  One detailing the most used ships, the second looking at the least used.
    shipFreq.sort("Frequency", inplace=True)
    mostUsedSeries = [{
            "name":"Most Used Ships",
            "x":shipFreq.tail(10).index.values,
            "y": shipFreq.tail(10)['Frequency'].values
    }]    

    graph = discreteBarChart(
                name="MostUsedShips"+key,
                key= 'MostUsedShips' + key,
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Top 10 Equipped Ships " + key,
                subtitle="A look the top 10 most equipped ships",
                resize=True,
                )   
    graph.width = None

    for s in mostUsedSeries:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Ship", extras={"rotateLabels":-25})
    _writeGraph(graph)

    leastUsedSeries = [{
            "name":"Most Used Ships",
            "x":shipFreq.head(10).index.values,
            "y": shipFreq.head(10)['Frequency'].values
    }]

    graph = discreteBarChart(
                name="LeastUsedShips"+key,
                key= 'LeastUsedShips'+key,
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title= "10 Least Equipped Ships " + key,
                subtitle="A look the 10 least equipped ships",
                resize=True,
                )   
    graph.width = None

    for s in leastUsedSeries:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".3%")
    graph.create_x_axis("xAxis", "Ship", extras={"rotateLabels":-25})
    _writeGraph(graph)


def factionsByClass(data):
    #first we need a list of all faction items
    factionItems = {'Hunter':{
                        "Future War Cult":['Astrolord Cloak', 'Choas Cloak', 'Cloak of Immanent War', 'Cloak of No Tomorrow', 'Cloak of Repair'],
                        "Dead Orbit": ['Cloak of Oblivion', ' Cloak of the Exodus', 'Cloak of the Sojourn','Dead Light Cloak'], 
                        "New Monarchy": ['Cloak of Order', 'Cloak of the Justicars', 'Cloak of the Rising'],
                },
    'Warlock':{
                "Future War Cult":['Circle of War', 'Immanent War', 'No Tomorrow', 'The Chaos Constant'],
                "Dead Orbit": ['Death of Fate', 'Light Beyond', 'Ritual Expansion', 'Willful Exodus'], 
                "New Monarchy": ['Faceless Demise', 'The Age to Come', 'The Order','The Risen Ones'],
            },
    'Titan':{
                "Future War Cult":['Immanent War Mark', 'Mark of Chaos', 'Mark or No Tomorrow','Mark of the Circle'],
                "Dead Orbit": ['Dead Light Mark', 'Mark of Oblivion', 'Mark of the Exodus', 'Mark of the Sojourn'], 
                "New Monarchy": ['Mark of the Executor','Mark of the Initiative','Mark of the Order','Mark of the Rising'],
            }
    }

    data = data[data['level'] >= 20]
    groupByClass = data.groupby("class")

    factions = ['Future War Cult', 'Dead Orbit', 'New Monarchy']
    factionBreakdown = pd.DataFrame({c:{f:len(g[g['Class Armor'].isin(factionItems[c][f])])/float(len(g)) for f in factions} for c,g in groupByClass}).T

    #now we have to add the "other" category.
    for c,_ in groupByClass:
        for f in factions:
            factionBreakdown.ix[c,'Other'] = 1.0- factionBreakdown.ix[c].sum()

    #rotate it back so that factions are the x axis, and classes are colors
    factionBreakdown = factionBreakdown.T

    print "BY CLASS:\n", factionBreakdown.T, '\n',factionBreakdown.T.sum(),"\n------------------------"

    series = [{
            "name": c,
            "x":factionBreakdown.columns.values,
            'y':factionBreakdown.ix[c].values
    }for c in factionBreakdown[c].index.values]

    graph = multiBarChart(
                name="FactionBreakdownByClass",
                key= 'FactionBreakdownByClass',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Faction Breakdown By Class",
                subtitle="A look at how each pledges to a faction",
                resize=True,
                )   
    graph.width = None

    for s in series:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Class", extras={"rotateLabels":-25})
    
    _writeGraph(graph)

    #now to factions by level
    #it follows the same structure as groupby class
    groupByLevel = data.groupby("level")

    #we want to change the factionItems map to now map factions to their particular armor pieces irregardless of class
    #the first step creates a map where the keys are the factions and the items are a list of lists of items
    #the second step breaksdown the lists of lists into a single flattened list
    factionItemsNotClass = {f:[factionItems[c][f] for c in factionItems.keys()] for f in factions}
    factionItemsNotClass = {f: [i for sublist in factionItemsNotClass[f] for i in sublist] for f in factions}

    factionBreakdown = pd.DataFrame({c:{f:len(g[g['Class Armor'].isin(factionItemsNotClass[f])])/float(len(g)) for f in factions} for c,g in groupByLevel}).T

    #now we have to add the "other" category.
    for c,_ in groupByLevel:
        for f in factions:
            factionBreakdown.ix[c,'Other'] = 1.0- factionBreakdown.ix[c].sum()
    print "BY LEVEL: \n", factionBreakdown
    series = [{
            "name": c,
            "x":factionBreakdown[c].index.values.astype(str),
            'y':factionBreakdown[c].values
    }for c in factionBreakdown.columns[0:3]]

    graph = lineChart(
                name="FactionBreakdownByLevel",
                key= 'FactionBreakdownByLevel',
                js_path = "javascripts",
                use_interactive_guideline = True,
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Faction Breakdown By Level",
                subtitle="A look to see if rank affects faction participation",
                resize=True,
                )   
    graph.width = None

    for s in series:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Class", extras={"rotateLabels":-25})
    
    _writeGraph(graph)

    #now we can look at it without grouping at all
    factionBreakdown = pd.DataFrame({f:len(data[data['Class Armor'].isin(factionItemsNotClass[f])])/float(len(data)) for f in factions}, index=["Freq"]).T
    print(factionBreakdown)
    factionBreakdown.ix['Other'] = 1.0 - factionBreakdown["Freq"].sum()
    series = [{
            "name": "Distribution",
            "x":factionBreakdown.index.values[0:3],
            'y':factionBreakdown['Freq'].values[0:3]
    }]

    graph = discreteBarChart(
                name="FactionBreakdown",
                key= 'FactionBreakdown',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Faction Breakdown By Level",
                subtitle="A look at how players join factions",
                resize=True,
                color="category10"
                )   
    graph.width = None

    for s in series:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Class", extras={"rotateLabels":-25})
    
    _writeGraph(graph)



def statBreakdownByClass(data):
    data = data[data['level'] >= 20]
    groupByClass = data.groupby("Subclass")

    statColumns = [c for c in data.columns if "STAT_" in c]

    #there are more stats in the stats columns than just Intellect, Discipline, Strength.
    #make a separate list of the IDS stats here
    IDS = ['STAT_INTELLECT', 'STAT_DISCIPLINE', 'STAT_STRENGTH']

    statBreakdown = pd.DataFrame({sub : {c:g[c].mean() for c in statColumns} for sub, g in groupByClass}).T

    series = [{
            "name":col[5] + col[6:].lower(),
            "y": statBreakdown[col].values,
            "x":statBreakdown[col].index.values
    } for col in IDS]

    graph = multiBarChart(
                name="IntellectDisciplineStrengthBySub",
                key= 'IntellectDisciplineStrengthBySub',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Stat Breakdown by Subclass",
                subtitle="A look at how each subclass makes use of Intellect, Discipline and Strength",
                resize=True,
                )   
    graph.width = None

    for s in series:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".1f")
    graph.create_x_axis("xAxis", "Class", extras={"rotateLabels":-25})
    
    graph.buildcontent()

    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
    template_values = {
        'destinyGraph': graph.__dict__,
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + ".html")), 'w') as f:
        f.write(output)




def exoticSelectionByClass(data):
    data = data[data['level'] >= 20]
    #data.sort('Subclass', inplace=True)
    groupByClass = data.groupby("Subclass")

    armorCols = ['Chest Armor Tier', 'Gauntlets Tier', 'Helmet Tier', 'Leg Armor Tier']

    exoticChoices = pd.DataFrame({sub: {c:float(len(g[g[c] == 'Exotic']))/len(g) for c in armorCols} for sub,g in groupByClass}).T

    series = [{
                "name": col[0:-5],
                "x": exoticChoices.index.values,
                "y": exoticChoices[col].values
    } for col in exoticChoices.columns]


    graph = multiBarChart(
                name="ExoticArmorChoicesBySub",
                key= 'ExoticArmorChoicesBySub',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Exotic Armor Slot Selection Breakdown by Sub",
                subtitle="A look at how players chose to use their exotic armor by subclass",
                resize=True,
                )   
    graph.width = None

    for s in series:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Class", extras={"rotateLabels":-25})
    
    graph.buildcontent()

    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
    template_values = {
        'destinyGraph': graph.__dict__,
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + ".html")), 'w') as f:
        f.write(output)



def mostUsedShaderByClass(data):
    data = data[data['level'] >= 20]

    topShaders = []
    groupByClass = data.groupby("class")
    for c, g in groupByClass:
        groupByShader = g.groupby('Shaders')
        top10Shaders = pd.DataFrame([{'Class':c, 'Shader':s, 'Freq':float(len(group))/len(g)} for s, group in groupByShader]).sort("Freq").tail(10)
        topShaders.append(top10Shaders)
    
    topShadersByClass = pd.concat(topShaders).sort(["Class", "Freq"], ascending=False)

    groupByShader = topShadersByClass.groupby("Class")
    series = [{
                "name": c,
                "x": g['Shader'].values,
                "y": g['Freq'].values,
            } for c, g in groupByShader]

    graph = multiBarChart(
                name="Top10ShadersInEachClass",
                key= 'Top10ShadersInEachClass',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Top 10 Equipped Shaders in Each Class",
                subtitle="A look at the top 10 most frequently equipped shaders for each class",
                resize=True,
                )   
    graph.width = None

    for s in series:
        graph.add_serie(**s)
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Shader", extras={"rotateLabels":-25})
    
    graph.buildcontent()

    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
    template_values = {
        'destinyGraph': graph.__dict__,
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + ".html")), 'w') as f:
        f.write(output)
 

def mostUsedShader(data):
    groupByMostUsed = data.groupby("Shaders")
    mostUsed = pd.DataFrame([(d, len(groupByMostUsed.get_group(d))) for d in groupByMostUsed.groups.keys() if d != 'None'])
    mostUsed.columns = ['Name', 'Length']

    totalUsers = len(data[data['Shaders'] != 'None'])
    mostUsed['Frequency'] = mostUsed['Length']/totalUsers


    mostUsed.sort("Frequency",ascending=False,inplace=True)

    x = mostUsed['Name'][0:10].values
    y = mostUsed['Frequency'][0:10].values

    graph = discreteBarChart(
                name="Top10Shaders",
                key= 'Top10Shaders',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Top 10 Equipped Shaders",
                subtitle="A look at the top 10 most frequently equipped shaders",
                resize=True,
                plotText="This is a snapshot look at the top 10 shaders.  It is not to say these are the most used over life, they are the most currently equipped.</br>"+
                        "The top 10 shaders account for <strong>{0:.2f}<strong> percent of use".format(float(sum(y))*100)
                )   
    graph.width = None
    #graph.width = "$({0}).width()".format(graph.divTitle)
    #graph.height = "$({0}).height()".format(graph.divTitle)

    graph.add_serie(y=y, x=x, name="Shaders")
    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Shaders", extras={"rotateLabels":-25})
    
    graph.buildcontent()

    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
    template_values = {
        'destinyGraph': graph.__dict__,
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + ".html")), 'w') as f:
        f.write(output)


def shadersByLevel(data):
    data = data[data['level'] >= 20]
    
    groupByMostUsed = data.groupby("Shaders")
    mostUsed = pd.DataFrame([(d, len(groupByMostUsed.get_group(d))) for d in groupByMostUsed.groups.keys() if d != 'None'])
    mostUsed.columns = ['Name', 'Length']

    totalUsers = len(data[data['Shaders'] != 'None'])
    mostUsed['Frequency'] = mostUsed['Length']/totalUsers

    mostUsed.sort("Frequency",ascending=False,inplace=True)

    topShaders = sorted(mostUsed['Name'][0:10].values)
    print(topShaders)

    groupByLevel = data.groupby("level")

    x = sorted([str(g) for g in list(groupByLevel.groups.keys())])

    shadersByLevel = [{
                        "name":shader,
                        "x":x,
                        "y": [ float(len(g[g["Shaders"]==shader]))/len(g) for l, g in groupByLevel]
                    } for shader in topShaders]
    
    graph = multiBarChart(
                name="Top10ShadersByLevel",
                key= 'Top10ShadersByLevel',
                js_path = "javascripts",
                html_path = FULL_PLOT_HTML_DIRECTORY,
                title="Top 10 Equipped Shaders by Level",
                subtitle="A look at the top 10 most frequently equipped shaders across each level group",
                resize=True,
                plotText="This is a snapshot look at the top 10 shaders broken down by character level" +
                            "Since player's can't equip shaders before level 20, this is a subset of the data looking only at players above level 20."
                )   
    #graph.width = "$('#"+graph.divTitle+"').width()"
    graph.width = None
    graph.height = None


    for s in shadersByLevel:
        graph.add_serie(**s)

    graph.create_y_axis("yAxis", "Frequency", format=".2%")
    graph.create_x_axis("xAxis", "Shaders", extras={"rotateLabels":-25})
    
    graph.buildcontent()

    with open(graph.fullJS, 'w') as f:
        f.write(graph.htmlcontent)

    #write to html file
    template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
    template_values = {
        'destinyGraph': graph.__dict__,
    }
    output = template.render(template_values)
    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY, (graph.name + ".html")), 'w') as f:
        f.write(output)

if __name__ == "__main__":
    #teamData = pd.read_csv("datafiles/teamData.csv")
    data = pd.read_csv("datafiles/character_data.csv")
    """
    mostUsedShader(data)
    shadersByLevel(data)
    mostUsedShaderByClass(data)
    exoticSelectionByClass(data)
    statBreakdownByClass(data)
    """
    shipBreakdown(data)
    shipBreakdownAbove20(data)
    shipBreakdownBelow20(data)
    factionsByClass(data)
    #write to index html file
    template = jinja2_env.get_template(os.path.join('index.html'))
    template_values = {
        'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
        f.write(output.encode('ascii', 'ignore'))
        #f.write(output)
