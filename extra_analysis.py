import pandas as pd 
import destinyPlatform as destiny 
import json
import os
import numpy as np
import jinja2
import logging
import sys
from nvd3py import *

FULL_PLOT_HTML_DIRECTORY = os.path.join("fullPlots")
FULL_PLOT_JS_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "javascripts")
FULL_PLOT_JSON_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "datafiles")

PLOT_TEMPLATES = "plotTemplates"

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

logger.addHandler(ch)


class destinyPlot(object):
	def __init__(self, data, title, key, htmlFilePath, subtitle,
					plotText = "Hello World!", 
					dataFilePath="datafiles", jsFilePath="javascripts",
					jsTemplateName = "javascriptTemplate.js",
					stacked = False, reduceXAxis = False):
		"""
		Initialize new plot object

		:param data:	data to be used for plot
		:param title:	title of graph
		:param key:		unique identifier for this graph. This key is used to generate div ids and json and javascript filenames
		"""

		self.data = data
		self.title = title
		self.key = key

		self.divTitle = key
		self.javascriptFileName = key+".js"
		self.jsonFileName = key+'.json'
		self.htmlFileName = key+".html"
		self.javascriptFileLocation = os.path.join(jsFilePath, self.javascriptFileName)
		self.jsonFileLocation = os.path.join(dataFilePath, self.jsonFileName)
		self.htmlFileLocation = os.path.join(htmlFilePath, self.htmlFileName)

		self.subtitle = subtitle
		self.plotText = plotText

		self.stacked = stacked
		self.reduceXAxis = reduceXAxis
		
		#write data to json file
		with open(os.path.join(htmlFilePath, dataFilePath, self.jsonFileName), 'w') as f:
			json.dump(data, f)

		#write to javascript file
		template = jinja2_env.get_template(os.path.join(jsTemplateName))
		template_values = {
			'destinyGraph':self.__dict__,
		}
		output = template.render(template_values)

		with open(os.path.join(htmlFilePath, jsFilePath, self.javascriptFileName), 'w') as f:
			f.write(output)

		#write to html file
		template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
		template_values = {
			'destinyGraph': self.__dict__,
		}
		output = template.render(template_values)

		with open(self.htmlFileLocation, 'w') as f:
			f.write(output)

def classUsage(data):
	"""
	Create a graph that shows the usage of each class
	"""

	data = data[data['characterClass'] != '0']
	groupByClass = data.groupby("characterClass")


	graph = discreteBarChart(
				name="ClassUsage",
				key= 'ClassUsage',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				title="Class Usage Breakdown",
				subtitle="A look at how frequently each class is used in Control",
				resize=True,
				)	
	graph.width = "$('#"+graph.divTitle+"').width()"
	graph.height = '450'

	x = groupByClass.groups.keys()
	y = [len(groupByClass.get_group(key))/float(len(data)) for key in x]


	graph.add_serie(y=y, x=x)
	graph.create_y_axis("yAxis", "Frequency", format=".2%")
	graph.create_x_axis("xAxis", "Class")
	
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



def objectivesByMap(data):
	"""
	Create the graph that shows the average number of objectives winning teams capture per game versus losing teams.

	:param data:	the data from teamData.csv
	"""
	logger.info("Building objectives completed per winner and loser")

	groupedByMapStanding = data.groupby(['refrencedId', 'standing'])

	victoryToString ={0:"Winners",1:"Losers"}
	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapStanding.groups.keys()}

	"""objectivesCompleted = [{'key':victoryToString[v], 
						'values': [{
							'x': mapDict[map],
							'y': float(groupedByMapStanding.get_group((map, v))['objectivesCompleted'].mean())
						} for map, _ in groupedByMapStanding.groups.keys()]
					}for v in victoryToString.keys()]

	graph = destinyPlot(objectivesCompleted, 
						"Objectives Completed by Winner and Loser on each Map", 
						"objectivesCompleted",
						FULL_PLOT_HTML_DIRECTORY,
						"Look at how many objectives winning teams on average completed in comparison to losing teams.",
						dataFilePath = FULL_PLOT_JSON_DIRECTORY,
						jsFilePath = FULL_PLOT_JS_DIRECTORY,
						)
	"""
	graph = lineChart(name="objectivesByMap", x_is_date=False)
	x = mapDict.values()
	ySeries = [{"name":victoryToString[v], "data": float(groupedByMapStanding.get_group((map, v))['objectivesCompleted'].mean())} for map,v in groupedByMapStanding.groups.keys()]  

	for series in ySeries:
		graph.add_serie(y=series['data'], x=x, name=series['name'])

	graph.buildContent()
	with open(os.path.join(FULL_PLOT_JS_DIRECTORY, "objectivesComplete.js")) as f:
		f.write(graph.htmlcontent)

	#write to html file
	template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
	template_values = {
		'destinyGraph': graph.__dict__,
	}
	output = template.render(template_values)

	with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,graph.name), 'w') as f:
		f.write(output)

	
