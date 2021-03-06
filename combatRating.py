"""
Attempt to reverse engineer Bungie's Combat Rating metric
"""

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.feature_selection import chi2, f_regression, f_classif
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

from sklearn.svm import SVR

from math import sqrt

import destinyPlatform as destiny


def rSquaredForEachColumn(data, columns):
    values ={}
    for k in numeric_columns:
        yFeature="combatRating"
        regr = linear_model.RidgeCV([.01,.1,1])
        print('Fitting to {0}'.format(k))
        regr.fit(train[[k]], train[yFeature])

        # The coefficients

        values[k] = {"Coefficient": regr.coef_, "Alpha":regr.alpha_}
        
        # Prediciton
        prediction = regr.predict(test[[k]])

        # The mean square error
        values[k]["Residual sum of squares"]= np.mean((prediction - test[yFeature]) ** 2)    # Explained variance score: 1 is perfect prediction
        values[k]['Variance score']= regr.score(test[[k]], test[yFeature])
        values[k]['R-Squared']= r2_score(prediction,test[yFeature])
        values[k]['RMSE'] = sqrt(mean_squared_error(prediction, test[yFeature]))
    
    return pd.DataFrame(values).T

def derviedCRPrediction(data):
    for i in range(0,10):
        print("splitting data into test and train sets")
        seed = 17*i
        np.random.seed(seed)
        msk = np.random.rand(len(df)) < 0.8
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        numeric_columns = [c for c in df.select_dtypes(include=numerics).columns.values if 
            c not in ['combatRating','characterId','gameId','membershipId','fireTeamId','refrencedId', 'mode','completionReason', 'team', 'activityDurationSeconds'] 
            and "mostUsedWeapon" not in c and "weaponKills" not in c and "OfPlayer" not in c and "Weapon" not in c]

        print("NUMERIC_COLUMNS: {0}".format(len(numeric_columns)))

        KBest = SelectPercentile(f_regression, percentile=10)
        X_new = KBest.fit_transform(df[numeric_columns], df['combatRating'])
        featureList = pd.DataFrame(zip(numeric_columns, X_new), columns=['name','scores'])
        featureList['score'] = [i[0] for i in featureList['scores']]
        featureList['pvalue'] = [i[1] for i in featureList['scores']]

        features = df[[numeric_columns[i] for i in KBest.get_support(indices=True)]].columns.values

        print("TOP K FEATURES: {0}".format(features))
        print(sorted(zip(numeric_columns, KBest.scores_), key = lambda x: -x[1]))

        train = df[msk]
        test = df[~msk]
        #train = df.head(int(.8*len(df)))
        #test = df.tail(len(df)-len(train))
        print("TEST: {0}\nTRAIN: {1}".format(len(test), len(train)))

        
        # Create linear regression object
        regr = linear_model.RidgeCV(alphas=range(1,100))
        # Train the model using the training sets
        print("Fitting regression for alpha")
        yFeature = 'combatRating'
        regr.fit(train[features], train[yFeature])


        # The coefficients
        values[seed] = {"Coefficient": regr.coef_, "Alpha":regr.alpha_}
        
        # Prediciton
        prediction = regr.predict(test[features])

        # The mean square error
        values[seed]["Residual sum of squares"]= np.mean((prediction - test[yFeature]) ** 2)    # Explained variance score: 1 is perfect prediction
        values[seed]['Variance score']= regr.score(test[features], test[yFeature])
        values[seed]['R-Squared']= r2_score(prediction,test[yFeature])
        values[seed]['RMSE'] = sqrt(mean_squared_error(prediction, test[yFeature]))

def cleaning(dirty_df):
    df = dirty_df[dirty_df['combatRating'] > 0]

    if 'activityDurationSeconds' in df.columns:
        df['killsPerMinute'] = df['kills']/(df['activityDurationSeconds']/60)
    if 'kills' in df.columns and 'precisionKills' in df.columns:
        df['normalKills'] = df['kills'] - df['precisionKills']
    if 'completed' in df.columns:
        df['completed'] = abs(df['completed'] - 1)
    if 'standing' in df.columns:
        df['standing'] = abs(df['standing'] - 1)
    if 'place' in df.columns:
        df['rank'] = 1.0 - (df['place']/df['playerCount'])

    return df

