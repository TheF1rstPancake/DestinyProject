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
import destinyutils

logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger("DestinyProject")
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
logger.info('Destiny Blog Project - Hello World!')

HOOLIGAN_COMMITTEE = ["Jalepeno112","lil spoon 219", 
                     "ArcticSupremecy", "sunnyD7768",
                     "BigBadCarp","InfernoMatrix","StangbroZ", 
                     "Dmen7201", 'RangerCampos', 'Grim314']

def addGame(most_recent):
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
        player_data.update({k:v['basic']['value'] for k,v in player['values'].items()})
            
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
                         'weaponKillsGrenade', 'weaponKillsRelic',
                         'killsOfPlayerHunter', 'killsOfPlayerTitan','killsOfPlayerWarlock',
                         'deathsOfPlayerHunter','deathsOfPlayerTitan','deathsOfPlayerWarlock', 
                         "medalsDominationKill", "zonesNeutralized", 'resurrectionsPerformed','resurrectionsReceived',
                         ]
        #not everyone has those keys.  The weaponKill keys only occur if a player had a kill with that weapon
        #check to see if the key exists, if it does get the value, else fill with 0
        for k in extended_keys:
            if k in player['extended']['values']:
                player_data[k] = player['extended']['values'][k]['basic']['value']
            else:
                player_data[k] = 0
        
        if "medalsDominationKill" in player['extended']['values']:
            player_data['dominationKills'] = player['extended']['values']['medalsDominationKill']['basic']['value']

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

def _getGame(membershipId, characterId, uniqueGameIds=[], gametype='Control'):
    #start_user_characters = destiny.getCharacterInfo(membershipId)
    #character_info = start_user_characters['Response']['data']['characters']

    logger.info("Getting most recent {0} game for {1}".format(gametype, membershipId))

    #get a game
    games_to_fetch = 1
    try:
        most_recent = destiny.getMostRecentPvPGames(membershipId,characterId,count = games_to_fetch, mode=gametype)
    except Exception as e:
        raise e

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
                                                   characterId,
                                                   count = games_to_fetch, mode=gametype)    
        except Exception as e:
            raise e
        logger.info("Sucessfully retrieved {0} games".format(len(more_games)))
        most_recent = [more_games[-1]]
        game_id = most_recent[0]['Response']['data']['activityDetails']['instanceId'] 

    logger.info("Using game {0}".format(game_id))
    
    game_details = addGame(most_recent)

    return game_details

def randomWalk(user_membership, game_data=None):
    """
    Do a random walk through the Destiny PostGameCarnageReport

    :param user_membership:   a dictionary whose key is the membership id and value is the characterId to start the walk with
    :param gameData:          *optional*; a dataframe from a previous walk that you want to expand upon
    """

    logger.info("Starting random walk with:\n\tMember:\t\t{0}\n\tCharacter:\t{1}".format(list(user_membership.keys())[0], list(user_membership.values())[0]))

    #check if we need to initialize gameData
    if game_data is None:
        game_data = pd.DataFrame(columns=['gameId'])

    #number of games we hope to get from this user
    try:
        next_member = user_membership['membershipId']
        next_character = user_membership['characterId']
        gametype = user_membership['gametype']
        num_games = user_membership['num_games']
        for i in range(num_games):
            game_details = None

            #get a game.  If using the current user causes problems, then try a different user in the dataframe
            while game_details is None:
                try:
                    game_details = _getGame(next_member, next_character, game_data['gameId'].unique(), gametype=gametype)
                except destiny.BadRequestError as e:
                    logger.warning("Received bad request error for {0}. Trying again with different player".format(next_member))
                    game_details = None
                    pass
                except destiny.NoDataError as e:
                    logger.warning("Recieved no data error for {0}.  Trying again with different player".format(next_member))
                    game_details = None
                    pass
                except requests.exceptions.ConnectionError as e:
                    logger.warning("Received Connection error for {0}.  Pausing and trying again".format(next_member))
                    logger.warning(e.message)
                    time.sleep(60)
                    pass
                except Exception as e:
                    logger.warning("Unkown exception")
                    raise

                if game_details is None:
                    #get a random person from the dataframe and try them instead
                    rand_idx = random.randrange(0,len(game_data))
                    logger.info("Picking new random starting point from frame: {0}".format(rand_idx))
                    
                    #get their membership id and character id
                    next_member = game_data['membershipId'][rand_idx]
                    next_character = game_data['characterId'][rand_idx]
               

            #add the new dataframe in
            game_data = pd.concat([game_data,game_details], ignore_index=True)
            
            #from the most recent game 
            #pick a player that is NOT the character we used in the last one
            next_user_options = game_details[game_details['membershipId'] != next_member]
            rand_idx = random.randrange(0,len(next_user_options))
            next_member = next_user_options['membershipId'][next_user_options.index.values[rand_idx]]
            next_character = next_user_options['characterId'][next_user_options.index.values[rand_idx]]

            logger.info("Games: {0}".format(i))

    except Exception as e:
           logger.exception(e)
           logger.error("GAME_DATA LENGTH: {0}".format(len(game_data)))
           #logger.error(game_data['membershipId'])
           #in the event of an error, return the dataframe that we have can at least use something
           return (0,game_data)
    return (1,game_data)

def runBlogProject(start_user = ["Jalepeno112"], num_games=1000, datafilename = 'data.csv', gametype="Control"):
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

    start_user_characters = [{"membershipId":membershipId, "characterId":characterId, "gametype":gametype, 'num_games':num_games} 
                    for membershipId in start_users_ids for characterId in destiny.getCharacters(membershipId).keys()]

    p = multiprocessing.Pool(4)
    mapped_list = p.map(randomWalk, start_user_characters)
    
    #mapped_list is a list of tuples. The first item in the tuple is a 1 or 0 indicate successful completion
    #second is the dataframe
    #concat the dataframes together and then drop duplicates
    game_data = pd.concat([t[1] for t in mapped_list], ignore_index=True)

    logger.info("Dropping duplicates")
    game_data = game_data.drop_duplicates()

    #add weapon type, name, and class info
    #it's faster to do it after the dataframe has been built.
    #That way we only make as many requests as there are unique weapons
    logger.info("Adding extra data")
    try:
        game_data = destinyutils._addFeatureMultiProcess(game_data,destinyutils._adjustData)
        game_data = destinyutils._addFeatureMultiProcess(game_data, destinyutils._addPrimarySecondaryHeavy)
    except Exception as e:
        logger.exception(e)
        pass

    logger.info("Writing to file")
    game_data.sort("date",inplace=True)
    game_data.to_csv(datafilename, encoding="utf-8")
    return game_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_games", default=1000, type=int)
    parser.add_argument("--datafilename", default="datafiles/data.csv")
    parser.add_argument("--gametype", default="Control")
    parser.add_argument("--start_user",default=HOOLIGAN_COMMITTEE, type=list)


    args = parser.parse_args()    

    if not os.path.exists(os.path.dirname(args.datafilename)):
        logger.error("Datafile {0} does not exist!  Try again".format(os.path.dirname(args.datafilename)))
        sys.exit(2)

    runBlogProject(start_user=args.start_user, 
        num_games=args.num_games, datafilename=args.datafilename, gametype=args.gametype)
   