import re
import json
import yaml
import requests
import sqlite3
import zipfile
import StringIO
import os
NETWORKS = {"XBL":1, "PSN":2}                               #network names to values

#open configuration from yaml file
#user needs to create this file and add the following three fields
#   Manifest: ""
#   MANIFEST_FILE: "" 
#   API_KEY: "YOUR_API_KEY"
#All fields can be empty except YOUR_API_KEY.  :func:`fetchManifest will take care of the other 2
with open("config.yaml", 'r') as f:
        CONFIG = yaml.load(f)

HEADERS = {"X-API-Key":CONFIG['API_KEY']}  #headers we need to add to the request


CLASS_HASH = {                                              #the hash for class types
                2271682572: 'Warlock',
	            671679327: 'Hunter',
	            3655393761: 'Titan'
             }

class NoDataError(Exception):
    pass

class BadRequestError(Exception):
    pass

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')

def upsert(base, key, dictionary):
    if key in base:
        base[key].update(dictionary)
    else:
        base[key] = dictionary
    return base

def JSONtoDict(response):
    """
    Take a urllib2 response object and loads the data into a dictionary
    """
    data = json.loads(response.read())
    
    #if there is nothing in the data['Response'] then the request did not go through properly
    #if not data['Response']:
    #    raise NoDataError

    return data


def getPvPGame(gameId):
    response = requests.get("http://www.bungie.net/platform/Destiny/Stats/PostGameCarnageReport/{0}/".format(gameId))
    if response is None:
        raise NoDataError("No data returned for game {0}".format(gameId))
    return response.json()

def getAggregateAcitivtyStats(membershipId, characterId, network='XBL', definitions=False):
    response = requests.get("http://www.bungie.net/platform/Destiny/Stats/AggregateActivityStats/1/{0}/{1}/?definitions={2}".format(membershipId,characterId,definitions))

    return response.json()

def getMembershipID(gamertag, network='XBL', definitions=False):

    #http://www.bungie.net/Platform/Destiny/SearchDestinyPlayer/{membershipType}/{tag}/
    #replace spaces with %20
    gamertag = re.sub(r' ','%20',gamertag)
    
    URL = "http://www.bungie.net/Platform/Destiny/SearchDestinyPlayer/{0}/{1}/?definitions={2}".format(NETWORKS[network],gamertag,definitions)
    response = requests.get(URL, headers=HEADERS)
    data = response.json()


    #TODO:  create destiny errors
    #if 'ErrorCode' in data:
     #   raise NoDataError(data['Message'])

    return data['Response'][0]['membershipId']

def getCharacters(membershipId, network='XBL'):
    try:
        character_info = getCharacterInfo(membershipId)
    except NoDataError as e:
        raise e

    characters = {c['characterBase']['characterId']:CLASS_HASH[c['characterBase']['classHash']]
                  for c in character_info['Response']['data']['characters']}

    return characters


def getCharacterInfo(membershipId,network='XBL'):
   response = requests.get("http://www.bungie.net/Platform/Destiny/{0}/Account/{1}/".format(NETWORKS[network],membershipId),
                           headers=HEADERS)
   data = response.json()

   return data

def getActivityHistory(membershipID, characterID, network="XBL",mode="None",count=25,page=0,definitions=False):
    network = NETWORKS[network]
    response = requests.get("http://www.bungie.net/Platform/Destiny/Stats/ActivityHistory/{0}/{1}/{2}/?mode={3}&page={4}&count={5}&definitions={6}".format(network, membershipID,characterID,mode,page,count,definitions),
                            headers= HEADERS)
    data = response.json()
    return data


def getMostRecentPvPGames(membershipID, characterID, network ="XBL", count = 25, mode=5):
    """
    Fetch the most recent PVP games for a particular character
    
    """
    history = getActivityHistory(membershipID, characterID, mode = mode, count = count)
    
    if history['ErrorStatus'] != 'Success':
        raise BadRequestError("Bad request for character {0}. \nhistory['Message']".format(characterID))
    if not history['Response']['data']:
        raise NoDataError("Data not found in activity history for character {0}".format(characterID))

    #pull the gameId for each activity in the history
    activityIDs = [e['activityDetails']['instanceId'] for e in history['Response']['data']['activities']]

    #go fetch the PostGameCarnageReport for each gameId
    recent =[requests.get("http://www.bungie.net/Platform/Destiny/Stats/PostGameCarnageReport/{0}".format(id),
                            headers=HEADERS).json() for id in activityIDs]

    return recent

def getInventoryItemOnline(itemHash):
    """
    Get a weapon's definition using the Destiny Platform REST API rather than the database
    .. note::
        this function was created because I was having a problem where item hashes were not being found in the downloaded manifest
        but were valid when passed to the REST API 

    :param itemHash:    hash of the item we want info for 
    """
    invetoryItemUrl = "http://www.bungie.net/Platform/Destiny/Manifest/inventoryitem/{0}".format(int(itemHash))

    r = requests.get(invetoryItemUrl)
    return r.json()


MANIFEST_CONN = sqlite3.connect(CONFIG['MANIFEST_FILE'])

def getItemFromManifest(table, hash):
    """
    Take a Destiny Platform hash value and look it up in the manifest

    :param table:       name of the table within the manifest we want to look in
    :param hash:        hash id value
    """
    c = MANIFEST_CONN.cursor()
    c.execute("select * from {0} where id = {1}".format(table, hash))
    response = c.fetchone()

    return respose

def fetchFile(url, local_filename):
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
    return local_filename

def fetchAndUnzip(url):
    r = requests.get(url)
        
    if r.status_code != 200:
        raise requests.HTTPError
    #unzip content
    try:
        z = zipfile.ZipFile(StringIO.StringIO(r.content))
        z.extractall()
    except:
        raise

def getMapName(hash):
    url = "http://www.bungie.net/Platform/Destiny/Manifest/activity/{0}".format(int(hash))
    r = requests.get(url)
    if r != 200:
        r.raise_for_status()
    data = r.json()
    return data['Response']['data']['activity']['activityName']

def fetchManifest():
    """
    Fetch the most recent Destiny manifest.  Returns the string pointing to the SQLite file.
    If the database is being updated, then it will fetch it and unzip it so it can be used.
    """
    response = requests.get("http://www.bungie.net/Platform/Destiny/Manifest", headers=HEADERS)
    data = response.json()

    world_manifest = data['Response']['mobileWorldContentPaths']['en']

    #get the local_filename from world_manifest.
    #world_mainfest will look like: 'content/.../en/SOMETHING_HASH.content
    #we want to use SOMETHING_HASH.content
    local_filename = world_manifest.split('/')[-1]

    #check to see if the manifest has updated
    if world_manifest != CONFIG['Manifest']:
        #download new manifest
        url = "http://www.bungie.net{0}".format(world_manifest)
        r = requests.get(url)
        
        if r.status_code != 200:
            raise requests.HTTPError

        #update the manifest in config
        CONFIG['Manifest'] = world_manifest

        #write the new config out
        with open("config.yaml", 'w') as f:
               f.write(yaml.dump(CONFIG))

        #unzip content
        try:
            z = zipfile.ZipFile(StringIO.StringIO(r.content))
            z.extractall()
        except:
            raise


    return local_filename

