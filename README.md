# Destiny Data Analysis

All of this code is meant to be used to examine data from Bungie's Destiny.
Bungie provides a REST API for accessing basically all the data that you could possibly want.

## Overview

This repo contains a lot of different code files all meant to do different things.
This was more an expiriment on how to get data out of the REST API.

### Base

The destinyPlatform.py file contains the basic functions necessary to pull data out of the API

### Data Analysis

The DestinyBlogProject.py, teamBuilding.py, extra_anlysis.py, and predict.py were created to do some analysis on Crucible data.
The results from these procedures can be found at this repo's gh-pages site.

http://jalepeno112.github.io/DestinyProject/CrucibleDataAnalysis.html

### Tornado Server

server.py, index.html, and postgamestats.html were an expirement in running a Tornado webserver and using the destinyPlatform.py underneath.

### Datafiles

Probably the most useful thing in this repo.  Under the datafiles directory	there are two large csv files:
	- data.csv
	- teamData.csv

data.csv contains over 160,000 rows and 60 columns taken from about 11,500 games.  Each row is a different player, and every column a different feature.
teamData.cssv split data.csv into games and then merged each team into one vector, so its only about 23,000 rows (11,500 *2) and 60 columns.