def teamModel(df):
    values = {}
    yFeature = 'combatRating'

    features = []
    numeric_columns = ['teamScore','standing']
    KBest = None
    for i in range(0,1):
        print("splitting data into test and train sets")
        seed = 17*i
        np.random.seed(seed)
        msk = np.random.rand(len(df)) < 0.8

        features = numeric_columns

        train = df[msk]
        test = df[~msk]
        print("TEST: {0}\nTRAIN: {1}".format(len(test), len(train)))

        # Create linear regression object
        #regr = linear_model.RidgeCV(alphas=range(1,100))
        regr = linear_model.BayesianRidge()

        # Train the model using the training sets
        print("Fitting regression for alpha")
        regr.fit(train[features], train[yFeature])


        # The coefficients
        #values[seed] = {"Coefficient": regr.coef_, "Alpha":regr.alpha_}
        values[seed] = {"Coefficient":regr.coef_, 'Alpha':0}
        
        # Prediciton
        prediction = regr.predict(test[features])

        # The mean square error
        values[seed]["Residual sum of squares"]= np.mean((prediction - test[yFeature]) ** 2)    # Explained variance score: 1 is perfect prediction
        values[seed]['Variance score']= regr.score(test[features], test[yFeature])
        values[seed]['R-Squared']= r2_score(prediction,test[yFeature])
        values[seed]['RMSE'] = sqrt(mean_squared_error(prediction, test[yFeature]))

    return values, features

def ratioModel(df):
    values = {}
    yFeature = 'combatRating'

    features = []
    numeric_columns = ['ratioPrediction']
    KBest = None
    for i in range(0,1):
        print("splitting data into test and train sets")
        seed = 17*i
        np.random.seed(seed)
        msk = np.random.rand(len(df)) < 0.8

        features = numeric_columns

        train = df[msk]
        test = df[~msk]
        print("TEST: {0}\nTRAIN: {1}".format(len(test), len(train)))

        # Create linear regression object
        #regr = linear_model.RidgeCV(alphas=range(1,100))
        regr = linear_model.BayesianRidge()

        # Train the model using the training sets
        print("Fitting regression for alpha")
        regr.fit(train[features], train[yFeature])


        # The coefficients
        #values[seed] = {"Coefficient": regr.coef_, "Alpha":regr.alpha_}
        values[seed] = {"Coefficient":regr.coef_, 'Alpha':0}
        
        # Prediciton
        prediction = regr.predict(test[features])

        # The mean square error
        values[seed]["Residual sum of squares"]= np.mean((prediction - test[yFeature]) ** 2)    # Explained variance score: 1 is perfect prediction
        values[seed]['Variance score']= regr.score(test[features], test[yFeature])
        values[seed]['R-Squared']= r2_score(prediction,test[yFeature])
        values[seed]['RMSE'] = sqrt(mean_squared_error(prediction, test[yFeature]))

    return values, features



def scoreModel(df):
    values = {}
    yFeature = 'combatRating'

    features = []
    numeric_columns = ['completed', 'score','contribution','scoreStdRatio']
    KBest = None
    for i in range(0,1):
        print("splitting data into test and train sets")
        seed = 17*i
        np.random.seed(seed)
        msk = np.random.rand(len(df)) < 0.8

        features = numeric_columns

        train = df[msk]
        test = df[~msk]
        print("TEST: {0}\nTRAIN: {1}".format(len(test), len(train)))

        # Create linear regression object
        #regr = linear_model.RidgeCV(alphas=range(1,100))
        regr = linear_model.BayesianRidge()

        # Train the model using the training sets
        print("Fitting regression for alpha")
        regr.fit(train[features], train[yFeature])


        # The coefficients
        #values[seed] = {"Coefficient": regr.coef_, "Alpha":regr.alpha_}
        values[seed] = {"Coefficient":regr.coef_, 'Alpha':0}
        
        # Prediciton
        prediction = regr.predict(test[features])

        # The mean square error
        values[seed]["Residual sum of squares"]= np.mean((prediction - test[yFeature]) ** 2)    # Explained variance score: 1 is perfect prediction
        values[seed]['Variance score']= regr.score(test[features], test[yFeature])
        values[seed]['R-Squared']= r2_score(prediction,test[yFeature])
        values[seed]['RMSE'] = sqrt(mean_squared_error(prediction, test[yFeature]))

    return values, features


