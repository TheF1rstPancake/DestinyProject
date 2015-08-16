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

if __name__ == "__main__":
    #create training and testing datasets
    df = pd.read_csv("datafiles/data.csv", index_col = 0 )
    df = df[df['combatRating'] > 0]
    #print train[[c for c in train.columns if c != "standing" and c!="date"].columns

    df['killsPerMinute'] = df['kills']/(df['activityDurationSeconds']/60)
    df['normalKills'] = df['kills'] - df['precisionKills']
    values = {}
    df['completed'] = abs(df['completed'] - 1)
    df['standing'] = abs(df['standing'] - 1)
    df['rank'] = 1.0 - (df['place']/df['playerCount'])
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
                        'offensiveKills', 'defensiveKills', 'rank', 'averageScorePerKill',
                        'killsPerMinute','averageScorePerLife']
    #numeric_columns.extend([c for c in df.columns if 'weaponKills' in c])
    KBest = None
    for i in range(0,1):
        print("splitting data into test and train sets")
        seed = 17*i
        np.random.seed(seed)
        msk = np.random.rand(len(df)) < 0.8


        KBest = SelectPercentile(f_regression, percentile=100, )
        X_new = KBest.fit_transform(df[numeric_columns], df[yFeature])


        features = df[[numeric_columns[i] for i in KBest.get_support(indices=True)]].columns.values
        print("TOP K FEATURES: {0}".format(features))
        print(sorted(zip(numeric_columns, KBest.scores_), key = lambda x: -x[1]))

        train = df[msk]
        test = df[~msk]
        print("TEST: {0}\nTRAIN: {1}".format(len(test), len(train)))

        # Create linear regression object
        #regr = linear_model.RidgeCV(alphas=range(1,100))
        #regr = linear_model.BayesianRidge()

        regr = SVR()

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

        """
        print 'Coefficients: \n', sorted(zip(features,regr.coef_))
        print 'Alpha: {0}'.format(regr.alpha_)
        
        # Prediciton
        prediction = regr.predict(test[features])

        # The mean square error
        print("Residual sum of squares: %.2f"
              % np.mean((prediction - test[yFeature]) ** 2))    # Explained variance score: 1 is perfect prediction
        print('Variance score: %.4f' % regr.score(test[features], test[yFeature]))
        print('R-Squared: %.4f' % r2_score(prediction,test[yFeature]))
        print('RMSE: {0}'.format(sqrt(mean_squared_error(prediction, test[yFeature]))))
        """
    prediction_df = pd.DataFrame(values).T
    print  prediction_df.mean()
    key_to_coef = pd.DataFrame(zip(features, prediction_df.mean().ix['Coefficient']), columns=['variable', 'coefficient'])
    KBestScores = pd.DataFrame(zip(numeric_columns, KBest.scores_), columns=['variable','KBestScore'])

    prediction_df.mean().to_csv("datafiles/extras/combatRating_prediciton_df.csv")
    key_to_coef.to_csv("datafiles/extras/combatRating_keyToCoef.csv")
    KBestScores.to_csv("datafiles/extras/combatRating_kBestScores.csv")

    print(key_to_coef.sort("coefficient"))   
    