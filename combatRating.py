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

from math import sqrt


def rSquaredForEachColumn(data, columns):
    values ={}
    for k in numeric_columns:
        yFeature="combatRating"
        regr = linear_model.RidgeCV(alphas=range(1,100))
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



if __name__ == "__main__":
    #create training and testing datasets
    df = pd.read_csv("datafiles/data.csv", index_col = 0 )
    df = df[df['combatRating']!= -1]
    #print train[[c for c in train.columns if c != "standing" and c!="date"].columns

    features = [ 
            'kills',
            'completed',
            'averageScorePerLife',
            'standing',
            'score',
            'killsDeathsAssists',
            'killsDeathsRatio',
            'precisionKills',
            'orbsDropped',
            'place',
            'deaths',

            ]

    #features.extend([c for c in df.columns if 'kills' in c or 'Kills' in c])
    values = {}
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
    print(pd.DataFrame(values).T.mean())

   
    