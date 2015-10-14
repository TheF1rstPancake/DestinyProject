"""
Utility functions for DestinyBlogProject.
These functions are designed to add new data onto an existing dataset.
This is done either by combing through the data currently in the dataset or by going back out and fetching new data.
"""

import destinyPlatform as destiny
import pandas as pd
import random
import os
import logging
import sys
import argparse
import multiprocessing
import time
import requests

logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger("DestinyProject")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)1.1s %(asctime)s %(module)s]:%(lineno)d %(message)s", "%y%m%d %H:%M:%S")

def writeToCsv(df, file_name):
    df.to_csv(file_name, encoding="utf-8", float_format="%.8f")

def _adjustData(game_data, columnTitle = None):
    """
    Go through the weapon columns and add further data about them.  Namely, weapon name and tier (ie. exoctic, legendary,etc.)
    We do it after fetching the entire dataset because it is easier to do this at the end than after each fetch.
    This way, we only have to one fetch to get the stats for each unique weapon in the dataset.
    
    :param game_data:   the data frame of game data compiled by running :func:`runBlogProject`

    """
    if columnTitle == None:
        columnTitle = ['mostUsedWeapon1', 'mostUsedWeapon2']

    for t in columnTitle:
        game_data[t+'Name'] = 'None'
        game_data[t+'Tier'] = 'None'
        game_data[t+'Type'] = 'None'
        #get the unique items in that column
        unique_items = game_data[t].unique()
        unique_items_map = {}
        for i in unique_items:
            logger.info("Getting data for weapon {0}".format(i))
            weapon_map = { i : {
                                "Name": 'None',
                                "Tier": "None",
                                "Type": "None",
                                }
                        }
            definition = destiny.getInventoryItemOnline(list(weapon_map.keys())[0])

            if definition is not None and definition['ErrorStatus'] == 'Success':
                logger.info("Successfully fetched data for {0}".format(i))
                weapon_map[i]['Name'] = definition['Response']['data']['inventoryItem']['itemName']
                weapon_map[i]['Tier'] = definition['Response']['data']['inventoryItem']['tierTypeName']
                weapon_map[i]['Type'] = definition['Response']['data']['inventoryItem']['bucketTypeHash']
            unique_items_map.update(weapon_map)
        #update game data with the name, tier and type we just pulled
        for hash,data in unique_items_map.items():
            game_data.ix[game_data[t] == hash, t+'Name'] = data['Name']
            game_data.ix[game_data[t] == hash, t+'Tier'] = data['Tier']
            game_data.ix[game_data[t] == hash, t+'Type'] = data['Type']

        #game_data.to_csv("data_updated.csv",encoding='utf-8')
    return game_data

def _addFireteamInfo(game_data):
    count = 0
    for g in game_data:
        g['inFireTeam'] = 0
        g['membersInFireTeam'] = 1
        for t in g.fireTeamId.unique():
            msk = g.fireTeamId == t
            membersInFT = len(g[msk])
            if membersInFT > 1:
                g.ix[msk, ["inFireTeam", "membersInFireTeam"]] = [1, membersInFT]
        print("{0:.3f} complete".format(count/len(game_data)))
        count = count + 1

    return game_data
def _addFeatureMultiProcess(game_data, func, **kwargs):
    """
    Add a new feature to a dataframe by chunking the dataframe and then applying a function over the chunks.
    Each chunk will then have the new feature, and these chunks can be joined back together in order to create an update dataframe.

    .. note::
        The function you pass must modify the dataframe **and** return it.
        See the functions below for examples.

    :param game_data:   pandas dataframe containing all of the data
    :param func:        name of the function we want to use to modify the dataframe
    """
    start = time.time()
    p = multiprocessing.Pool(4)

    #group the dataframe by map to make for nice chunks of data
    #then place each chunk in a list so we can iterate over it
    groupByClass = game_data.groupby('characterClass')
    game_list = [game for _, game in groupByClass]

    update_games = p.map(func, game_list)
    #mapped_list is a list of tuples. The first item in the tuple is a 1 or 0 indicate successful completion
    #second is the dataframe
    #concat the dataframes together and then drop duplicates
    #p.join()

    duration = time.time() - start
    logger.info("Data fetched in {0} seconds".format(duration))

    logger.info("Building dataframe from chunks and writing to file")
    game_data = pd.concat([g for g in update_games], ignore_index=True)
    game_data = game_data.drop_duplicates()
    game_data.to_csv("data_updated_multi.csv", encoding="utf-8")

    return game_data


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def multiProcessByGame(game_data, func, writeToFile = False, **kwargs):
    start = time.time()
    p = multiprocessing.Pool(4)

    #group the dataframe by map to make for nice chunks of data
    #then place each chunk in a list so we can iterate over it
    groupByGame = game_data.groupby('gameId')
    num_games = len(groupByGame.groups)

    game_list = chunks([game for _, game in groupByGame], round(num_games/4))

    print("Length: ", len(game_list))

    update_games = p.map(func, game_list)
    
    #mapped_list is a list of tuples. The first item in the tuple is a 1 or 0 indicate successful completion
    #second is the dataframe
    #concat the dataframes together and then drop duplicates
    #p.join()

    duration = time.time() - start
    logger.info("Data fetched in {0} seconds".format(duration))

    logger.info("Building dataframe from chunks and writing to file")
    print(len(update_games))
    game_data = pd.concat([i for g in update_games for i in g], ignore_index=True)
    game_data = game_data.drop_duplicates()
    if writeToFile:
        game_data.to_csv("data_updated_multi.csv", encoding="utf-8")

    return game_data    