def averageKillsPerMinute(data):
	"""
	Build a graph showing the average kills per minute on each map.
	"""
	logger.info("Average Kills Per Minute")

	groupedByMap = data.groupby("refrencedId")

	mapDict = {h:destiny.getMapName(h) for h in groupedByMap.groups.keys()}

	groupedByMap = data.groupby(("refrencedId","gameId"))

	totalKillsOnEachMap = {}
	totalTimeOnEachMap = {}

	for map, game in groupedByMap.groups.keys():
		totalKillsOnEachMap[mapDict[map]] = totalKillsOnEachMap.get(mapDict[map],0.0) + groupedByMap.get_group((map,game))['kills'].sum()
		totalTimeOnEachMap[mapDict[map]] = totalTimeOnEachMap.get(mapDict[map],0.0) + groupedByMap.get_group((map,game))['activityDurationSeconds'].max()

	print(totalKillsOnEachMap)
	print(totalTimeOnEachMap)

	"""averageKillsPerMinute = {"key":"averageKillsPerMinute",
							"values": [{
										"x":mapDict[map],
										"y":float(((groupedByMap.get_group(map)['kills']/groupedByMap.get_group(map)['activityDurationSeconds']) *60).mean())
									}for map in groupedByMap.groups.keys()]
							}"""


	graph = discreteBarChart(
				name="KillsPerMinute",
				key= 'KillsPerMinute',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				#use_interactive_guideline = True,
				title="Kills Per Minute on Each Map",
				resize=True,
				margin_bottom = 100,
				)

	graph.width = "$('#"+graph.divTitle+"').width()"
	y = [(float(totalKillsOnEachMap[map])/totalTimeOnEachMap[map]) *60.0 for map in sorted(list(mapDict.values()))]
	x = sorted(list(mapDict.values()))

	graph.add_serie(x=x, y=y, name="Kills Per Minute")
	graph.create_y_axis("yAxis", "Kills Per Minute", format=".3f")
	graph.create_x_axis("xAxis", "Map Name", extras={"rotateLabels":-25})
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


	"""

	#totalKillsOnEachMap = {map:groupedByMap.get_group(map)['kills'].sum() for map in groupedByMap.groups.keys()}
	#totalTimeOnEachMap = {map:groupedByMap.get_group(map)['activityDurationSeconds'].sum() for map in groupedByMap.groups.keys()}
	#y = [float(((groupedByMap.get_group(map)['kills']/groupedByMap.get_group(map)['activityDurationSeconds']) *60 * len(groupedByMap.get_group(map))).mean() )
	#								for map in groupedByMap.groups.keys()]

	averageKillsPerMinute = {"key":"averageKillsPerMinute",
								"values":[{
									"x":x,
									"y":y,
								}]
							}
	graph = destinyPlot(averageKillsPerMinute, 
				"Average Kills Per Minute on Each Map", 
				"mapAverageKillsPerMinute",
				FULL_PLOT_HTML_DIRECTORY,
				"A look at how many kills occur each minute on each map",
				dataFilePath = FULL_PLOT_JSON_DIRECTORY,
				jsFilePath = FULL_PLOT_JS_DIRECTORY,
				plotText="This plot attempts to show that certain maps have a faster style of gameplay than others."
				)
	"""

