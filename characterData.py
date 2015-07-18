import pandas as pd
import destinyPlatform as destiny
import sqlite3
import argparse
import multiprocessing
import logging
import sys
import requests
import json
import time
import itemHashes

logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(levelname)1.1s %(asctime)s %(module)s %(process)d]:%(lineno)d %(message)s", "%y%m%d %H:%M:%S")


if 'ch' not in logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    ch.name ='ch'
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

if 'filehandler' not in logger.handlers:
    filehndlr = logging.FileHandler("character_log.log")
    filehndlr.name = 'filehandler'
    filehndlr.setLevel(logging.DEBUG)
    filehndlr.setFormatter(formatter)
    logger.addHandler(filehndlr)

#load item definitions
c = destiny.MANIFEST_CONN.cursor()


def getCharacterData(membershipId, clanName, grimoireScore, c):
	"""
	Pull out information for one character

	:param membershipId: 	the membershipId that this character belongs to
	:param clanName:		name of the clan this member belongs to
	:param grimoireScore:	member's grimoire score
	:param c:			 	the json object holding this character's information

	.. note::
		The first three parameters are member specific.  They **do not** change for each character belonging to a particular member.

	"""

	if 'characterBase' not in c:
		logger.warning("Character does not have all info.  Returning empty dict")
		return {}

	logger.info("Gathering character data for {0}".format(c['characterBase']['characterId']))
	characterData = {}
		
	#place membership specific items with each character
	#we can do a groupby object later to get membership details
	#logger.info("Adding membershipId")
	characterData['membershiId'] = membershipId
	characterData['clanName'] = clanName
	characterData['grimoireScore'] = grimoireScore

	#logger.info("Getting emblem")
	characterData['emblemHash'] = c['emblemHash']
	characterData['level'] = c['characterLevel']

	#get the character's class, race and gender
	#logger.info("Getting class,race, and gender")
	characterData['class'] = destiny.CLASS_HASH[c['characterBase']['classHash']]
	characterData['race'] = destiny.RACE_HASH[c['characterBase']['raceHash']]
	characterData['gender'] = destiny.GENDER_HASH[c['characterBase']['genderHash']]

	#get other keys straight from the character base.  No extra logic necessary
	#logger.info("Getting characterBase info")
	characterData['characterId'] = c['characterBase']['characterId']
	characterData['buildStatGroupHash'] = c['characterBase']['buildStatGroupHash']
	characterData['classType'] = c['characterBase']['classType']
	characterData['wearHelmet'] = c['characterBase']['customization']['wearHelmet']
	characterData['minutesPlayedTotal'] = c['characterBase']['minutesPlayedTotal']
	characterData['minutesPlayedThisSession'] = c['characterBase']['minutesPlayedThisSession']
	characterData['dateLastPlayed'] = c['characterBase']['dateLastPlayed']
	
	#get all of the stat values for this character
	#this is things like discipline, strength, intellect, agility, etc.
	for k in c['characterBase']['stats']:
		characterData[k] = c['characterBase']['stats'][k]['value']

	#parse the peerview
	#this tells us what the character has currently equipped in each visible slot.
	#This gets us all armor and weapons and gets us shader, ship, sparrow, and class item
	peerView = c['characterBase']['peerView']['equipment']

	#build a list of all the items the player currently has equipped
	peerViewItems = [itemHashes.ITEM_HASH[d['itemHash']] for d in peerView]
	#peerViewItems = [destiny.getItemFromManifest(d['itemHash'], "DestinyInventoryItemDefinition") for d in peerView]

	#then, for each item, map the bucket name for that item to the item name, tier, hash, and type
	characterData.update({itemHashes.BUCKET_HASH[i['bucketTypeHash']]['bucketName']				: i['itemName'] for i in peerViewItems})
	characterData.update({itemHashes.BUCKET_HASH[i['bucketTypeHash']]['bucketName'] + " Tier"	: i['tierTypeName'] for i in peerViewItems})
	characterData.update({itemHashes.BUCKET_HASH[i['bucketTypeHash']]['bucketName'] + " Hash" 	: i['itemHash'] for i in peerViewItems})
	characterData.update({itemHashes.BUCKET_HASH[i['bucketTypeHash']]['bucketName'] + " Type"	: i['itemTypeName'] for i in peerViewItems})

	return characterData