def _addMissingWeapons(game_data):
    game_data['weaponKillsMachinegun'] = 0
    game_data['weaponKillsHandCannon'] = 0
    game_data['weaponKillsSideArm'] = 0

    groupByGame = game_data.groupby("gameId")

    totalGames = len(groupByGame)
    count = 1
    for group in list(groupByGame.groups.keys()):
        logger.info("Grabbing for game {0}; {1} out of {2}".format(group, count, totalGames))
        game_json = destiny.getPvPGame(group)
        for player in game_json['Response']['data']['entries']:
            memId = player['player']['destinyUserInfo']['membershipId']
            if 'weaponKillsHandCannon' in player['extended']['values']:
                game_data.ix[(game_data['gameId'] == group) & (game_data['membershipId'] == int(memId)), 'weaponKillsHandCannon'] = player['extended']['values']['weaponKillsHandCannon']['basic']['value']
            if 'weaponKillsMachinegun' in player['extended']['values']:
                game_data.ix[(game_data['gameId'] == group) & (game_data['membershipId'] == int(memId)), 'weaponKillsMachinegun'] = player['extended']['values']['weaponKillsMachinegun']['basic']['value']
            if 'weaponKillsSideArm' in player['extended']['values']:
                game_data.ix[(game_data['gameId'] == group) & (game_data['membershipId'] == int(memId)), 'weaponKillsSideArm'] = player['extended']['values']['weaponKillsSideArm']['basic']['value']

        count = count + 1
    game_data.to_csv("data_post_houseOfWolvesUpdate.csv", encoding='utf-8')

def _addPrimarySecondaryHeavy(game_data):
    primaryColumns = ['weaponKillsScoutRifle', 'weaponKillsAutoRifle', 'weaponKillsPulseRifle', 'weaponKillsHandCannon']
    secondaryColumns = ['weaponKillsSideArm', 'weaponKillsShotgun', 'weaponKillsSniper', 'weaponKillsFusionRifle']
    heavyColumns = ['weaponKillsRocketLauncher', 'weaponKillsMachinegun']


    game_data['PrimaryWeapon'] = game_data[(game_data[primaryColumns] > 0).any(1)][primaryColumns].idxmax(1).apply(lambda x: x.replace("weaponKills",""))
    game_data['PrimaryWeapon'].fillna("None",inplace = True)

    game_data['SecondaryWeapon'] = game_data[(game_data[secondaryColumns] > 0).any(1)][secondaryColumns].idxmax(1).apply(lambda x: x.replace("weaponKills",""))
    game_data['SecondaryWeapon'].fillna("None",inplace = True)    
    
    game_data['HeavyWeapon'] = game_data[(game_data[heavyColumns] > 0).any(1)][heavyColumns].idxmax(1).apply(lambda x: x.replace("weaponKills",""))
    game_data['HeavyWeapon'].fillna("None",inplace = True)

    return game_data

def _addZonesNeutralized(game_data):
    game_data['zonesNeutralized'] = 0
    groupByGame = game_data.groupby("gameId")
    totalGames = len(groupByGame)
    count = 1
    for group in list(groupByGame.groups.keys()):
        logger.info("Grabbing game {0}; {1} out of {2}".format(group, count, totalGames))
        game_json = destiny.getPvPGame(group)
        for player in game_json['Response']['data']['entries']:
            memId = player['player']['destinyUserInfo']['membershipId']
            if "zonesNeutralized" in player['extended']['values']:
                game_data.ix[(game_data['gameId'] == group) & (game_data['membershipId'] == int(memId)), 'zonesNeutralized'] = player['extended']['values']['zonesNeutralized']['basic']['value']
        count = count + 1
    return game_data


def _addDominationMedals(game_data):
    game_data['dominationKills'] = 0
    groupByGame = game_data.groupby("gameId")

    totalGames = len(groupByGame)
    count = 1
    for group in list(groupByGame.groups.keys()):
        logger.info("Grabbing game {0}; {1} out of {2}".format(group, count, totalGames))
        game_json = destiny.getPvPGame(group)
        for player in game_json['Response']['data']['entries']:
            memId = player['player']['destinyUserInfo']['membershipId']
            if "medalsDominationKill" in player['extended']['values']:
                game_data['dominationKills'] = player['extended']['values']['medalsDominationKill']['basic']['value']
        count = count + 1
    return game_data

def _addGrenadeKills(game_data):
    logger.info("Adding Grenade and Relic Kill values for all games")
    game_data['weaponKillsGrenade'] = 0
    game_data['weaponKillsRelic'] = 0
    groupByGame = game_data.groupby('gameId')

    totalGames = len(groupByGame)
    count = 1
    for group in list(groupByGame.groups.keys()):
        logger.info("Grabbing for game {0}; {1} out of {2}".format(group, count, totalGames))
        game_json = destiny.getPvPGame(group)
        for player in game_json['Response']['data']['entries']:
            memId = player['player']['destinyUserInfo']['membershipId']
            if 'weaponKillsGrenade' in player['extended']['values']:
                game_data.ix[(game_data['gameId'] == group) & (game_data['membershipId'] == int(memId)), 'weaponKillsGrenade'] = player['extended']['values']['weaponKillsGrenade']['basic']['value']                
            if 'weaponKillsRelic' in player['extended']['values']:
                 game_data.ix[(game_data['gameId'] == group) & (game_data['membershipId'] == int(memId)), 'weaponKillsRelic'] = player['extended']['values']['weaponKillsRelic']['basic']['value']
        count = count + 1
    return game_data