def quitRateByKillsPerMinute(data):
	logger.info("Quit Rate By Kills Per Minute")
	groupedByMap = data.groupby("refrencedId")

	mapDict = {h:destiny.getMapName(h) for h in groupedByMap.groups.keys()}

	groupedByMap = data.groupby(("refrencedId","gameId"))

	totalKillsOnEachMap = {}
	totalTimeOnEachMap = {}

	for map, game in groupedByMap.groups.keys():
		totalKillsOnEachMap[mapDict[map]] = totalKillsOnEachMap.get(mapDict[map],0.0) + groupedByMap.get_group((map,game))['kills'].sum()
		totalTimeOnEachMap[mapDict[map]] = totalTimeOnEachMap.get(mapDict[map],0.0) + groupedByMap.get_group((map,game))['activityDurationSeconds'].max()

	groupedByMap = data.groupby("refrencedId")

	quitRateByMap = [{"map":mapDict[map], "quitRate":1.0 - (groupedByMap.get_group(map)['completed'].sum()/float(len(groupedByMap.get_group(map))))} for map in groupedByMap.groups.keys()]
	killsPerMinute = [{"map":map,"kills":(float(totalKillsOnEachMap[map])/totalTimeOnEachMap[map]) *60.0} for map in list(mapDict.values())]

	quitRateDF = pd.DataFrame.from_records(quitRateByMap)
	quitRateDF['map'] = quitRateDF['map'].astype(str)
	quitRateDF.index = quitRateDF['map']
	del(quitRateDF['map'])
	killsPerMinuteDF = pd.DataFrame.from_records(killsPerMinute)
	killsPerMinuteDF['map'] = killsPerMinuteDF['map'].astype(str)
	killsPerMinuteDF.index = killsPerMinuteDF['map']

	quitRateByKillsPerMinute = pd.concat([quitRateDF, killsPerMinuteDF], axis=1)
	quitRateByKillsPerMinute.sort(['kills'], ascending=[True], inplace=True)

	killsAsIndex = pd.DataFrame(quitRateByKillsPerMinute)
	killsAsIndex.index = killsAsIndex['kills']

	graph = scatterChart(
				name="quitRateByKillsPerMinute",
				key= 'quitRateByKillsPerMinute',
				js_path = "javascripts",
				html_path = FULL_PLOT_HTML_DIRECTORY,
				#use_interactive_guideline = True,
				title="Quit Rate By Kills Per Minute on Each Map",
				subtitle = "A look at how kills per minute impacts quit rate",
				resize=True,
				height = 450,
				margin_bottom=50,
				xOrdinalValues = killsAsIndex['map'].to_dict(),
				plotText = "The x-axis displays the map name but it is sorted by increasing kills per minute. \
							The point of this graph is to show that as the kills per minute increases, the quit rate generally decreases."
		)
	graph.width = "$('#"+graph.divTitle+"').width()"

	extra_serie = {"tooltip":{"y_start":"Quit Rate: ", "y_end":""}}
	graph.add_serie(x=quitRateByKillsPerMinute['kills'].values, y=quitRateByKillsPerMinute['quitRate'].values, name="Quit Rate", extra=extra_serie)
	graph.create_y_axis("yAxis", "Quit Rate", format=".2%")
	graph.create_x_axis("xAxis", "Kills Per Minute", tickValues = list(quitRateByKillsPerMinute['kills'].values), 
							format="function(d){return xOrdinal[d];}", custom_format = True, extras={"rotateLabels":-25})
	graph.buildcontent()

	print('GRAPH: {0}'.format(graph.__dict__))


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




def getWeaponRatiosByMap(data):
	"""
	Build the graph that shows the usage of each weapon type on each map

	:param data:	the data from teamData.csv
	"""
	logger.info("Building weapon ratios per map")
	weaponColumns = [c for c in data.columns if 'weapon' in c and 'Heavy' not in c and 'Secondary' not in c and 'Primary' not in c]
	groupedByMap = data.groupby('refrencedId')

	mapDict = {h:destiny.getMapName(h) for h in groupedByMap.groups.keys()}

	weaponRatios = {}
	weaponRatios = [{'key':c, 'values': [{'x':mapDict[map], 
							'y': float(groupedByMap.get_group(map)[c].sum())/groupedByMap.get_group(map)['kills'].sum()} for map in groupedByMap.groups.keys()]
					}for c in weaponColumns]

	graph = destinyPlot(weaponRatios, 
					"Weapon Breakdown by Map", 
					"weaponBreakdown",
					FULL_PLOT_HTML_DIRECTORY,
					"A look at how frequently weapon types are used on each map",
					)


