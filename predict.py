from sklearn.feature_extraction import text
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, f_regression
from math import sqrt

import pandas as pd
import numpy as np

def predictWinners(predictions):
	"""
	Given a datafile with 4 columns:
		index (id)
		gameId
		standing
		team
	Predict who wins and who looses a game.
	"""

	#load data
	#predictions = pd.read_csv(datafile)

	print("Cleaning data!")

	#group by game id
	groupedByGame = predictions.groupby("gameId")

	#for each game, predict one winner and one loser
	#UNLESS there is only one team, in which case they are automatically assinged as the winner (standing -> 0 is winner, 1 is loser)
	for gameId in groupedByGame.groups.keys():
		group  = groupedByGame.get_group(gameId)
		#print(group)
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
	return predictions


if __name__ == "__main__":
	#create training and testing datasets
	#just split the data in half
	teamData = pd.read_csv("teamData.csv")
	train = teamData.ix[0:len(teamData)/2, ]
	test = teamData.ix[(len(teamData)/2 + 1):len(teamData), ]

	#print train[[c for c in train.columns if c != "standing" and c!="date"].columns
 	features = ['characterLevel', 
				'combatRating',
				'combatRatingStd', 
				'killsDeathsRatio',
				'killsDeathsAssists', 
				'defensiveKills',
				'offensiveKills', 
				'objectivesCompleted', 
				'refrencedId',  
				'team',
				'hasHighestScoringPlayer', 
				'hasLowestScoringPlayer', 
				'numberOfFireTeams',
  				'weaponKillsHeavy',
  				'players',
  				'averageScorePerKill',
  				'longestKillSpree',
  				'dominationKills',
  				]

  	print(train[features].shape)
  	X_new = SelectKBest(f_regression).fit_transform(train[features], train['standing'])
 	print X_new.shape

	print("Building random forest!")  			
  	randomForest = RandomForestClassifier(n_estimators=200, )
  	randomForest.fit(train[features], train['standing'])
  
  	#predictions = randomForest.predict(test[features])
  	#get the probability that the team wins and that it loses
  	predictions = randomForest.predict_proba(test[features])
  	print(randomForest.classes_)
  	print(predictions[0:15])

  	submission = pd.DataFrame({"id":test.index.values, 
  		"standing":[i[1] for i in predictions], 
  		"gameId":test['gameId'],
  		"team":test['team'], 
  		"probabilityOfVictory":[i[0] for i in predictions]})

  	#given the probabilities of victory (and defeat) and turn those into 0s and 1s
  	submission = predictWinners(submission)

  	rms = sqrt(mean_squared_error(test['standing'], submission['standing']))

  	print("RMSE: {0}".format(rms))

  	submission.to_csv("submission.csv")