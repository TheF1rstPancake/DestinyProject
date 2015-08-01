import destinyPlatform as destiny
import pandas as pd
import logging
import sys
import multiprocessing
import requests

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


def _getGame(membershipId, characterId, uniqueGameIds=[], mode='IronBanner', network='XBL'):
    #start_user_characters = destiny.getCharacterInfo(membershipId)
    #character_info = start_user_characters['Response']['data']['characters']

    logger.info("Getting most recent {0} game for {1}".format(mode, membershipId))

    #get a game
    games_to_fetch = 1
    try:
        most_recent = destiny.getMostRecentPvPGames(membershipId,characterId,
                                                count = games_to_fetch, mode=mode, network = network)
    except destiny.BadRequestError as e:
        logger.exception('BadRequestError')
        raise e
    except destiny.NoDataError as e:
        logger.exception('NoDataError')
        raise e

    #game_id is the unique identifier for the GAME
    #reference_id is the unique identifier for the MAP that the game is played on
    game_id = most_recent[0]['Response']['data']['activityDetails']['instanceId']

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
                                                   count = games_to_fetch, mode=mode, network=network)    
        except destiny.BadRequestError as e:
            logger.exception('BadRequestError')
            raise e
        except destiny.NoDataError as e:
            logger.exception('NoDataError')
            raise e
        except requests.exceptions.ConnectionError as e:
            logger.exception("ConnectionError")
            raise e
        except Exception as e:
            logger.exception("Unknown exception")
            raise e
        logger.info("Sucessfully retrieved {0} games".format(len(more_games)))
        most_recent = [more_games[-1]]
        game_id = most_recent[0]['Response']['data']['activityDetails']['instanceId'] 

    logger.info("Found game {0}".format(game_id))
    game_details = [{"gameId" : game_id, 
                        "membershipId"  : p['player']['membershipId'], 
                        "characterId"   : p['characterId'] }for p in most_recent[0]['Response']['data']['entries']]
    
    return game_details

def _findGame(next_member, next_character, game_data, network="XBL"):
    game_details = None

    #get a game.  If using the current user causes problems, then try a different user in the dataframe
    while game_details is None:
        try:
            game_details = _getGame(next_member, next_character, game_data['gameId'].unique(), network=network)
        except destiny.BadRequestError as e:
            logger.warning("Received bad request error for {0}. Trying again with different player".format(next_member))
            pass
        except destiny.NoDataError as e:
            logger.warning("Recieved no data error for {0}.  Trying again with different player".format(next_member))
            pass
        except requests.exceptions.ConnectionError as e:
            logger.warning("Received Connection error for {0}.  Pausing and trying again".format(next_member))
            logger.warning(e.message)
            time.sleep(60)
            pass
        except Exception as e:
            logger.warning("Unkown exception")
            raise
    return game_details
def randomWalk(user_membership, game_data=None, num_games = 1000):
    """
    Do a random walk through the Destiny PostGameCarnageReport

    :param user_membership:   a dictionary whose key is the membership id and value is the characterId to start the walk with
    :param gameData:          *optional*; a dataframe from a previous walk that you want to expand upon
    """

    logger.info("Starting random walk with:\n\tMember:\t\t{0}\n\tCharacter:\t{1}".format(user_membership.keys()[0], user_membership.values()[0]))

    #check if we need to initialize gameData
    if game_data is None:
        game_data = pd.DataFrame(columns=['gameId'])

    #number of games we hope to get from this user
    try:
        next_member = [k for k in user_membership.keys() if k != "Network"][0]
        next_character = user_membership[next_member]
        network = user_membership['Network']
        for i in range(num_games):
            
            #try and get a game_id
            game_details = _findGame(next_member, next_character, game_data, network=network)

            #if we don't sucessfully return a game, then we need to fix that
            #pull a random person
            if game_details is None:
                #get a random person from the dataframe and try them instead
                rand_idx = random.randrange(0,len(game_data))
                logger.info("Picking new random starting point from frame: {0}".format(rand_idx))

                if len(game_data) == 0:
                    logger.info("No other data to chose from.  Bombing out")
                    return (0,game_data)

                #get their membership id and character id
                next_member = game_data['membershipId'][rand_idx]
                next_character = game_data['characterId'][rand_idx]
            else:
                #add the new game_id in 
                game_data = pd.concat([game_data,pd.DataFrame(game_details, index = [0])], ignore_index=True)

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

def prepWalk(gamertags, network="XBL"):
    """
    Build the necessary structures to start the walk.

    :param gamertags:   List of XBL/PSN gamertags to use as anchors for the walk.
    """

    #if result comes back with a 0, then something eventually went wrong in the walk
    #go to the next user in our list in order to get data
    start_users_ids = [destiny.getMembershipID(user, network=network) for user in gamertags]

    start_user_characters = [{membershipId: characterId, "Network":network} for membershipId in start_users_ids for characterId in destiny.getCharacters(membershipId).keys()]
    return start_user_characters

if __name__ == "__main__":
    PSN_GAMERTAGS = ["Aforyea","dad-core", "nickofblades", "ItzMaddox", 
                    "DocMutes", "Potato_Slammer", "Mikro_jg", "Runpuddrun", "pwnrkill"]
    datafilename = "datafiles/PSN_GameIds.csv"

    membership_info = prepWalk(PSN_GAMERTAGS, network="PSN")

    p = multiprocessing.Pool(4)
    mapped_list = p.map(randomWalk, membership_info)
    
    #mapped_list is a list of tuples. The first item in the tuple is a 1 or 0 indicate successful completion
    #second is the dataframe
    #concat the dataframes together and then drop duplicates
    game_data = pd.concat([t[1] for t in mapped_list], ignore_index=True)

    logger.info("Dropping duplicates")
    game_data = game_data.drop_duplicates()

    logger.info("Writing to file")
    game_data.to_csv(datafilename)