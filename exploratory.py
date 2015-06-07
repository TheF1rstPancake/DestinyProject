# coding: utf-8
import pandas as pd
data = pd.read_csv("data.csv")
import destinyPlatform as destiny
import destinyPlatform as destiny
destiny.fetchMainfest()
destiny.fetchManifest()
import sqlite3
dir()
mostUsedWeaponLengths = [{k:len(mostUsedWeapon.groups[k])} for k in list(mostUsedWeapon.groups.keys())]
mostUsedWeapon = data.groupby("mostUsedWeapon1")
mostUsedWeaponLengths = [{k:len(mostUsedWeapon.groups[k])} for k in list(mostUsedWeapon.groups.keys())]
mostUsedWeaponLengths = [{"hash":k,"length":len(mostUsedWeapon.groups[k])} for k in list(mostUsedWeapon.groups.keys())]
max(mostUsedWeaponLengths, 5)
max(mostUsedWeaponLengths, 1)
max(mostUsedWeaponLengths)
max(mostUsedWeaponLengths,1)
max(mostUsedWeaponLengths, lambda x: x['length'])
max(mostUsedWeaponLengths, key = lambda x: x['length'])
max(mostUsedWeaponLengths,10,  key = lambda x: x['length'])
max(mostUsedWeaponLengths,10,key = lambda x: x['length'])
import heapq
heapq.nlargest(10,mostUsedWeaponLengths, key=lambda x:x['length'])
topTenWeapons = heapq.nlargest(10,mostUsedWeaponLengths, key=lambda x:x['length'])
topTenWeapons = sorted(topTenWeapons)
topTenWeapons
topTenWeapons = sorted(topTenWeapons, key='length')
topTenWeapons = sorted(topTenWeapons, key=lambda x: x['length'])
topTenWeapons
destiny_conn = sqlite3.connect('world_sql_content_1defc252b5033da365706c01ad24af74.content')
destiny_cursor = destiny_conn.cursor()
get_ipython().magic(u'cls ')
topTenWeapons
topTenWeapons[-1]
topTenWeapons[-1]['hash']
destiny_cursor.execute("select "+str(topTenWeapons[-1]['hash']) +" from DestinyInventoryItemDefinition")
destiny_cursor.fetchone()
destiny_cursor.execute("select "+str(int(topTenWeapons[-1]['hash'])) +" from DestinyInventoryItemDefinition")
destiny_cursor.fetchone()
destiny_cursor.execute("SELECT * FROM DestinyInventoryItemDefinition where id="+str(int(topTenWeapons[-1]['hash'])))
destiny_cursor.fetchone()
topTenWeapons[-1]['hash']
int(topTenWeapons[-1]['hash'])
str(int(topTenWeapons[-1]['hash']))
destiny_cursor.execute("SELECT * FROM DestinyInventoryItemDefinition where id="+str(int(topTenWeapons[-2]['hash'])))
destiny_cursor.fetchone()
destiny_cursor.execute("SELECT * FROM DestinyInventoryItemDefinition"))
destiny_cursor.execute("SELECT * FROM DestinyInventoryItemDefinition")
destiny_cursor.fetchall()
db = pd.DataFrame.from_records(destiny_cursor.fetchall())
db
destiny_cursor.execute("SELECT * FROM DestinyInventoryItemDefinition")
db = pd.DataFrame.from_records(destiny_cursor.fetchall())
db
db.columns
head(db)
db.head()
db.columns = ['id', 'description']
db.head()
db[db['id'] == int(topTenWeapons[-1])]
db[db['id'] == int(topTenWeapons[-1]['hash'])]
db[db['id'] == int(topTenWeapons[-2]['hash'])]
db[db['id'] == int(topTenWeapons[-3]['hash'])]
db[db['id'] == int(topTenWeapons[-4]['hash'])]
db[db['id'] == int(topTenWeapons[-5]['hash'])]
db[db['id'] == int(topTenWeapons[-6]['hash'])]
db[db['id'] == int(topTenWeapons[-7]['hash'])]
db[db['id'] == int(topTenWeapons[0]['hash'])]
db[db['id'] == int(topTenWeapons[1]['hash'])]
db[db['id'] == int(topTenWeapons[2]['hash'])]
db[db['id'] == int(topTenWeapons[3]['hash'])]
db[db['id'] == int(topTenWeapons[4]['hash'])]
db[db['id'] == int(topTenWeapons[5]['hash'])]
db[db['id'] == int(topTenWeapons[6]['hash'])]
db[db['id'] == int(topTenWeapons[7]['hash'])]
topTenWeapons
db[db['id'] == -int(topTenWeapons[-1]['hash'])]
import requests
invetoryItemBase = "http://www.bungie.net/Platform/Destiny/Manifest/invntoryItem/"
r = requests.get(invetoryItemBase + str(int(topTenWeapons[0]))
)
r = requests.get(invetoryItemBase + str(int(topTenWeapons[0]['hash'])))
r.json()
invetoryItemBase = "http://www.bungie.net/Platform/Destiny/Manifest/inventoryItem/"
r = requests.get(invetoryItemBase + str(int(topTenWeapons[0]['hash'])))
r
r.json()
suros = r.json()
suror
suros
get_ipython().magic(u'cls ')
suros['Response']['data'].keys()
suros['Response']['data']['inventoryItem']
suros_bucketType = suros['data']['inventoryItem']['bucketTypeHash']
suros_bucketType = suros['Response']['data']['inventoryItem']['bucketTypeHash']
suros_bucketType
destiny_cursor.executeexecute("SELECT * FROM DestinyInventoryBucketDefinition WHERE id="+str(suros_bucletType))
destiny_cursor.execute("SELECT * FROM DestinyInventoryBucketDefinition WHERE id="+str(suros_bucletType))
destiny_cursor.execute("SELECT * FROM DestinyInventoryBucketDefinition WHERE id="+str(suros_bucketType))
destiny_cursor.fetchall
destiny_cursor.fetchall()
suros['Response']['data']['inventoryItem'].keys()
suros['Response']['data']['inventoryItem']['itemSubType']
game_data
data
data["mostUsedWeapon1"].ix[1]
suros['Response']['data']['inventoryItem'].keys()
get_ipython().magic(u'cls ')
import imp
import destinyPlatform as destiny
import DestinyBlogProject as destinyBlog
game_data= destinyBlog._addWeaponNameAndTypeInfo(data)
import destinyPlatform as destiny
imp.reload(destiny)
imp.reload(destinyBlog)
game_data = destinyBlog._addWeaponNameAndTypeInfo(data)
imp.reload(destinyBlog)
imp.reload(destiny)
game_data = destinyBlog._addWeaponNameAndTypeInfo(data)
r = requests.get("http://www.bungie.net/Platform/Destiny/Manifest/inventoryItem/144553854/")
r.json()
imp.reload(destiny)
imp.reload(destinyBlog)
game_data = destinyBlog._addWeaponNameAndTypeInfo(data)
get_ipython().magic(u'cls ')
imp.reload(destinyBlog)
imp.reload(destiny)
game_data = destinyBlog._addWeaponNameAndTypeInfo(data)
get_ipython().magic(u'cls ')
topTenWeapons
data[data['mostUsedWeapon1"] == 0 && data['kills'] == 0]
data[data['mostUsedWeapon1"] == 0 & data['kills'] == 0]
data[data['mostUsedWeapon1"]]
data[data['mostUsedWeapon1'] && data['kills'] == 0]
data[data['mostUsedWeapon1'] & data['kills'] == 0]
data[data['mostUsedWeapon1']==0 && data['kills'] == 0]
data[data['mostUsedWeapon1']==0 & data['kills'] == 0]
data[data['mostUsedWeapon1']==0 and data['kills'] == 0]
data[data['mostUsedWeapon1']==0]
data = pd.read_csv("data.csv")
mostUsed0 = data[data['mostUsedWeapon1']==0]
mostUsed0[mostUsed0['kills'] == 0]
killsAndMostUsed0 = mostUsed0[mostUsed0['kills'] == 0]
head(killsAndMostUsed0)
killsAndMostUsed0.head()
len(killsAndMostUsed0)
len(killsAndMostUsed0)/len(data)
float(len(killsAndMostUsed0))/float(len(data))
topTenWeapons = heapq.nlargest(11,mostUsedWeaponLengths, key=lambda x:x['length'])
topTenWeapons
topTenWeapons = sorted(topTenWeapons, key = lambda x:-x['length'])
topTenWeapons
topTenWeapons.remove(0)
topTenWeapons.remove(3)
topTenWeapons[3]
topTenWeapons[2]
topTenWeapons.remove(topTenWeapons[2])
topTenWeapons
imp.reload(destiny)
sum = 0
for w in topTenWeapons:
    sum = sum + w['length']
    
sum
sum/len(data)
float(sum/len(data))
float(sum)/len(data))
float(sum)/len(data)
topWeapons = heapq.nlargest(15,mostUsedWeaponLengths, key=lambda x:x['length'])
topWeapons = [d for d in topWeapons if d['hash'] != 0
]
topWeapons
sum(d['length'] for d in topWeapons)
sum(topWeapons)
topWeapons
sum(d['length'] for d in topWeapons)
sum([d['length'] for d in topWeapons])
d for d in topWeapons
print(d for d in topWeapons)
print
print([d for d in topWeapons])
print([d['length'] for d in topWeapons])
sum([d['length'] for d in topWeapons])
sum = None
sum([d['length'] for d in topWeapons])
get_ipython().magic(u'reset_selective sum')
sum([d['length'] for d in topWeapons])
topWeapons
sum([d['length'] for d in topWeapons])/len(data)
float(sum([d['length'] for d in topWeapons]))/len(data)
for d in topWeapons:
    definition= destiny.getInventoryItemOnline(d['hash'])
    d['name'] = definition['Response']['data']['inventoryItem']['itemName']
    
topWeapons
for d in topWeapons:
    d['tierTypeName'] = definition['Response']['data']['inventoryItem']['tierTypeName']
    d['bucketTypeHash'] = definition['Response']['data']['inventoryItem']['bucketTypeHash']
    
topWeapons
topWeapons = pd.DataFrame.from_records(topWeapons)
topWeapons
for d in topWeapons:
    definition= destiny.getInventoryItemOnline(d['hash'])
    d['bucketTypeHash'] = definition['Response']['data']['inventoryItem']['bucketTypeHash']
    d['tierTypeName'] = definition['Response']['data']['inventoryItem']['tierTypeName']
    
imp.reload(destinyBlog)
topWeapons = destinyBlog._addWeaponNameAndTypeInfo(topWeapons)
clear
get_ipython().magic(u'ls ')
dir
topWeapons
r = destiny.getInventoryItemOnline(topWeapons['hash'][1])
r
topWeapons
del(topWeapons['mostUsedWeapon1Name'])
del(topWeapons['mostUsedWeapon1Type'])
del(topWeapons['mostUsedWeapon1Tier'])
dir
get_ipython().magic(u'ls ')
clear
get_ipython().magic(u'cls ')
topWeapons
del(topWeapons['bucketTypeHash'])
del(topWeapons['tierTypeName'])
get_ipython().magic(u'cls ')
topWeapons
groupedByWeapon = data.groupby("mostUsedWeapon1")
groupedByWeapon.mostUsedWeapon1
groupedByWeapon.mostUsedWeapon1()
groupedByWeapon
groupedByWeapon.groups
groupedByWeapon.get_group(topWeapons[0]['hash
groupedByWeapon.get_group(topWeapons[0]['hash'])
groupedByWeapon.get_group(topWeapons['hash'][0])
weapon1 = groupedByWeapon.get_group(topWeapons['hash'][0])
mean(weapon1['standing'])
avg(weapon1['standing'])
weapon1['standing'].mean()
data['standing'].mean()
victoryByWeapon = [{'hash':k, 'rate':1-groupedByWeapon.get_groups(k)['standing'].mean()} for k in topWeapons['hash']]
victoryByWeapon = [{'hash':k, 'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} for k in topWeapons['hash']]
victoryByWeapon
victoryByWeapon = [{'hash':k, 'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} for k in topWeapons['hash']]
topWeapons.index = topWeapons['hash']
victoryByWeapon = [{'hash':k, 'names':topWeapons[k]['names'], 'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} for k in topWeapons['hash']]
victoryByWeapon = [{'hash':k, 'names':topWeapons['names'].ix(k), 'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} for k in topWeapons['hash']]
topWeapons
victoryByWeapon = [{'hash':k, 'names':topWeapons['name'].ix(k), 'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} for k in topWeapons['hash']]
victoryByWeapon
victoryByWeapon = [{'hash':k, 'names':topWeapons['name'].ix[k], 'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} for k in topWeapons['hash']]
victoryByWeapon
topWeapons
