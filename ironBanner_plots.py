import pandas as pd 
import scipy.stats
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


def mostUsedVictory(data):
	non_weapon_columns = ['Unnamed: 0', 'characterClass', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))
	total_kills = data[weapon_columns].sum(1).sum()
	weaponFreq = pd.DataFrame({k:data[k].sum()/total_kills for k in weapon_columns}, index=['Name']).T
	weaponFreq.sort('Name', ascending=False, inplace=True)

	graph = discreteBarChart(
				name="Top20Victory",
				key= 'Top20Victory',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Victory Rate by Weapons",
				subtitle="A look at how weapons affect victory",
				resize=True,
				plotText="Each bar is the victory rate with the given weapon out of all weapon kills. " +
						"It should be read as <em>y</em> percent of players who use <em>x</em> win.  "
				)	
	graph.width = "$('#"+graph.divTitle+"').width()"
	

	top = weaponFreq.head(20).index.values
	y =[1.0 - (data.ix[data[c] > 0, 'standing'].sum()/float(len(data[data[c] > 0]))) for c in top]

	graph.add_serie(y=y, x=top, name="Weapons")
	graph.create_y_axis("yAxis", "Victory Rate", format=".2%")
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




def averageCombatRating(data):
	non_weapon_columns = ['combatRating', 'Unnamed: 0', 'Unnamed: 0.1', 'characterClass', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))
	data = data[data['combatRating'] != -1]
	weaponFreq = pd.DataFrame({k:data[k].sum() for k in weapon_columns}, index=['Name']).T
	weaponFreq.sort('Name', ascending=False, inplace=True)

	top20Weapons = weaponFreq.head(20)

	combatRatings = pd.DataFrame({k:data[data[k] > 0]['combatRating'].mean() for k in top20Weapons.index.values}, index=["CR"]).T
	combatRatings.sort("CR", ascending=False,inplace=True)

	graph = discreteBarChart(
			name="Top20WeaponsCR",
			key= 'Top20WeaponsCR',
			js_path = "javascripts",
			html_path = FULL_PLOT_HTML_DIRECTORY,
			title="The Average Combat Rating of Players who Use the Top 20 Most Used Weapons",
			subtitle="A look at the weapons with the relative combat ratings of players who use these weapons",
			resize=True,
			)	
	graph.width = "$('#"+graph.divTitle+"').width()"
	

	x = combatRatings.head(20).index.values
	y = combatRatings.head(20)['CR'].values

	graph.add_serie(y=y, x=x, name="Weapons")
	graph.create_y_axis("yAxis", "Frequency", format=".2f")
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



def killDeathRatio(data):
	non_weapon_columns = ['Unnamed: 0', 'characterClass', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))
	
	weaponFreq = pd.DataFrame({k:data[k].sum() for k in weapon_columns}, index=['Name']).T
	weaponFreq.sort('Name', ascending=False, inplace=True)

	top20Weapons = weaponFreq.head(20)

	averageKD = pd.DataFrame({k:data[data[k] > 0]['killDeathRatio'].mean() for k in top20Weapons.index.values}, index=["KDR"]).T
	averageKD.sort("KDR", ascending=False, inplace=True)

	graph = discreteBarChart(
			name="Top20WeaponsKDR",
			key= 'Top20WeaponsKDR',
			js_path = "javascripts",
			html_path = FULL_PLOT_HTML_DIRECTORY,
			title="The Average KDR of Players who Use the Top 20 Most Used Weapons",
			subtitle="A look at the Kill Death Ratio of players who use the top 20 most used weapons",
			resize=True,
			)	
	graph.width = "$('#"+graph.divTitle+"').width()"
	

	x = averageKD.head(20).index.values
	y = averageKD.head(20)['KDR'].values

	graph.add_serie(y=y, x=x, name="Weapons")
	graph.create_y_axis("yAxis", "KDR", format=".2f")
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

