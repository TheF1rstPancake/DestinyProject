import destinyPlatform as destiny
import itemHashes
import requests
import pandas as pd
import numpy as np 
import multiprocessing 
import logging
import time
import sys

logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)1.1s %(asctime)s %(module)s]:%(lineno)d %(message)s", "%y%m%d %H:%M:%S")


if 'ch' not in logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    ch.name ='ch'
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if 'filehandler' not in logger.handlers:
    filehndlr = logging.FileHandler("log.log")
    filehndlr.name = 'filehandler'
    filehndlr.setLevel(logging.DEBUG)
    filehndlr.setFormatter(formatter)
    logger.addHandler(filehndlr)


def _getPlayerData(player, game_id, game_mode,reference_id, date):
    #build a dictionary to hold this players data
    #we will later take this dictionary and turn it into a dataframe row
    player_data = {"gameId":game_id,
                   "mode":game_mode,
                   "refrencedId":reference_id,
                   "date":date
                   }
    player_data['characterId'] = player['characterId']
    player_data['membershipId'] = player['player']['destinyUserInfo']['membershipId']

    #get the user's 2 most used weapons
    #if they only used one weapon, then just fill the second with 0
    if 'weapons' in player['extended']:
        weapons = player['extended']['weapons']
        weaponUsage = {w["referenceId"]:w['values']['uniqueWeaponKills']['basic']['value'] for w in weapons}
        player_data.update(weaponUsage)

    #grab some extra data just in case we want to do some trending
    player_data['score'] = player['score']['basic']['value']
    player_data['killDeathRatio'] = player['values']['killsDeathsRatio']['basic']['value']
    player_data['kills'] = player['values']['kills']['basic']['value']
    player_data['standing'] = player['standing']
    player_data['completed'] = player['values']['completed']['basic']['value']
    player_data['characterClass'] = player['player']['characterClass']
    player_data['characterLevel'] = player['player']['characterLevel']
    player_data['team'] = player['values']['team']['basic']['value']

    return player_data

def GetWeaponData(game_ids):
    #given a list of game_ids, go back and try get the weaponData for each player in that game
    #we also need the timestamp for the game and it wouldn't be a bad idea to get the map either (just for extra stuff)

    game_data =[]
    logger.info("Getting data for {0} games".format(len(game_ids)))
    count = 0
    for g in game_ids:
        #create a list to hold the data for each character
        #each character's data will be a different dict
        #gameData =[]
        count = count + 1
        logger.info("Attempting to get data for {0}.\t{1:.2f}".format(g, (float(count)*100)/len(game_ids)))
        try:
            game = destiny.getPvPGame(g)
        except destiny.NoDataError as e:
            logger.info('Game data could not be grabbed for {0}.  Trying next game'.format(g))
            continue
        except destiny.BadRequestError as e:
            logger.warning("Received bad request error for {0}. Skipping this game".format(g))
            continue
        except destiny.NoDataError as e:
            logger.warning("Recieved no data error for member {0}. Skipping this game".format(g))
            continue
        except requests.exceptions.ConnectionError as e:
            logger.warning("Received Connection error for {0}.  Pausing and skipping game".format(g))
            logger.warning(e.message)
            time.sleep(60)
            continue

        #game_id is the unique identifier for the GAME
        #reference_id is the unique identifier for the MAP that the game is played on
        game_id = game['Response']['data']['activityDetails']['instanceId']
        reference_id = game['Response']['data']['activityDetails']['referenceId']

        #get the game mode
        game_mode = game['Response']['data']['activityDetails']['mode']

        #get the date
        date = game['Response']['data']['period']

        #get each players data
        #create a list of dictionaries that we will then use to create a dataframe
        #NOTE:  this includes all players that entered the game, including any that quit
        game_data.extend([_getPlayerData(player, game_id, reference_id, game_mode, date) for player in game['Response']['data']['entries']])

    game_details = pd.DataFrame(game_data)
    return game_details


def _addCombatRating(data):
    #go through each game in this chunk of data and find the player's combat rating
    data['combatRating'] = 0

    #get a list of unique game ids in this chunk
    
    game_ids = data['gameId'].unique()
    logger.info("Getting data for {0} games".format(len(game_ids)))

    count = 0
    #fetch each game
    for k in game_ids:
        count = count + 1
        logger.info("Fetching game {0}\t{1:.2f}".format(k, (float(count)*100)/len(game_ids)))
        try:
            r = destiny.getPvPGame(k)
        except requests.exceptions.ConnectionError as e:
            logger.exception("ConnectionError! Resting and trying request again!")
            time.sleep(120)
            r = destiny.getPvPGame(k)
            pass
        #for each player, set their combat rating
        for player in r['Response']['data']['entries']:
            charId = player['characterId']
            data.ix[(data['gameId'] == int(k)) & (data['characterId'] == int(charId)), 'combatRating'] = player['extended']['values'].get("combatRating",0)
    return data

def _addKADR(data):
    #go through each game in this chunk of data and find the player's combat rating
    data['killDeathAssist'] = 0

    #get a list of unique game ids in this chunk
    
    game_ids = data['gameId'].unique()
    logger.info("Getting data for {0} games".format(len(game_ids)))

    count = 0
    #fetch each game
    for k in game_ids:
        count = count + 1
        logger.info("Fetching game {0}\t{1:.2f}".format(k, (float(count)*100)/len(game_ids)))
        try:
            r = destiny.getPvPGame(k)
        except requests.exceptions.ConnectionError as e:
            logger.exception("ConnectionError! Resting and trying request again!")
            time.sleep(120)
            r = destiny.getPvPGame(k)
            pass
        #for each player, set their combat rating
        for player in r['Response']['data']['entries']:
            charId = player['characterId']
            data.ix[(data['gameId'] == int(k)) & (data['characterId'] == int(charId)), 'killDeathAssist'] = player['extended']['values'].get("killsDeathsAssists",0)
    return data


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
    chunks = [d for d in weaponData.chunks(df, len(df)/4)]
    update_games = p.map(func, chunks)
    
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
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


if __name__ == "__main__":
    """data = pd.read_csv("datafiles/IronBanner.csv")

    #groupedByMap = data.groupby("refrencedId")
    #df_chunks = [game for _, game in groupedByMap]
    game_ids = list(data['gameId'].unique())

    logger.info("Building chunks")
    n = len(game_ids)/4
    game_id_chunks = [c for c in chunks(game_ids,n)]

    p = multiprocessing.Pool(4)

    logger.info("Fetching data")
    weaponData = p.map(GetWeaponData, game_id_chunks)

    data = pd.concat(weaponData, ignore_index=True)
    data.to_csv("datafiles/IB_WeaponData.csv", encoding='utf-8')
    """
    data = pd.read_csv("datafiles/IB_WeaponsUpdated.csv")
    p = multiprocessing.Pool(4)

    #group the dataframe by map to make for nice chunks of data
    #then place each chunk in a list so we can iterate over it
    chunk = [d for d in chunks(data, len(data)/5)]
    update_games = p.map(_addKADR,chunk)
    #updated_games = p.map(_addCombatRating, chunk)
    updated = pd.concat(updated_games)

    updated.to_csv("IB_WeaponsUpdated.csv", encoding="utf-8")

