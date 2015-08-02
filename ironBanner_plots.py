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

FULL_PLOT_HTML_DIRECTORY = os.path.join("blog","content", "fullPlots","IronBanner")
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


def getTopWeapons(data, top=20):
	#get the names of the top 20 weapons
	non_weapon_columns = ['Unnamed: 0', 'characterClass', 'combatRating', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))
	
	top20Weapons = pd.DataFrame({k:data[k].sum() for k in weapon_columns}, index=['Name']).T
	top20Weapons.sort('Name', ascending=False, inplace=True)

	top20Weapons = top20Weapons.head(top).index.values

	return top20Weapons


def weaponUsageByCR(data, top20Weapons, weapon_columns):


	quantiles = data.sort("quantile")['quantile'].unique()
	groupByQuantile = data.groupby("quantile")

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
				title="Distribution of Weapon Kills in Each Combat Ratings ",
				subtitle="A look at the frequency of weapon kills within each combat rating group",
				resize=True,
				plotText='Each bar is the number of kills with a particular weapon in a bin divided by the total number of kills in the bin. ' +
						'This is going to show us how each group uses the top 20 weapons used overall.  ' + 
						'The difference in bar height when all bars are stacked is because each group does not use these top 20 equally. ' +
						'A big difference in a percentage would indicate that a certain combat rating group does not get as many kills with a weapon as others. '+
						'Consistent percentages for a give weapon contributes to the total number of kills for that group equally compared to others. ' +
						'The emphasis here is on <strong>kills</strong> not on use.'
				)	
	weaponGraph.width = "$('#"+weaponGraph.divTitle+"').width()"

	for s in weaponUsageByCR:
		weaponGraph.add_serie(**s)

	weaponGraph.create_y_axis("yAxis", "Frequency", format=".2%")
	weaponGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	weaponGraph.buildcontent()
	_writeToFile(weaponGraph)

	return weaponGraph

def KillsPerPlayerPerWeaponPerBin(data, top20Weapons, weapon_columns):

	quantiles = data.sort("quantile")['quantile'].unique()
	groupByQuantile = data.groupby("quantile")

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
				plotText="This graph shows the Kills-per-Player with each weapon within each group. " +
						"Each bar is the number of kills with that weapon in that group divided by the number of players who use that weapon in that group."
				)	
	kppGraph.width = "$('#"+kppGraph.divTitle+"').width()"

	for s in killsPerPlayerPerBin:
		kppGraph.add_serie(**s)

	kppGraph.create_y_axis("yAxis", "Kills per Player", format=".2f")
	kppGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	kppGraph.buildcontent()
	_writeToFile(kppGraph)

	return kppGraph

def PercentKilledUsedPerBin(data, top20Weapons,weapon_columns):

	percentKilledUsedSeries =[]
	quantiles = data.sort("quantile")['quantile'].unique()
	groupByQuantile = data.groupby("quantile")

	for weapon in top20Weapons:
		series = {"name":weapon, "x":quantiles, "y":[]}
		for q,g in groupByQuantile:
			if g[weapon].sum() == 0:
				series['y'].append(0)
			else:
				percentKills = g[weapon].sum()/g[weapon_columns].sum(1).sum()
				percentUsed = float(len(g[g[weapon] > 0]))/len(g)
				series['y'].append(percentKills/percentUsed)

		percentKilledUsedSeries.append(series)

	percentKillsUsedGraph = multiBarChart(
				name="combatRatingPercentKilledUsed",
				key= 'combatRatingPercentKilledUsed',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Percent Killed divided by Percent Used for Each Combat Rating ",
				subtitle="A different look at the effectiveness of each weapon",
				resize=True,
				plotText="This graph shows the effectiveness of each weapon in each combat rating group. "
						"Each bar is the percentage of kills with a particular weapon divided by the percentage of players using that weapon. " +
						"What this does is show us the impact that certain weapons have on each group.  "
						"Values greater than 1 mean that the percentage of kills is higher than the percentage of users.  " +
						"In other words, these users are generating more kills than other users in their combat rating group. "+
						"For example, if a 15 percent of <em>Group-A</em> use <em>Weapon-Z</em> and <em>Weapon-Z</em> accounts for 30 percent of kills in that group, "+
						"Then <em>Weapon-Z's</em> effectiveness in that group is 2.  "+
						"This could then be compared to <em>Weapon-Y</em> which is used by 20 percent of players but only accounts for 10 percent of all kills. "+
						"While <em>Weapon-Y</em> is used more, it accounts for less kills thus making it less effective. "+
						"Be careful when comparing across groups though.  " +
						"Just because Weapon-Z has an effectiveness of 2 in Group-A and only an effectiveness of 1 in Group-B does not mean that Group-A is more effective with the weapon than Group-B."
				)	
	percentKillsUsedGraph.width = "$('#"+percentKillsUsedGraph.divTitle+"').width()"

	for s in percentKilledUsedSeries:
		percentKillsUsedGraph.add_serie(**s)

	percentKillsUsedGraph.create_y_axis("yAxis", "Percent Killed/Percent Used", format=".2f")
	percentKillsUsedGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	percentKillsUsedGraph.buildcontent()
	_writeToFile(percentKillsUsedGraph)

