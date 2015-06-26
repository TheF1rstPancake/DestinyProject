import destinyPlatform as destiny
import pandas as pd
import random
import os
import logging
import sys
import argparse
import multiprocessing
import time

logging.getLogger("requests").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(process)d - %(levelname)s - %(message)s')

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

logger.info('LIBRARY LOADED---------------------------------\n')

HOOLIGAN_COMMITTEE = ["Jalepeno112","lil spoon 219", 
                     "ArcticSupremecy", "sunnyD7768",
                     "BigBadCarp","InfernoMatrix","StangbroZ"]

def getGame(membershipId, uniqueGameIds=[]):
    start_user_characters = destiny.getCharacterInfo(membershipId)
    character_info = start_user_characters['Response']['data']['characters']
    
    #take the user's highest level character
    #NOTE: if all characters are the same level, then this only gets one of them
    character_levels = [c['characterLevel'] for c in character_info]
    character_index = character_levels.index(max(character_levels))
    character = character_info[character_index]

    #get a game
    games_to_fetch = 1
    try:
        most_recent = destiny.getMostRecentPvPGames(membershipId,character['characterBase']['characterId'],count = games_to_fetch, mode='Control')
    except destiny.BadRequestError as e:
        logger.exception('BadRequestError')
        raise e
    except destiny.NoDataError as e:
        logger.exception('NoDataError')
        raise e

    #break the most recent game into a dataframe
    #each character's info is under the 'entries' dictionary
    #what we need in the dataframe is:
    #   gameID    activityDetails['referenceId']
    #   gametype  activityDetils['mode']
    #   character Ids / membershipIds (either works.  Just to establish separate users)
    #   kills   game_data['kills']['basic']['value']
    #   deaths  game_data['deaths']['basic']'value']
    #   assits  game_data['assists']['basic']['value']
    #   precisionKills
    #   averageLifespan
    #   objectivesCompleted
    #   averageScorePerKill
    #   team
    #   standing (0 for victory, 1 for defeat)
    #   averageScorePerLife
    #   averageScorePerKill
    #   combatRating

    #game_id is the unique identifier for the GAME
    #reference_id is the unique identifier for the MAP that the game is played on
    game_id = most_recent[0]['Response']['data']['activityDetails']['instanceId']
    reference_id = most_recent[0]['Response']['data']['activityDetails']['referenceId']

    #if this game is already in the dataset, then we need to get another game
    #jump back and get a different game
    #print(game_id, uniqueGameIds)
    while game_id in uniqueGameIds:
        logger.warning("Game {0} already logged! Looking for another game!".format(game_id))
        games_to_fetch = games_to_fetch + 1
        
        try:
            logger.info("Fetching {0} games".format(games_to_fetch))
            more_games = destiny.getMostRecentPvPGames(membershipId,
                                                   character['characterBase']['characterId'],
                                                   count = games_to_fetch, mode='Control')    
        except destiny.BadRequestError as e:
            logger.exception('BadRequestError')
            raise e
        except destiny.NoDataError as e:
            logger.exception('NoDataError')
            raise e
        except Exception as e:
            logger.exception("Unknown exception")
            raise e
        logger.info("Sucessfully retrieved {0} games".format(len(more_games)))
        most_recent = [more_games[-1]]
        game_id = most_recent[0]['Response']['data']['activityDetails']['instanceId'] 

    logger.info("Using game {0}".format(game_id))
    
    #get the game mode
    game_mode = most_recent[0]['Response']['data']['activityDetails']['mode']
    
    #get the date
    date = most_recent[0]['Response']['data']['period']

    #get each players data
    #create a list of dictionaries that we will then use to create a dataframe
    #NOTE:  this includes all players that entered the game, including any that quit
    all_player_data = []
    for player in most_recent[0]['Response']['data']['entries']:
        #build a dictionary to hold this players data
        #we will later take this dictionary and turn it into a dataframe row
        player_data = {"gameId":game_id,
                       "mode":game_mode,
                       "refrencedId":reference_id,
                       "date":date
                       }
         
        player_data['characterId'] = player['characterId']
        player_data['membershipId'] = player['player']['destinyUserInfo']['membershipId']

        #add all of the data from the 'values' dictionary with a little bit of formatting
        #each key in values points to another dicitonary that holds the display and numeric values
        #we just want the numeric value
        #This gives us:
        #   u'activityDurationSeconds'
        #   u'assists'
        #   u'averageScorePerKill'
        #   u'averageScorePerLife'
        #   u'completed'
        #   u'completionReason'
        #   u'deaths'
        #   u'fireTeamId'
        #   u'kills'
        #   u'killsDeathsAssists'
        #   u'killsDeathsRatio'
        #   u'playerCount'
        #   u'score'
        #   u'standing'
        #   u'team'
        #   u'teamScore'
        #Standing tells us whether or not the user won the game 
        player_data.update({k:v['basic']['value'] for k,v in player['values'].iteritems()})
            
        #get bonus info
        #NOTE:  fireTeamId appears in the previous group but it does not contain any data.
        #the value is always 0.  But the actual fireTeamId appears in extended[values]
        if "extended" not in player:
            return None

        extended_keys = ['averageLifespan', 'combatRating', 'orbsDropped', 'precisionKills',
                         'orbsGathered', 'orbsDropped', 'objectivesCompleted',
                         'offensiveKills','defensiveKills', 'fireTeamId', 'longestKillSpree', 
                         'weaponKillsShotgun','weaponKillsSuper','weaponKillsSniper','weaponKillsMelee',
                         'weaponKillsPulseRifle','weaponKillsFusionRifle', 'weaponKillsScoutRifle','weaponKillsRocketLauncher',
                         'weaponKillsAutoRifle', 'weaponKillsMachinegun', 'weaponKillsHandCannon', 'weaponKillsSideArm',
                         'killsOfPlayerHunter', 'killsOfPlayerTitan','killsOfPlayerWarlock',
                         'deathsOfPlayerHunter','deathsOfPlayerTitan','deathsOfPlayerWarlock', 
                         "medalsDominationKill", "zonesNeutralized",
                         ]
        #not everyone has those keys.  The weaponKill keys only occur if a player had a kill with that weapon
        #check to see if the key exists, if it does get the value, else fill with 0
        for k in extended_keys:
            if k in player['extended']['values']:
                player_data[k] = player['extended']['values'][k]['basic']['value']
            else:
                player_data[k] = 0
        
        #get the user's 2 most used weapons
        #if they only used one weapon, then just fill the second with 0
        if 'weapons' in player['extended']:
            weapons = player['extended']['weapons']
            weaponUsage = [{"referenceId":w['referenceId'],"kills":w['values']['uniqueWeaponKills']['basic']['value']}
                            for w in weapons]
            if len(weaponUsage) == 0:
                player_data['mostUsedWeapon1'] = 0
                player_data['mostUsedWeapon1Kills'] = 0
                player_data['mostUsedWeapon2'] = 0
                player_data['mostUsedWeapon2Kills'] = 0
            elif len(weaponUsage) >= 2:
                #sorts from least to greatest.  Get the last two
                top_two = sorted(weaponUsage, key=lambda w:w['kills'])[-2:]
                player_data['mostUsedWeapon1'] = top_two[1]['referenceId']
                player_data['mostUsedWeapon1Kills'] = top_two[1]['kills']
                player_data['mostUsedWeapon2'] = top_two[0]['referenceId']
                player_data['mostUsedWeapon2Kills'] = top_two[0]['kills']
            elif len(weaponUsage) == 1:
                top_one = sorted(weaponUsage, key=lambda w:w['kills'])[-1:]
                player_data['mostUsedWeapon1'] = top_one[0]['referenceId']
                player_data['mostUsedWeapon1Kills'] = top_one[0]['kills']
                player_data['mostUsedWeapon2'] = 0
                player_data['mostUsedWeapon2Kills'] = 0
        else:
             player_data['mostUsedWeapon1'] = 0
             player_data['mostUsedWeapon1Kills'] = 0
             player_data['mostUsedWeapon2'] = 0
             player_data['mostUsedWeapon2Kills'] = 0
        
        #get simple character data
        player_keys = ['characterLevel', 'characterClass']
        for k in player_keys:
            if k in player['player']:
                player_data[k] = player['player'][k]
            else:
                player_data[k] = None

        #append to list
        all_player_data.append(player_data)
    
    #build a dataframe from our list of dicitonaries
    game_details = pd.DataFrame.from_records(all_player_data)

    return game_details


