import pandas as pd 
import destinyPlatform as destiny 
import json
import os
import numpy as np
import jinja2
import logging
import sys
from nvd3py import *
import extra_analysis

FULL_PLOT_HTML_DIRECTORY = os.path.join("fullPlots","IronBanner")
FULL_PLOT_JS_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "javascripts")
FULL_PLOT_JSON_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "datafiles")

PLOT_TEMPLATES = "plotTemplates"

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

logger.addHandler(ch)

def mostUsedWeapons(data):
	"""
	Create a graph that shows the usage of each class
	"""

	groupByMostUsed = data.groupby("mostUsedWeapon1Name")
	mostUsed = pd.DataFrame([(d, len(groupByMostUsed.get_group(d))) for d in groupByMostUsed.groups.keys() if d != 'None'])
	mostUsed.columns = ['Name', 'Length']

	totalUsers = len(data[data['mostUsedWeapon1Name'] != 'None'])
	mostUsed['Frequency'] = mostUsed['Length']/totalUsers


	graph = discreteBarChart(
				name="Top10Weapons",
				key= 'Top10Weapons',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Top 10 Weapons Used in Iron Banner",
				subtitle="A look at the top 10 most frequently used weapons in Iron Banner",
				resize=True,
				plotText="Each bar is the number of players who finish a game where that weapon is there most used. "+
						"It should be read as <em>y</em> percent of players finish a game with <em>x</em> as their most used weapon."
				)	
	graph.width = "$('#"+graph.divTitle+"').width()"
	
	mostUsed.sort("Frequency",ascending=False,inplace=True)


	x = mostUsed['Name'][0:10].values
	y = mostUsed['Frequency'][0:10].values


	graph.add_serie(y=y, x=x, name="Weapons")
	graph.create_y_axis("yAxis", "Frequency", format=".2%")
	graph.create_x_axis("xAxis", "Weapon Name", extras={"rotateLabels":-25})
	
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
	data = pd.read_csv("datafiles/IronBanner.csv")

	mostUsedWeapons(data)
	extra_analysis.weaponPairings(data, FULL_PLOT_HTML_DIRECTORY)

	#write to index html file
	template = jinja2_env.get_template(os.path.join('index.html'))
	template_values = {
		'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
	}
	output = template.render(template_values)

	with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
		f.write(output.encode('ascii', 'ignore'))
		#f.write(output)