def PercentUsedPerBin(data, top20Weapons, weapon_columns):
	quantiles = data.sort("quantile")['quantile'].unique()
	groupByQuantile = data.groupby("quantile")
	percentUsedSeries = [{
							"name":weapon,
							"x":quantiles,
							"y":[float(len(g[g[weapon] > 0]))/len(g) for q,g in groupByQuantile]
						} for weapon in top20Weapons]

	percentUsedGraph = multiBarChart(
				name="combatRatingPercentUsed",
				key= 'combatRatingPercentUsed',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Percent of Weapons Used for Each Combat Rating ",
				subtitle="A look at the frequency of use of the top 20 weapons in each combat rating group",
				resize=True,
				plotText= "This graph should be read as <em>y</em> percent of players with a combat rating of <em>x</em> use <em>color</em> weapon. " +
							"It is imporant to note that these percentages do not add up to 100.  In fact, stacking these bins will actually show many of them exceed 100. " +
							"That is because players can be counted twice if they use multiple weapons in a game.  It is still correct to say that "+
							"<em>y</em> percent of players with a combat rating of <em>x</em> use <em>color</em> weapon. " +
							"It is <strong>incorrect</strong> to say that <em>y</em> percent of players with a combat rating of <em>x</em> use <strong>only</strong> <em>color</em> weapon."
				)	
	percentUsedGraph.width = "$('#"+percentUsedGraph.divTitle+"').width()"

	for s in percentUsedSeries:
		percentUsedGraph.add_serie(**s)

	percentUsedGraph.create_y_axis("yAxis", "Percent Used", format=".2%")
	percentUsedGraph.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	percentUsedGraph.buildcontent()
	_writeToFile(percentUsedGraph)