def quittingByMap(data):
	"""
	Build the graph that looks at the quit rate by team on each map

	:param data:	the data from teamData.csv
	"""
	logger.info("Building quitting rate per map by team")
	teamKeys = [16, 17]
	teamKeysToTitles = {16:'Alpha', 17:"Bravo"}

	data = data[(data['team'] == 16) | (data['team'] == 17)]
	groupedByMapTeam = data.groupby(['refrencedId', 'team'])

	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapTeam.groups.keys()}

	quittingByMap = [{
						'key': teamKeysToTitles[team],
						'values': [{
									'x':mapDict[map],
									'y': 1.0 - (groupedByMapTeam.get_group((map, team))['completed'].sum()/float(len(groupedByMapTeam.get_group((map,team))))),
									} for map,_ in groupedByMapTeam.groups.keys() if (map,team) in groupedByMapTeam.groups.keys()]
					} for team in teamKeys]
	
	graph = destinyPlot(quittingByMap, 
					"Quitting Rate by Map for each Team", 
					"quittingByMap",
					FULL_PLOT_HTML_DIRECTORY,
					"A look at how often players from each team quit on each map",
					plotText="NOTE: stacking this graph does not give an accurate overall quit rate.  The overall quit rates are likely closer to half of the stacked value."
					)

def neutralizedVersusCaptured(data):
	logger.info("Building neutralizedVersusCaptured")
	groupedByMapStanding = data.groupby(['refrencedId', 'standing'])

	victoryToString ={0:"Winners",1:"Losers"}
	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapStanding.groups.keys()}

	objectivesCompleted = [{'key':victoryToString[v], 
						'values': [{
							'x': mapDict[map],
							'y': float((groupedByMapStanding.get_group((map, v))['objectivesCompleted']/groupedByMapStanding.get_group((map,v))['zonesNeutralized']).replace([np.inf,-np.inf],0).mean())
						} for map, _ in groupedByMapStanding.groups.keys() if (map,v) in groupedByMapStanding.groups.keys()]
					}for v in victoryToString.keys()]

	graph = destinyPlot(objectivesCompleted, 
						"Zones Captured/Neutralized by Winner and Loser on each Map", 
						"objectivesRatio",
						FULL_PLOT_HTML_DIRECTORY,
						"Look at how a team's ability to effeciently capture points impacts victory",
						)

def dominationByMap(data):
	logger.info("Building domination kills for each team by map")
	groupedByMapStanding = data.groupby(['refrencedId', 'standing'])

	victoryToString ={0:"Winners",1:"Losers"}
	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapStanding.groups.keys()}

	dominationKills = [{'key':victoryToString[v], 
						'values': [{
							'x': mapDict[map],
							'y': float(groupedByMapStanding.get_group((map, v))['dominationKills'].mean())
						} for map, _ in groupedByMapStanding.groups.keys()]
					}for v in victoryToString.keys()]
	graph = destinyPlot(dominationKills, 
				"Average Number of Domination Kills per Team", 
				"dominationKills",
				FULL_PLOT_HTML_DIRECTORY,
				"A look at how domination kills affect victory",
				plotText = "This plot was created by grouping the dataframe by map and then by standing" +
								"It then takes the average number of <strong>domination kills</strong> that all winning teams had on that map, and does the same for losing teams."+
								"Domnination kills are obtained when a player gets a kill and their team controls all zones.",
				)

	print(graph.__dict__)

	#with open(os.path.join('..','gh-pages', 'datafiles', 'dominationKills.json'), 'w') as f:
	#	json.dump(dominationKills, f)

