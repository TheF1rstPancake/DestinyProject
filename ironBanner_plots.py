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

def mostUsedWeaponsV2(data):
	non_weapon_columns = ['Unnamed: 0', 'characterClass', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))
	total_kills = data[weapon_columns].sum(1).sum()
	weaponFreq = pd.DataFrame({k:data[k].sum()/total_kills for k in weapon_columns}, index=['Name']).T
	weaponFreq.sort('Name', ascending=False, inplace=True)

	graph = discreteBarChart(
				name="Top20WeaponsV2",
				key= 'Top20WeaponsV2',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Top 20 Killing Machines in Iron Banner",
				subtitle="A look at the weapons with the most kills in Iron Banner",
				resize=True,
				plotText="Each bar is the number of kills with the given weapon out of all weapon kills. " +
						"It should be read as <em>y</em> percent of weapon kills are with <em>x</em>.  "+
						"Note that these percentages do not include super, grenade, melee, or other kills.  It is only out of weapon kills."
				)	
	graph.width = "$('#"+graph.divTitle+"').width()"
	

	x = weaponFreq.head(20).index.values
	y = weaponFreq.head(20)['Name'].values

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

def killsPerPlayer(data):
	weaponSums = {k:data[k].sum() for k in data.columns}
	players = {k: len(data[data[k] > 0]) for k in data.columns}
	totalKills = data.sum(1).sum()

	weaponUsage = pd.DataFrame({"Sum":weaponSums, "Players":players})
	weaponUsage['Frequency'] = weaponUsage['Sum']/totalKills
	weaponUsage['KillsPerPlayer'] = weaponUsage['Sum']/weaponUsage['Players']

	weaponUsage.sort("Frequency", ascending = False, inplace = True)
	top20Weapons = weaponUsage.head(20).sort("KillsPerPlayer", ascending=False)

	graph = discreteBarChart(
				name="Top20KillsPerPlayer",
				key= 'Top20KillsPerPlayer',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Weapons with the Highest Kills Per Player",
				subtitle="A look at the weapons with the most kills per player in Iron Banner",
				resize=True,
				)	
	graph.width = "$('#"+graph.divTitle+"').width()"

	x = top20Weapons.index.values
	y = top20Weapons['KillsPerPlayer'].values

	graph.add_serie(y=y, x=x, name="Weapons")
	graph.create_y_axis("yAxis", "Kills Per Player", format=".2f")
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
	weapon_data = pd.read_csv("datafiles/IronBanner_WeaponUsage.csv", index_col=0)

	mostUsedWeapons(data)
	mostUsedWeaponsV2(weapon_data)
	killsPerPlayer(weapon_data)
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
