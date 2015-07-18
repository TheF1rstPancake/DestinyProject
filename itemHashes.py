import destinyPlatform as destiny
import requests
import json


#load item definitions
c = destiny.MANIFEST_CONN.cursor()

def _loadItemHash():
	#get all items from the manifest
	items = c.execute("select json from DestinyInventoryItemDefinition").fetchall()
	items = [json.loads(i[0]) for i in items]
	return {i['itemHash']:i for i in items}

def _loadBucketHash():
#get all items from the manifest
	items = c.execute("select json from DestinyInventoryBucketDefinition").fetchall()
	items = [json.loads(i[0]) for i in items]
	return {i['bucketHash']:i for i in items}

ITEM_HASH = _loadItemHash()
BUCKET_HASH= _loadBucketHash()