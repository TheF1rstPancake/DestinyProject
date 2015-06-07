"""
Split a dataset built from the Destiny Platform REST API into a smaller subset of teams.
"""
import pandas as pd
import logging
import sys
import argparse

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(ch)

def groupByTeam(dataFileName):
	"""
    Given a datafile (created by :func:`DestinyBlogProject.runBlogProject`), group the data into team vectors
    At the end, we expect each game to have two teams assocaited with it.
    This funtion also creates features to define each team based on the attributes of the players of that team
    """
	data = pd.read_csv(dataFileName)

	#the teams will be 16 (alpha) and 17 (bravo)
	#NOTE: there is also team -1, which means something went wrong with them
	#the only pattern I found was that the teamScore of the players equals 0
	#this could mean the game ended due to some unknown reason
	#or that the player was disconnected.  
	#We probably don't want to include these players when building our team based data since they don't fit the mold
	#everyone with a team of -1 was given a standing of 0 (victory)
	data = data[data['team'] != -1]

	#setup the output frame
	outData = pd.DataFrame()

	#group the data frame into individual gamse
	groupedByGame = data.groupby("gameId")

	#loop through each game and build the a dictionary for each team
	#then take that list of dicitonaries and create a dataframe
	#and add it to the output dataframe
	#at the end we should have a nice rectangular matrix
	totalGames = len(groupedByGame)
	count = 0
	for game in groupedByGame.groups.keys():
		count = count + 1
		logger.info("Building team data for {0}. {1} out of {2}".format(game,count,totalGames))
		gameData = groupedByGame.get_group(game)
		teams = gameData.groupby("team")

		teamBreakdown =[]
		for t in teams.groups.keys():
			teamDict = {}
			teamData = teams.get_group(t)

			teamDict['gameId'] = game
			teamDict['team'] = t
			teamDict['date'] = teamData['date']

			teamDict['standing'] = teamData['standing'].values[0]
			teamDict['killsDeathsAssists'] = teamData['killsDeathsAssists'].mean()
			teamDict['killsDeathsRatio'] = teamData['killsDeathsRatio'].mean()
			teamDict['averageScorePerKill'] = teamData['averageScorePerKill'].mean()
			teamDict['assists'] = teamData['assists'].sum()
			teamDict['assistsAvg'] = teamData['assists'].mean()
			teamDict['kills'] = teamData['kills'].sum()
			
			teamDict['hunters'] = len(teamData[teamData['characterClass'] == "Hunter"])
			teamDict['titans'] = len(teamData[teamData['characterClass'] == "Titan"])
			teamDict['warlocks'] = len(teamData[teamData['characterClass'] == "Warlock"])
			
			teamDict['combatRating'] = teamData['combatRating'].mean()
			teamDict['combatRatingStd'] = teamData['combatRating'].std()
			
			teamDict['characterLevel'] = teamData['characterLevel'].mean()
			teamDict['characterLevelStd'] = teamData['characterLevel'].std()

			teamDict['numberOfFireTeams'] = len(teamData['fireTeamId'].unique())
			
			teamDict['refrencedId'] = teamData['refrencedId'].values[0]
			teamDict['orbsDropped'] = teamData['orbsDropped'].sum()
			teamDict['orbsGathered'] = teamData['orbsGathered'].sum()
			teamDict['orbsGatheredDroppedRatio'] = float(teamDict['orbsGathered'])/teamDict['orbsDropped']
			
			teamDict['players'] = len(teamData)
			teamDict['teamScore'] = teamData['teamScore'].max()
			teamDict['scoreStd'] = teamData['score'].std()
			teamDict['scoreAvg'] = teamData['score'].mean()
			
			teamDict['precisionKillsAvg'] = teamData['precisionKills'].mean()
			teamDict['precisionKills'] = teamData['precisionKills'].sum()
			
			teamDict['averageLifespan'] = teamData['averageLifespan'].mean()
			teamDict['averageLifespanStd'] = teamData['averageLifespan'].std()

			teamDict['defensiveKills'] = teamData['defensiveKills'].sum()
			teamDict['defensiveKillsAvg'] = teamData['defensiveKills'].mean()
			teamDict['defensiveKillsStd'] = teamData['defensiveKills'].std()

			teamDict['offensiveKills']  = teamData['offensiveKills'].sum()
			teamDict['offensiveKillsAvg'] = teamData['offensiveKills'].mean()
			teamDict['offensiveKillsStd'] = teamData['offensiveKills'].std()

			teamDict['objectivesCompleted'] = teamData['objectivesCompleted'].sum()
			teamDict['objectivesCompletedAvg'] = teamData['objectivesCompleted'].mean()
			teamDict['zonesNeutralized'] = teamData['zonesNeutralized'].sum()

			#get the number of exotic and legendary weapons that a team used
			teamDict['numberOfExotics'] = len(teamData.ix[teamData['mostUsedWeapon1Tier'] == 'Exotic', 'mostUsedWeapon1Tier']) + len(teamData.ix[teamData['mostUsedWeapon2Tier'] == 'Exotic', 'mostUsedWeapon2Tier'])

			teamDict['numberOfLegendaries'] = len(teamData.ix[teamData['mostUsedWeapon1Tier'] == 'Legendary', 'mostUsedWeapon1Tier']) + len(teamData.ix[teamData['mostUsedWeapon2Tier'] == 'Legendary', 'mostUsedWeapon2Tier'])

			weaponKeys = [c for c in list(teamData.columns) if 'weapon' in c]
			
			for w in weaponKeys:
				teamDict[w] = teamData[w].sum()

			teamDict['weaponKillsHeavy'] = teamData['weaponKillsMachinegun'].sum() + teamData['weaponKillsRocketLauncher'].sum()
			teamDict['weaponKillsPrimary'] = teamData['weaponKillsPulseRifle'].sum() + teamData['weaponKillsAutoRifle'].sum() + teamData['weaponKillsScoutRifle'].sum() +teamData['weaponKillsHandCannon'].sum()
			teamDict['weaponKillsSecondary'] = teamData['weaponKillsShotgun'].sum() + teamData['weaponKillsSniper'].sum() +teamData['weaponKillsFusionRifle'].sum() + teamData['weaponKillsSideArm'].sum()

			teamDict['longestKillSpree'] = teamData['longestKillSpree'].mean()
		
			teamDict['highestScore'] = teamData['score'].max()
			teamDict['lowestScore'] = teamData['score'].min()	

			teamDict['dominationKills'] = teamData['dominationKills'].sum()

			#add to list
			teamBreakdown.append(teamDict)

		#add a few more features that involve comparing the two teams
		#Team with highest scoring player
		if len(teamBreakdown) == 1:
			teamBreakdown[0]['hasHighestScoringPlayer'] = 1
			teamBreakdown[0]['hasLowestScoringPlayer'] = 1	
		else:
			if teamBreakdown[0]['highestScore']	> teamBreakdown[1]['highestScore']:
				teamBreakdown[0]['hasHighestScoringPlayer'] = 1
				teamBreakdown[1]['hasHighestScoringPlayer'] = 0	

			elif teamBreakdown[0]['highestScore'] < teamBreakdown[1]['highestScore']:
				teamBreakdown[0]['hasHighestScoringPlayer'] = 0
				teamBreakdown[1]['hasHighestScoringPlayer'] = 1
			else:
				teamBreakdown[0]['hasHighestScoringPlayer'] = 0
				teamBreakdown[1]['hasHighestScoringPlayer'] = 0

			#mark team with lowest scoring player
			if teamBreakdown[0]['lowestScore']	> teamBreakdown[1]['lowestScore']:
				teamBreakdown[0]['hasLowestScoringPlayer'] = 0
				teamBreakdown[1]['hasLowestScoringPlayer'] = 1	

			elif teamBreakdown[0]['lowestScore'] < teamBreakdown[1]['lowestScore']:
				teamBreakdown[0]['hasLowestScoringPlayer'] = 0
				teamBreakdown[1]['hasLowestScoringPlayer'] = 1
			else:
				teamBreakdown[0]['hasLowestScoringPlayer'] = 0
				teamBreakdown[1]['hasLowestScoringPlayer'] = 0

		team_df = pd.DataFrame.from_records(teamBreakdown)
		outData = pd.concat([outData,team_df], ignore_index=True)
	return outData