def randomWalk(user_membershipId, game_data=None, num_games = 1000):
    """
    Do a random walk through the Destiny PostGameCarnageReport

    :param user_membershipId:   the starting user's ID to use for the walk
    :param gameData:            *optional*; a dataframe from a previous walk that you want to expand upon
    """

    #check if we need to initialize gameData
    if game_data is None:
        game_data = pd.DataFrame(columns=['gameId'])

    #number of games we hope to get from this user
    try:
        for i in range(num_games):
            game_details = None
            next_member = user_membershipId

            #get a game.  If using the current user causes problems, then try a different user in the dataframe
            while game_details is None:
                try:
                    game_details = getGame(next_member,game_data['gameId'].unique())
                except destiny.BadRequestError as e:
                    logger.warning("Received bad request error for {0}. Trying again with different player".format(next_member))
                    game_details = None
                    pass
                except destiny.NoDataError as e:
                    logger.warning("Recieved no data error for {0}.  Trying again with different player".format(next_member))
                    game_details = None
                    pass
                except Exception as e:
                    logger.warning("Unkown exception")
                    raise

                if game_details is None:
                    #get a random person from the dataframe and try them instead
                    rand_idx = random.randrange(0,len(game_data))
                    logger.info("Picking new random starting point from frame: {0}".format(rand_idx))
                    next_member = game_data['membershipId'][rand_idx]

               

            #add the new dataframe in
            game_data = pd.concat([game_data,game_details], ignore_index=True)
            
            #from the most recent game 
            #pick a player that is NOT the character we used in the last one
            user_membershipId_options = [id for id in game_details['membershipId'] if id != user_membershipId]
            user_membershipId = user_membershipId_options[random.randrange(0,len(user_membershipId_options))] 
            logger.info("Games: {0}".format(i))

    except Exception as e:
           logger.exception(e)
           logger.error("GAME_DATA LENGTH: {0}".format(len(game_data)))
           logger.error(game_data['membershipId'])
           #in the event of an error, return the dataframe that we have can at least use something
           return (0,game_data)
    return (1,game_data)