def combatRatingDist(data):
	data = pd.DataFrame(data[(data['combatRating'] > 0)])
	top20Weapons = getTopWeapons(data,20)
	CR = data['combatRating']

	non_weapon_columns = ['Unnamed: 0', 'characterClass', 'combatRating', 'characterId', 'characterLevel', 'completed', 
							'date', 'gameId', 'killDeathRatio', 'kills','membershipId','mode','refrencedId','score','standing','team']

	weapon_columns = list(set(data.columns.values) - set(non_weapon_columns))


	#build a histogram of 20 bins from (0,300)
	#The range is set because of a first glance look at the data
	num_bins = 12
	hist = scipy.stats.histogram(CR,numbins=num_bins, defaultlimits=(0,240))

	#add the extra points to the last bin.
	#this will cause there to be a slight increase in the last bin in comparison to the bin before it.
	hist[0][-1] = hist[0][-1]+hist[3]

	#some of the bins barely contain any data.  Add these all to one extended bin

	bins = [c*hist[2] for c in xrange(0,num_bins)]
	bin_strings = ["[{0:.2f}, {1:.2f})".format(bins[b], bins[b+1]) for b in xrange(0,num_bins-1)]
	bin_strings.append("[{0:.2f}, Inf)".format(bins[-1]))


	logger.info("Combat Rating Dist")
	graph = multiBarChart(
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


	#create a quantile for the combat rating so we can do crazy pandas stuff
	#need to add np.inf to bins for this to work
	bins = np.append(bins, np.inf)
	data['quantile'] = pd.cut(data['combatRating'], bins, right=False)

	groupByQuantile = data.groupby("quantile")
	quantiles = data.sort("quantile")['quantile'].unique()

	logger.info("Weapon Usage by CR Graph")
	weaponGraph = weaponUsageByCR(data,top20Weapons,weapon_columns)
	
	logger.info("KPP Per Weapon Per Bin")
	killsPerPlayerPerWeaponPerBin = KillsPerPlayerPerWeaponPerBin(data,top20Weapons,weapon_columns)

	logger.info("Percent Killed/ Percent Used")
	PercentKilledUsedPerBin(data,top20Weapons, weapon_columns)

	logger.info("Percent Used")
	PercentUsedPerBin(data, top20Weapons, weapon_columns)
	
	killsPerCombatRating = discreteBarChart(
				name="combatRatingKills",
				key= 'combatRatingKills',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Kills by Combat Rating",
				subtitle="A look at the the number of kills each combat rating contributes to all carnage",
				resize=True,
				plotText= "The distribution of kills across all players.  Each bar is the total kills in that bin divided by the total number of kills in the set."
				)	
	killsPerCombatRating.width = "$('#"+killsPerCombatRating.divTitle+"').width()"


	total_kills = data[weapon_columns].sum(1).sum()
	killsPerBin = [g[weapon_columns].sum(1).sum()/total_kills for _,g in groupByQuantile]
	killsPerCombatRating.add_serie(x=quantiles, y = killsPerBin, name="%Kills")

	killsPerCombatRating.create_y_axis("yAxis", "Frequency", format=".2%")
	killsPerCombatRating.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})


	killsPerCombatRating.buildcontent()
	_writeToFile(killsPerCombatRating)


	killsPerPlayerPerCombatRating = discreteBarChart(
				name="combatRatingKillsPerPlayerAll",
				key= 'combatRatingKillsPerPlayerAll',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Kills per Player in Each Combat Rating",
				subtitle="A look at the the efficiency of each player in each combat rating group",
				resize=True,
				plotText= "Each bar is the total number of kills in the bin divided by the number of players in that bin. " +
						"We expect the KPP to increase with combat rating.  'Better' players should be getting more kills than 'worse' players."
				)	
	killsPerPlayerPerCombatRating.width = "$('#"+killsPerPlayerPerCombatRating.divTitle+"').width()"


	total_kills = data[weapon_columns].sum(1).sum()
	killsPerPlayerPerCombatRating.add_serie(x=quantiles, y = [g[weapon_columns].sum(1).sum()/len(g) for _,g in groupByQuantile], name="%Kills")

	killsPerPlayerPerCombatRating.create_y_axis("yAxis", "Frequency", format=".2f")
	killsPerPlayerPerCombatRating.create_x_axis("xAxis", "Combat Rating", extras={"rotateLabels":-25})
	
	killsPerPlayerPerCombatRating.buildcontent()
	_writeToFile(killsPerPlayerPerCombatRating)



if __name__ == "__main__":
	data = pd.read_csv("datafiles/IronBanner.csv")
	weapon_data = pd.read_csv("datafiles/IronBanner_WeaponUsage.csv", index_col=0)
	extras = pd.read_csv("datafiles/IB_Weapons_Fixed.csv")
	#combatRatings = pd.read_csv("datafiles/IB_WeaponsUpdated.csv")
	
	mostUsedWeapons(data)
	extra_analysis.weaponPairings(data, FULL_PLOT_HTML_DIRECTORY)
	mostUsedWeaponsV2(weapon_data)
	killsPerPlayer(weapon_data)
	mostUsedVictory(extras)
	killDeathRatio(extras)
	#averageCombatRating(combatRatings)
	#combatRatingDist(combatRatings)



	#write to index html file
	template = jinja2_env.get_template(os.path.join('index.html'))
	template_values = {
		'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
	}
	output = template.render(template_values)

	with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
		f.write(output.encode('ascii', 'ignore'))
		#f.write(output)