def pieceByPieceModel(df):
    #add some new columns and modify some variables
    values = {}
    yFeature = 'combatRating'
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    numeric_columns = [c for c in df.select_dtypes(include=numerics).columns.values if 
        c not in [yFeature, 'characterLevel', 'playerCount', 'combatRating', 
                    'characterId','gameId','membershipId','fireTeamId','refrencedId', 'mode',
                    'completionReason', 'team', 'teamScore','precisionKills', 'activityDurationSeconds', 'averageScorePerKill', 
                    'killsDeathsAssists', 
                    'objectivesCompleted', 'zonesNeutralized', 'defensiveKills','offensiveKills','dominationKills', 'standing'] 
        and "mostUsedWeapon" not in c and "weaponKills" not in c and "OfPlayer" not in c and "Weapon" not in c and 'orbs' not in c]

    print("NUMERIC_COLUMNS: {0}".format(len(numeric_columns)))

    features = []
    #numeric_columns = ['longestKillSpree', 'completed', 'averageLifespan', 'place', 'kills','deaths','assists']
    numeric_columns = ['assists', 'deaths', 'completed', 'longestKillSpree', 'kills',
                        'offensiveKills', 'defensiveKills', 'rank',
                        'dominationKills', 'standing',
                        'objectivesCompleted', 'zonesNeutralized',
                        'averageScorePerKill','averageScorePerLife',]
    #numeric_columns.extend([c for c in df.columns if 'weaponKills' in c])
    KBest = None
    for i in range(0,1):
        print("splitting data into test and train sets")
        seed = 17*i
        np.random.seed(seed)
        msk = np.random.rand(len(df)) < 0.8

        features = numeric_columns

        train = df[msk]
        test = df[~msk]
        print("TEST: {0}\nTRAIN: {1}".format(len(test), len(train)))

        # Create linear regression object
        #regr = linear_model.RidgeCV(alphas=range(1,100))
        regr = linear_model.BayesianRidge()

        # Train the model using the training sets
        print("Fitting regression for alpha")
        regr.fit(train[features], train[yFeature])


        # The coefficients
        #values[seed] = {"Coefficient": regr.coef_, "Alpha":regr.alpha_}
        values[seed] = {"Coefficient":regr.coef_, 'Alpha':0}
        
        # Prediciton
        prediction = regr.predict(test[features])

        # The mean square error
        values[seed]["Residual sum of squares"]= np.mean((prediction - test[yFeature]) ** 2)    # Explained variance score: 1 is perfect prediction
        values[seed]['Variance score']= regr.score(test[features], test[yFeature])
        values[seed]['R-Squared']= r2_score(prediction,test[yFeature])
        values[seed]['RMSE'] = sqrt(mean_squared_error(prediction, test[yFeature]))

    return (values, numeric_columns)


def standardizeScorePerGame(df):
    groupByGame = df.groupby("gameId")

    df['standardScoreInGame'] = 0
    i = 0
    for s, g in groupByGame:
        i = i +1
        df.ix[g.index, 'standardScore'] = (g.score - g.score.mean())/(g.score.max() - g.score.min())
        print("Standardized: {0:.2f}".format(float(i)/len(groupByGame.groups.keys())))

    destiny.writeToCsv(df, "datafiles/standard_data.csv")
    return df

def standardizeScoreDataset(df):
    df['scoreStandardized'] = (df.score - df.score.mean())/(df.score.max() - df.score.min())
    destiny.writeToCsv(df, "datafiles/standard_data.csv")
    return df

