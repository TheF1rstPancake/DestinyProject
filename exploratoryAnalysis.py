"""
Do some exploratory data analysis on the dataset we built from the Destiny Platform API
This does not produce any graphs, but builds other datasets that can then be loaded into other applications such as R and D3

Ideally, I could do this all in R, but I have a lot more experience with pandas and Python which makes it easier to do here.
"""

import pandas as pd
import destinyPlatform as destiny
import destinyPlatform as destiny
import sqlite3
import heapq


def exploratoryAnalysis():
	#load data
	data = pd.read_csv("data.csv")

	#fetch the destiny manifest.  Just to make sure we have it and it is the most update version
	destiny.fetchManifest()

	groupedByWeapon = data.groupby("mostUsedWeapon1")

	#get the number of times each weapon was used in the game
	mostUsedWeaponLengths = [{"hash":k,
		"length":len(groupedByWeapon.groups[k])} 
	for k in list(groupedByWeapon.groups.keys())]

	#get the 15 most used weapons
	#We grab 16 because one of the larger weapon hashes is 0
	#0 is a number we stuck in the dataset when building it to indicate that this information wasn't available for that user
	topWeapons = heapq.nlargest(16,mostUsedWeaponLengths, key=lambda x:x['length'])
	topWeapons = [d for d in topWeapons if d['hash'] != 0]

	for d in topWeapons:
		definition = destiny.getInventoryItemOnline(d['hash'])
		d['name'] = definition['Response']['data']['inventoryItem']['itemName']
	topWeapons = pd.DataFrame.from_records(topWeapons)
	topWeapons.index = topWeapons['hash']


	victoryByWeapon = [{'hash':k, 
		'names':topWeapons['name'].ix[k], 
		'rate':1-groupedByWeapon.get_group(k)['standing'].mean()} 
	for k in topWeapons['hash']]

if __name__ == "__main__":
	exploratoryAnalysis()