def _writeToFile(graph):
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

	weaponUsage = pd.DataFrame({"Total Kills":weaponSums, "Players Using":players})
	weaponUsage['Frequency'] = weaponUsage['Total Kills']/totalKills
	weaponUsage['KillsPerPlayer'] = weaponUsage['Total Kills']/weaponUsage['Players Using']

	weaponUsage.sort("Frequency", ascending = False, inplace = True)
	top20Weapons = weaponUsage.head(20).sort("KillsPerPlayer", ascending=False)
	weaponUsage.to_csv("weaponUsageTabular.csv", encoding="utf-8")

	graph = discreteBarChart(
				name="Top20KillsPerPlayer",
				key= 'Top20KillsPerPlayer',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Kills per Player for the top 20 Weapons Used",
				subtitle="A different way to look at the most used weapons in Iron Banner",
				resize=True,
				plotText= "Each bar is the kills per player for that weapon.  " +
							"Kills Per Player is caluclated by taking the total number of kills for that weapon divided by the numer of people who use it. " +
							"Looking at this graph and comparing it to the top 20 weapons in Iron Banner, we can see that the most used weapon isn't necessarily the most effective. "
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


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def combatRatingDist(data):
	data = pd.DataFrame(data[(data['combatRating'] > 0)])
	CR = data['combatRating']

	#build a histogram of 20 bins from (0,300)
	#The range is set because of a first glance look at the data
	num_bins = 15
	hist = scipy.stats.histogram(CR,numbins=num_bins, defaultlimits=(0,300))

	#add the extra points to the last bin.
	#this will cause there to be a slight increase in the last bin in comparison to the bin before it.
	hist[0][-1] = hist[0][-1]+hist[3]

	#some of the bins barely contain any data.  Add these all to one extended bin

	bins = [c*hist[2] for c in xrange(0,num_bins)]
	bin_strings = ["[{0:.2f}, {1:.2f})".format(bins[b], bins[b+1]) for b in xrange(0,num_bins-1)]
	bin_strings.append("[{0:.2f}, Inf)".format(bins[-1]))

	print(len(bin_strings))
	print(len(hist[0]))

	graph = discreteBarChart(
				name="combatRatingDist",
				key= 'combatRatingDist',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Distribution of Combat Ratings in Iron Banner",
				subtitle="A look at the distribution of combat ratings for players in IB",
				resize=True,
				plotText="Shows the distribution of combat ratings in Iron Banner.  Each bar represents a bin extending from it's starting x position to the next in the following fashion [x, x1)"
				)	
	graph.width = "$('#"+graph.divTitle+"').width()"

	graph.add_serie(x=bin_strings, y = hist[0]/len(CR), name='Distribution')
	graph.create_y_axis("yAxis", "Frequency", format=".2%")
	graph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	graph.buildcontent()
	_writeToFile(graph)

	#get the names of the top 20 weapons
	non_weapon_columns = ['Unnamed: 0', 'characterClass', 'combatRating', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))
	
	top20Weapons = pd.DataFrame({k:data[k].sum() for k in weapon_columns}, index=['Name']).T
	top20Weapons.sort('Name', ascending=False, inplace=True)

	top20Weapons = top20Weapons.head(20).index.values

	#create a quantile for the combat rating so we can do crazy pandas stuff
	#need to add np.inf to bins for this to work
	bins = np.append(bins, np.inf)
	data['quantile'] = pd.cut(data['combatRating'], bins, right=False)
	groupByQuantile = data.groupby("quantile")

	quantiles = data.sort("quantile")['quantile'].unique()
	print(quantiles)
	"""
	weaponUsageByCR = [{
							"name":weapon,
							"x": quantiles,
							"y":[g[weapon].sum()/g[weapon_columns].sum(1).sum() for q, g in groupByQuantile]
						} for weapon in top20Weapons]

	weaponGraph = multiBarChart(
				name="combatRatingWeaponBreakdown",
				key= 'combatRatingWeaponBreakdown',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Distribution of Weapons in Each Combat Ratings ",
				subtitle="A look at the distribution of weapons within each combat rating group",
				resize=True,
				)	
	weaponGraph.width = "$('#"+weaponGraph.divTitle+"').width()"

	for s in weaponUsageByCR:
		weaponGraph.add_serie(**s)

	weaponGraph.create_y_axis("yAxis", "Frequency", format=".2%")
	weaponGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	weaponGraph.buildcontent()
	_writeToFile(weaponGraph)
	"""
	killsPerPlayerPerBin = [{
								"name":weapon,
								"x": quantiles,
								"y": [g[weapon].sum()/len(g[g[weapon] > 0]) for q,g in groupByQuantile if g[weapon].sum() > 0]
							}for weapon in top20Weapons]

	kppGraph = multiBarChart(
				name="combatRatingKPP",
				key= 'combatRatingKPP',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Kills per Player for the top 20 weapons by combat rating ",
				subtitle="A look at the effectiveness of each group with the top 20 weapons",
				resize=True,
				)	
	kppGraph.width = "$('#"+kppGraph.divTitle+"').width()"

	for s in killsPerPlayerPerBin:
		kppGraph.add_serie(**s)

	kppGraph.create_y_axis("yAxis", "Kills per Player", format=".2f")
	kppGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	kppGraph.buildcontent()
	_writeToFile(kppGraph)


	killsPerPlayerPerBin =[]
	for weapon in top20Weapons:
		series = {"name":weapon, "x":quantiles, "y":[]}
		for q,g in groupByQuantile:
			if g[weapon].sum() == 0:
				series['y'].append(0)
			else:
				percentKills = g[weapon].sum()/g[weapon_columns].sum(1).sum()
				percentUsed = float(len(g[g[weapon] > 0]))/len(g)
				series['y'].append(percentKills/percentUsed)

		killsPerPlayerPerBin.append(series)



	percentKillsUsedGraph = multiBarChart(
				name="combatRatingPercentKilledUsed",
				key= 'combatRatingPercentKilledUsed',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Percent Killed divided by Percent Used for Each Combat Rating ",
				subtitle="A different look at the effectiveness of each weapon",
				resize=True,
				)	
	percentKillsUsedGraph.width = "$('#"+percentKillsUsedGraph.divTitle+"').width()"

	for s in killsPerPlayerPerBin:
		percentKillsUsedGraph.add_serie(**s)

	percentKillsUsedGraph.create_y_axis("yAxis", format=".2f")
	percentKillsUsedGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	percentKillsUsedGraph.buildcontent()
	_writeToFile(percentKillsUsedGraph)

if __name__ == "__main__":
	#data = pd.read_csv("datafiles/IronBanner.csv")
	#weapon_data = pd.read_csv("datafiles/IronBanner_WeaponUsage.csv", index_col=0)
	#extras = pd.read_csv("datafiles/IB_Weapons_Fixed.csv")
	combatRatings = pd.read_csv("datafiles/IB_WeaponsUpdated.csv")
	#mostUsedWeapons(data)
	#mostUsedWeaponsV2(weapon_data)
	#killsPerPlayer(weapon_data)
	#mostUsedVictory(extras)
	#killDeathRatio(extras)
	#averageCombatRating(combatRatings)
	combatRatingDist(combatRatings)


	#extra_analysis.weaponPairings(data, FULL_PLOT_HTML_DIRECTORY)

	#write to index html file
	template = jinja2_env.get_template(os.path.join('index.html'))
	template_values = {
		'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
	}
	output = template.render(template_values)

	with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
		f.write(output.encode('ascii', 'ignore'))
		#f.write(output)