def victoryByMapAndTeam(data):
	logger.info("Building victory by map and team")
	teamKeys = [16, 17]

	teamKeysToTitles = {16:'Alpha', 17:"Bravo"}

	groupedByMapTeam = data.groupby(['refrencedId', 'team'])

	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapTeam.groups.keys()}

	victoryByMap = [{
						'key': teamKeysToTitles[team],
						'values': [{
									'x':mapDict[map],
									'y': 1.0 - (groupedByMapTeam.get_group((map, team))['standing'].sum()/float(len(groupedByMapTeam.get_group((map,team))))),
									} for map,_ in groupedByMapTeam.groups.keys() if (map,team) in groupedByMapTeam.groups.keys()]
					} for team in teamKeys]
	
	graph = destinyPlot(victoryByMap, 
			"Victory Rate for each Team on each Map", 
			"victoryByMap",
			FULL_PLOT_HTML_DIRECTORY,
			"A look at how each team performs on a given map",
			)



	#with open(os.path.join('..','gh-pages', 'datafiles', 'victoryByMap.json'), 'w') as f:
	#	json.dump(victoryByMap, f)

def weaponsByClass(data):
	logger.info("Building weapons per class")
	data = data[data['characterClass'] != '0']
	groupByClass = data.groupby(['characterClass'])
	weaponColumns = [c for c in data.columns if 'weapon' in c and 'Heavy' not in c and 'Secondary' not in c and 'Primary' not in c]

	weaponRatios = [{'key':w, 
					'values': [{
								'x': c, 
								'y': float(groupByClass.get_group(c)[w].sum())/groupByClass.get_group(c)['kills'].sum()
							} for c in groupByClass.groups.keys()]
					}for w in weaponColumns]

	graph = destinyPlot(weaponRatios, 
			"Weapon Usage by Class", 
			"weaponByClass",
			FULL_PLOT_HTML_DIRECTORY,
			"A breakdown of which weapon types each class uses",
			)

def orbsGeneratedVersusSuperKills(data):
	logger.info("Graph to compare each class and their ability to produce orbs per super kill")

	data = data[data['characterClass'] != '0']
	groupByClass = data.groupby("characterClass")

	orbsVsSuper = [{'key': 'Classes',
					'values': [{
							'x' : c,
							'y' : float(groupByClass.get_group(c)['orbsDropped'].sum()/(groupByClass.get_group(c)['weaponKillsSuper'] + groupByClass.get_group(c)['weaponKillsRelic']).sum())
						} for c in groupByClass.groups.keys()]
					}]
	graph = destinyPlot(orbsVsSuper, 
						"Orb Generated per Super Kill for each Class",
						"orbsVsSuper",
						FULL_PLOT_HTML_DIRECTORY,
						"A look at each class's ability to produce orbs",
						)

def weaponPairings(data, location=FULL_PLOT_HTML_DIRECTORY):
	logger.info("Graph to show frequency of weapon pairings")

	#data = data[(data['PrimaryWeapon'] != 'None') & (data['SecondaryWeapon'] != 'None')]

	groupByPrimary = data.groupby(["PrimaryWeapon",'SecondaryWeapon'])
	secondaryColumns = ['FusionRifle', 'Sniper', 'SideArm', 'Shotgun', 'None']
	primaryColumns = ['PulseRifle','HandCannon', 'ScoutRifle', 'AutoRifle', 'None']

	total = len(data)

	weaponPairingsGlobal = [{'key':s,
						'values': [{
							'x' : p,
							'y': float(len(groupByPrimary.get_group((p,s))))/total
						} for p in primaryColumns if (p,s) in groupByPrimary.groups.keys()]
					} for s in secondaryColumns]

	#figure out which key combo was not present and give it a series too
	#weaponPairingsGlobal

	graph = destinyPlot(weaponPairingsGlobal, 
						"Frequency of Primary/Secondary Weapon Pairings",
						"weaponPairings",
						location,
						"A look at how primary and secondary weapons are paired together",
						plotText = 'This graph shows  how frenquently weapons are paired together over the <strong>entire</strong> set of data.  '+
									'The x-axis is primary weapons, and the colors represent different secondary weapons.  '+
									'When hovering over a bar, you should read the frequency as: <em>y</em> percent of players use <em>x</em> and <em>color</em> combo.  ' +
									'For example, 16 percent of players use a Hand Cannon and Shotgun combo.  ' +
									'<strong>None</strong> is for players who go through an entire game without using a primary weapon, but do have registered secondary weapon kills.  '
						)

	groupByPrimary = data.groupby("PrimaryWeapon")
	weaponPairingsLocal = [{'key':s,
						'values': [{
							'x' : p,
							'y': float(len(groupByPrimary.get_group(p)[groupByPrimary.get_group(p)['SecondaryWeapon'] == s]))/len(groupByPrimary.get_group(p))
						} for p in primaryColumns if p in groupByPrimary.groups.keys()]
					} for s in secondaryColumns]
	graph = destinyPlot(weaponPairingsLocal, 
						"Frequency of Secondary Weapons with each Primary Weapons",
						"primarySecondary",
						location,
						"A look at the disctrubtion of secondary weapons amongs primary weapons",
						dataFilePath = "datafiles",
						jsFilePath = "javascripts",
						plotText = 'This graph shows how often each secondary weapon is paired with a primary weapon.  '+
									'It is looking at the distribution within each primary weapon, not over the entire set of data.  '+
									'If you stack the bars on top of one another, each x-axis tick would go up to 1.00 (or 100%).  '+
									'When hovering over a bar, you should read the result as: <em>y</em> percent of players who use <em>x</em> pair it with <em>color</em>.  ' +
									'For example, 46 percent of players who use Hand Cannons pair it with Shotguns.'
						)



