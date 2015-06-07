import pandas as pd 
import destinyPlatform as destiny 
import json
import os
import numpy as np
import jinja2


FULL_PLOT_HTML_DIRECTORY = os.path.join("..","gh-pages","fullPlots")
FULL_PLOT_JS_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "javascripts")
FULL_PLOT_JSON_DIRECTORY = os.path.join(FULL_PLOT_HTML_DIRECTORY, "datafiles")

PLOT_TEMPLATES = "plotTemplates"

jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader('plotTemplates'))

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
		with open(self.jsonFileLocation, 'w') as f:
			json.dump(data, f)

		#write to javascript file
		template = jinja2_env.get_template(os.path.join(jsTemplateName))
		template_values = {
			'destinyGraph':self.__dict__,
		}
		output = template.render(template_values)

		with open(self.javascriptFileLocation, 'w') as f:
			f.write(output)

		#write to html file
		template = jinja2_env.get_template(os.path.join('htmlTemplate.html'))
		template_values = {
			'destinyGraph': self.__dict__,
		}
		output = template.render(template_values)

		with open(self.htmlFileLocation, 'w') as f:
			f.write(output)

def objectivesByMap(data):
	print("Building objectives completed per winner and loser")

	groupedByMapStanding = data.groupby(['refrencedId', 'standing'])

	victoryToString ={0:"Winners",1:"Losers"}
	mapDict = {h:destiny.getMapName(h) for h,_ in groupedByMapStanding.groups.keys()}

	objectivesCompleted = [{'key':victoryToString[v], 
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

def getWeaponRatiosByMap(data):
	print("Building weapon ratios per map")
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
					dataFilePath = FULL_PLOT_JSON_DIRECTORY,
					jsFilePath = FULL_PLOT_JS_DIRECTORY,
					)

	return weaponRatios

def quittingByMap(data):
	print("Building quitting rate per map by team")
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
					dataFilePath = FULL_PLOT_JSON_DIRECTORY,
					jsFilePath = FULL_PLOT_JS_DIRECTORY,
					)


	#with open(os.path.join('..','gh-pages', 'datafiles', 'quittingByMap.json'), 'w') as f:
	#	json.dump(quittingByMap, f)

def neutralizedVersusCaptured(data):
	print("Building neutralizedVersusCaptured")
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
						dataFilePath = FULL_PLOT_JSON_DIRECTORY,
						jsFilePath = FULL_PLOT_JS_DIRECTORY,
						)

def dominationByMap(data):
	print("Building domination kills for each team by map")
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
				dataFilePath = FULL_PLOT_JSON_DIRECTORY,
				jsFilePath = FULL_PLOT_JS_DIRECTORY,
				)

	#with open(os.path.join('..','gh-pages', 'datafiles', 'dominationKills.json'), 'w') as f:
	#	json.dump(dominationKills, f)

def victoryByMapAndTeam(data):
	print("Building victory by map and team")
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
			dataFilePath = FULL_PLOT_JSON_DIRECTORY,
			jsFilePath = FULL_PLOT_JS_DIRECTORY,
			)



	#with open(os.path.join('..','gh-pages', 'datafiles', 'victoryByMap.json'), 'w') as f:
	#	json.dump(victoryByMap, f)

def weaponsByClass(data):
	print("Building weapons per class")
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
			dataFilePath = FULL_PLOT_JSON_DIRECTORY,
			jsFilePath = FULL_PLOT_JS_DIRECTORY,
			)
	#with open(os.path.join('..','gh-pages', 'datafiles', 'weaponsByClass.json'), 'w') as f:
	#	json.dump(weaponRatios, f)

def scorePerKill(data):
	print("Building score per kill")
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
			dataFilePath = FULL_PLOT_JSON_DIRECTORY,
			jsFilePath = FULL_PLOT_JS_DIRECTORY,
			)

	#with open(os.path.join('..','gh-pages', 'datafiles', 'averageScorePerKills.json'), 'w') as f:
	#	json.dump(averageScorePerKill, f)

def getSniperRatiosByVictory(data):
	print("Building sniper ratio victory")
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
			dataFilePath = FULL_PLOT_JSON_DIRECTORY,
			jsFilePath = FULL_PLOT_JS_DIRECTORY,
			)
	return sniperRatios

def classLevelVictory(data):
	"""
	Build json file for a graph that displays how frequent a class wins based on their level
	"""
	print("Building victory rates for each class by character level")
	data = data[data['characterClass'] != '0']
	data = data[data['characterLevel'] != 0]

	victoryToString = {0:"Winners", 1:"Losers"}

	groupByClass = data.groupby(['characterClass', 'characterLevel'])

	print("Formatting data")

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
			dataFilePath = FULL_PLOT_JSON_DIRECTORY,
			jsFilePath = FULL_PLOT_JS_DIRECTORY,
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

	print("Formatting actual data")

	actual_json = [{'key':teamToString[team], 
							'values': [{
								'x': float(gameId),
								'y': int(actual_groupedByTeam.get_group((team,gameId))['standing'])
							} for gameId in gameIdKeys if (team,gameId) in actual_groupedByTeam.groups.keys()]
						 } for team in teamKeys]

	print("Formatting predicted data")
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
	print("Building weapon ratios per map and victory")
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
					dataFilePath = FULL_PLOT_JSON_DIRECTORY,
					jsFilePath = FULL_PLOT_JS_DIRECTORY,
					jsTemplateName= "javascriptScatterTemplate.js"
					)

if __name__ == "__main__":
	teamData = pd.read_csv("teamData.csv")
	data = pd.read_csv("data.csv")
	getWeaponRatiosByMap(teamData)
	objectivesByMap(teamData)
	quittingByMap(data)
	victoryByMapAndTeam(teamData)
	weaponsByClass(data)
	scorePerKill(teamData)
	getSniperRatiosByVictory(teamData)
	classLevelVictory(data)
	victoryRateByWeapon(teamData)
	neutralizedVersusCaptured(teamData)
	dominationByMap(teamData)

	#write to index html file
	template = jinja2_env.get_template(os.path.join('index.html'))
	template_values = {
		'files': [ f for f in os.listdir(FULL_PLOT_HTML_DIRECTORY) if os.path.isfile(os.path.join(FULL_PLOT_HTML_DIRECTORY,f)) ]
	}
	output = template.render(template_values)

	with open(os.path.join(FULL_PLOT_HTML_DIRECTORY,'index.html'), 'w') as f:
		f.write(output.encode('ascii', 'ignore'))
		#f.write(output)