def runBlogProject(start_user = ["Jalepeno112"], num_games=1000, datafilename = 'data.csv'):
    """
    Build a dataset by querying the Destiny Platform API.

    :param start_user:  list indicating the names of players to use to be anchors for the random walk through the Platform
    :param num_games:   maximum number of games to get for each player in start_user 

    .. note::
        If an error occurs while fetching data during the random walk, this function will just jump to the next anchor in *start_user*.
        So the maximum number of games is:
            len(start_user) * num_games
    """

    #fetch lots of data -> format into one large dataframe -> write to CSV

    #fetch
    #random walk among user's games -> start with me
    #take most recent game, get data for all players, and then randomly pick a character and go get their most recent game
    #if the recent game is the same then get there 2nd most recent game
    
    game_data = pd.DataFrame()
    

    #if result comes back with a 0, then something eventually went wrong in the walk
    #go to the next user in our list in order to get data
    #if result is 1, we got all the data we wanted off one person
    start_users_ids = [destiny.getMembershipID(user) for user in start_user]

    p = multiprocessing.Pool(4)
    mapped_list = p.map(randomWalk, start_users_ids)
    
    #mapped_list is a list of tuples. The first item in the tuple is a 1 or 0 indicate successful completion
    #second is the dataframe
    #concat the dataframes together and then drop duplicates
    game_data = pd.concat([t[1] for t in mapped_list], ignore_index=True)

    #add weapon type, name, and class info
    #it's faster to do it after the dataframe has been built.
    #That way we only make as many requests as there are unique weapons
    game_data = _adjustData(game_data)

    game_data = game_data.drop_duplicates()

    game_data.to_csv(datafilename)
    return game_data

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
            definition = destiny.getInventoryItemOnline(weapon_map.keys()[0])

            if definition is not None and definition['ErrorStatus'] == 'Success':
                logger.info("Successfully fetched data for {0}".format(i))
                weapon_map[i]['Name'] = definition['Response']['data']['inventoryItem']['itemName']
                weapon_map[i]['Tier'] = definition['Response']['data']['inventoryItem']['tierTypeName']
                weapon_map[i]['Type'] = definition['Response']['data']['inventoryItem']['bucketTypeHash']
            unique_items_map.update(weapon_map)
        #update game data with the name, tier and type we just pulled
        for hash,data in unique_items_map.iteritems():
            game_data.ix[game_data[t] == hash, t+'Name'] = data['Name']
            game_data.ix[game_data[t] == hash, t+'Tier'] = data['Tier']
            game_data.ix[game_data[t] == hash, t+'Type'] = data['Type']

        game_data.to_csv("data_updated.csv",encoding='utf-8')

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
    groupByMap = game_data.groupby('refrencedId')
    game_list = [game for name, game in groupByMap]

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
    game_data.to_csv("data_updated_multi.csv")

    return game_data



"""
All of the following functions were used to add more information to the dataset after it had initially been build
"""
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
"""
END SECTION
"""


if __name__ == "__main__":
    print("Hello World!")

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_games", default=1000, type=int)
    parser.add_argument("--datafilename", default="datafiles/data.csv")

    args = parser.parse_args()    

    runBlogProject(start_user=HOOLIGAN_COMMITTEE, 
        num_games=args.num_games, datafilename=args.datafilename)
   