def scorePerKill(data):
	logger.info("Building score per kill")
	groupedByMapStanding = data.groupby(['refrencedId', 'standing'])

	victoryToString ={0:"Winners",1:"Losers"}
	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapStanding.groups.keys()}

	averageScorePerKill = [{'key':victoryToString[v], 
						'values': [{
							'x': mapDict[map],
							'y': float(groupedByMapStanding.get_group((map, v))['averageScorePerKill'].mean())
						} for map, _ in groupedByMapStanding.groups.keys()]
					}for v in victoryToString.keys()]
	graph = destinyPlot(averageScorePerKill, 
			"Average Score Per Kill for Winners and Losers", 
			"averageScorePerKill",
			FULL_PLOT_HTML_DIRECTORY,
			"A look at how average score per kill affects victory",
			)


def getSniperRatiosByVictory(data):
	logger.info("Building sniper ratio victory")
	victoryToString ={0:"Winners",1:"Losers"}
	groupedByMapStanding = teamData.groupby(['refrencedId', 'standing'])

	mapDict = {h[0]:destiny.getMapName(h[0]) for h in groupedByMapStanding.groups.keys()}


	sniperRatios = [{'key':victoryToString[v], 
						'values': [{
							'x': mapDict[map],
							'y': float(groupedByMapStanding.get_group((map, v))['weaponKillsSniper'].sum()) / groupedByMapStanding.get_group((map,v))['kills'].sum()
						} for map, _ in groupedByMapStanding.groups.keys()]
					}for v in victoryToString.keys()]

	graph = destinyPlot(sniperRatios, 
			"Sniper rifle usage rate by winners and losers on each map", 
			"sniperRatioRate",
			FULL_PLOT_HTML_DIRECTORY,
			"A look at how using sniper rifles affects victory on a given map",
			)
def classLevelVictory(data):
	"""
	Build json file for a graph that displays how frequent a class wins based on their level
	"""
	logger.info("Building victory rates for each class by character level")
	data = data[data['characterClass'] != '0']
	data = data[data['characterLevel'] != 0]

	victoryToString = {0:"Winners", 1:"Losers"}

	groupByClass = data.groupby(['characterClass', 'characterLevel'])


	characterKeys = ['Warlock', 'Titan', 'Hunter']
	levelKeys = list(set([level for _,level in groupByClass.groups.keys()]))

	victoryByClassLevel = [{'key':character, 
							'values': [{
								'x': level,
								'y': 1.0 - (float((groupByClass.get_group((character, level))['standing'].sum()))/len(groupByClass.get_group((character,level))))
							} for  level in levelKeys if (character,level) in groupByClass.groups.keys()]
						}for character in characterKeys]

	graph = destinyPlot(victoryByClassLevel, 
			"Victory Rate for Each Class versus Character Level", 
			"victoryByClassLevel",
			FULL_PLOT_HTML_DIRECTORY,
			"A look at how characterLevel affects victory rate for each class",
			jsTemplateName = "javascriptLineTemplate.js",
			)


	#with open(os.path.join('..','gh-pages', 'datafiles', 'characterClassVictory.json'), 'w') as f:
	#	json.dump(victoryByClassLevel, f)
	return victoryByClassLevel