def predictWinners(datafile):
	"""
	Given a datafile with 4 columns:
		index (id)
		gameId
		standing
		team
	Predict who wins and who looses a game.
	"""

	#load data
	predictions = pd.read_csv(datafile)

	#group by game id
	groupedByGame = predictions.groupby("gameId")

	#for each game, predict one winner and one loser
	#UNLESS there is only one team, in which case they are automatically assinged as the winner (standing -> 0 is winner, 1 is loser)
	for gameId in groupedByGame.groups.keys():
		group  = groupedByGame.get_group(gameId)
		print(group)
		if len(group) == 1:
			predictions.ix[predictions['id'] == group['id'].values[0],'standing'] = 0
		else:
			if group['standing'].values[0] > group['standing'].values[1]:
				predictions.ix[predictions['id'] == group['id'].values[0], 'standing'] = 1
				predictions.ix[predictions['id'] == group['id'].values[1], 'standing'] = 0
			else:
				predictions.ix[predictions['id'] == group['id'].values[0], 'standing'] = 0
				predictions.ix[predictions['id'] == group['id'].values[1], 'standing'] = 1

	predictions.to_csv("predictions_binomial.csv")
			
if __name__=="__main__":
	print("Hello World")

	parser = argparse.ArgumentParser()
	parser.add_argument("--datafile", default="data.csv")
	parser.add_argument("--outfile", default="teamData.csv")

	args = parser.parse_args()

	data = groupByTeam(args.datafile)
	data.to_csv(args.outfile)