def ratioPrediction(df, writeToFile=True):
    df['ratioPrediction'] = 0.0
    groupByGame = df.groupby("gameId")
    i = 0
    for s,g in groupByGame:
        i = i + 1
        df.ix[g.index, 'ratioPrediction'] = (g.score/g.score.max())*g.combatRating.max()
        print("Calculating: {0:.2f}".format(float(i)/len(groupByGame.groups.keys())))

    if writeToFile:
        destiny.writeToCsv(df, "datafiles/standard_data.csv")
    return df    

def scoreOutOfMax(df, writeToFile=True):
    groupByGame = df.groupby("gameId")
    df['maxScoreRatio'] = 0.0
    i = 0
    for s,g in groupByGame:
        i = i + 1
        df.ix[g.index, 'maxScoreRatio'] = (g.score/g.score.max())
        df.ix[g.index, 'maxCombatRatingRatio'] = (g.combatRating/g.combatRating.max())
        print("Calculating: {0:.2f}".format(float(i)/len(groupByGame.groups.keys())))
    if writeToFile:
        destiny.writeToCsv(df, "datafiles/standard_data.csv")
    return df

def calculateContribution(df):
    groupByGame = df.groupby("gameId")
    df['contribution'] = 0.0
    i = 0
    for s,g in groupByGame:
        i = i + 1
        df.ix[g.index, 'contribution'] = (g.score/g.score.sum())
        print("Calculating: {0:.2f}".format(float(i)/len(groupByGame.groups.keys())))

    destiny.writeToCsv(df, "datafiles/standard_data.csv")
    return df

def combatRatingStd(df):
    groupByGame = df.groupby("gameId")
    df['combatRatingStd'] = 0
    i = 0
    total = len(groupByGame.groups.keys())
    for s,g in groupByGame:
        i = i + 1
        df.ix[g.index, 'combatRatingStd'] = g.combatRating.std()
        print("Calculating: {0:.2f}".format(float(i)/total))
    destiny.writeToCsv(df,"datafiles/standard_data.csv")
    return df 
def scoreStdRatio(df,writeToFile=True):
    groupByGame = df.groupby("gameId")
    df['scoreStdRatio'] = 0
    i = 0
    total = len(groupByGame.groups.keys())
    for s,g in groupByGame:
        i = i + 1
        df.ix[g.index, 'scoreStdRatio'] = g.score/g.combatRating.std()
        print("Calculating: {0:.2f}".format(float(i)/total))
    if writeToFile:
        destiny.writeToCsv(df,"datafiles/standard_data.csv")
    return df 

def combatRatingRelative(df):
    groupByGame = df.groupby("gameId")
    df['combatRatingReltaive'] = 0
    df['scoreRelative'] = 0
    i = 0
    total = len(groupByGame.groups.keys())
    for s,g in groupByGame:
        i = i + 1
        df.ix[g.index, 'combatRatingRelative'] = g.combatRating/g.combatRating.max()
        df.ix[g.index,'scoreRelative'] = g.score/g.score.max()
        print("Calculating: {0:.2f}".format(float(i)/total))
    destiny.writeToCsv(df,"datafiles/standard_data.csv")
    return df 

if __name__ == "__main__":
    #create training and testing datasets
    df = pd.read_csv("datafiles/standard_data.csv", index_col = 0 )

    #df = ratioPrediction(df)
    #df = calculateContribution(df)
    #df = standardizeScorePerGame(df)
    #df = standardizeScoreDataset(df)
    #df = scoreOutOfMax(df)
    #df = scoreStdRatio(df)

    df = cleaning(df)


    #teamData = pd.read_csv("datafiles/teamData.csv", index_col=0)
    #teamData = cleaning(teamData)
    #print train[[c for c in train.columns if c != "standing" and c!="date"].columns

    #values,features = pieceByPieceModel(df)
    #values, features = teamModel(teamData)
    values,features = scoreModel(df)
    #values,features = ratioModel(df)
    prediction_df = pd.DataFrame(values).T
    print(prediction_df.mean())
    key_to_coef = pd.DataFrame(list(zip(features, prediction_df.mean().ix['Coefficient'])), columns=['variable', 'coefficient'])

    print(key_to_coef.sort("coefficient"))