def predictedVsActual(actual, predicted):
	"""
	Build the json object for a graph that displays each team's actual victory and defeat by game, and then the predicted probability of their victory
	"""

	victoryToString ={0:"Winners", 1:"Losers"}
	teamToString = {16: 'Alpha', 17:'Bravo'}

	actual_groupedByTeam = actual.groupby(['team', 'gameId'])

	teamKeys = [16, 17]
	gameIdKeys = list(set([gameId for _,gameId in actual_groupedByTeam.groups.keys()]))

	logger.info("Formatting actual data")

	actual_json = [{'key':teamToString[team], 
							'values': [{
								'x': float(gameId),
								'y': int(actual_groupedByTeam.get_group((team,gameId))['standing'])
							} for gameId in gameIdKeys if (team,gameId) in actual_groupedByTeam.groups.keys()]
						 } for team in teamKeys]

	logger.info("Formatting predicted data")
	predicted_groupedByTeam = predicted.groupby(['team','gameId'])
	gameIdKeys = list(set([gameId for _,gameId in actual_groupedByTeam.groups.keys()]))

	predicted_json = [{'key':teamToString[team] +' Probability Of Victory',
							'values': [{
								'x': float(gameId),
								'y': float(predicted_groupedByTeam.get_group((team,gameId))['probabilityOfVictory'])
							} for gameId in gameIdKeys if (team,gameId) in predicted_groupedByTeam.groups.keys()]
						 } for team in teamKeys]

	return (actual_json + predicted_json)

def victoryRateByWeapon(teamData):
	logger.info("Building weapon ratios per map and victory")
	weaponColumns = [c for c in data.columns if 'weapon' in c and 'Heavy' not in c and 'Secondary' not in c and 'Primary' not in c]
	groupedByMap = data.groupby(['refrencedId','standing'])

	victoryToString ={0:"W",1:"L"}
	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMap.groups.keys()}

	weaponRatios = {}
	weaponRatios = [{'key':c, 
					'values': [{
						'x':mapDict[map], 
						'y':c[len("weaponKills"): ] +"_" + victoryToString[standing],
						'size': float(groupedByMap.get_group((map,standing))[c].sum())/groupedByMap.get_group((map,standing))['kills'].sum()
						} for map, standing in groupedByMap.groups.keys()]
					}for c in weaponColumns]

	graph = destinyPlot(weaponRatios, 
					"Weapon Breakdown by Map and Victory", 
					"weaponAndVictoryBreakdown",
					FULL_PLOT_HTML_DIRECTORY,
					"A look at how winning and losing teams use weapons differently",
					jsTemplateName= "javascriptScatterTemplate.js"
					)

if __name__ == "__main__":
	#teamData = pd.read_csv("datafiles/teamData.csv")
	data = pd.read_csv("datafiles/data.csv")

	weaponPairings(data)

	"""
	getWeaponRatiosByMap(teamData)
	
	#objectivesByMap(teamData)
	
	quittingByMap(data)
	victoryByMapAndTeam(teamData)
	weaponsByClass(data)
	scorePerKill(teamData)
	getSniperRatiosByVictory(teamData)
	classLevelVictory(data)
	victoryRateByWeapon(teamData)
	neutralizedVersusCaptured(teamData)
	dominationByMap(teamData)
	orbsGeneratedVersusSuperKills(data)
	averageKillsPerMinute(data)
	quitRateByKillsPerMinute(data)
	classUsage(data)
	"""


	#write to index html file
	template = jinja2_env.get_template(os.path.join('index.html'))
	template_values = {
		'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
	}
	output = template.render(template_values)

	with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
		f.write(output.encode('ascii', 'ignore'))
		#f.write(output)