def getDataForAllCharacters(membershipId):
	logger.info("Attemping to get characters for {0}".format(membershipId))
	
	try:
		characterInfo = destiny.getCharacterInfo(membershipId)
	except destiny.BadRequestError as e:
		logger.warning("Received bad request error for {0}. Skipping this member.".format(membershipId))
		return pd.DataFrame()
	except destiny.NoDataError as e:
		logger.warning("Recieved no data error for member {0}. Skipping this member".format(membershipId))
		return pd.DataFrame()
	except requests.exceptions.ConnectionError as e:
		logger.warning("Received Connection error for {0}.  Pausing and skipping member".format(membershipId))
		logger.warning(e.message)
		time.sleep(60)
		return pd.DataFrame()	

	logger.info("Successfully received data!")
	membershipDetails = characterInfo['Response']['data']

	#characterDetails will have the info for every character 
	#associated with this membership membershipId
	#we want to build a dictionary of key value pairs
	#that we will eventually turn into a dataframe

	clanName = membershipDetails.get("clanName", "None")
	grimoireScore = membershipDetails.get("grimoireScore", 0)

	#get the list of characters and all of their info	
	characters = characterInfo['Response']['data']['characters']

	#pull the info out and put it into this array
	characterDetails = [getCharacterData(membershipId, clanName, grimoireScore, c) for c in characters]

	return characterDetails

def mineCharacterData(membershipIds):
	"""
	Given a list of membership Ids, build a dataframe representing all of their characters

	:param membershipIds:	list of membership Ids
	"""

	records = []
	counter = 0
	for mem_id in membershipIds:
		counter=counter+1
		logger.info("Membership: {0}".format(counter))
		try:
			records.extend([d for d in getDataForAllCharacters(mem_id) if d is not None])
		except Exception as e:
			logger.exception("Craziness has happened.  Dumping what we have.")
			pass

	data = pd.DataFrame(records).convert_objects(convert_numeric=True)
	return data

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def buildCharacterDataset(membershipIds):
	"""
	Given a list of membership Ids, create a pool of processes to get all of their character data
	"""

	logger.info("Going to get info for {0} members".format(len(membershipIds)))

	#create pool
	p = multiprocessing.Pool(4)

	#partition membershipIds into a list of lists
	logger.info("Partitioning data")
	partitions = chunks(membershipIds, 8)

	logger.info("Fetching data!")
	mapped_list = p.map(mineCharacterData, partitions)

	#mapped_list contains a list of dataframes, concat them all and return the file
	logger.info("Adding all dataframes to one object")
	data = pd.concat(mapped_list, ignore_index=True)

	logger.info("Dropping duplicates")
	data = data.drop_duplicates()
	return data

def runGetData(datafile):
	data = pd.read_csv(datafile)

	membershipIds = list(data['membershipId'].unique())

	logger.info("Successfully loaded hashes:\n\tITEM HASH: \t{0}\n\tBUCKET_HASH: \t{1}".format(len(itemHashes.ITEM_HASH), len(itemHashes.BUCKET_HASH)))

	#clear data from memory.
	data = None
	data = buildCharacterDataset(membershipIds)

	return data
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--datafile", default="datafiles/data.csv", help="Datafile to pull membership Ids from")
	parser.add_argument("--outputfile", default="datafiles/character_data.csv")

	args = parser.parse_args()

	data = runGetData(args.datafile)
	
	logger.info("Successfully gathered data. Writing to {0}".format(args.outputfile))
	data.to_csv(args.outputfile, encoding="utf-8")	

