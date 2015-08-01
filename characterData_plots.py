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

    mostUsedShader(data)
    shadersByLevel(data)
    mostUsedShaderByClass(data)
    exoticSelectionByClass(data)
    statBreakdownByClass(data)
    #write to index html file
    template = jinja2_env.get_template(os.path.join('index.html'))
    template_values = {
        'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
    }
    output = template.render(template_values)

    with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
        f.write(output.encode('ascii', 'ignore'))
        #f.write(output)
