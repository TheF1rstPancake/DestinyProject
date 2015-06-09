#Do exploratory data analysis on the data pulled from the Destiny Platform REST API
#This relies on files we created doing exploratory anaylsis in Python
#This file is different than the Python one because this one will generate plots

library("ggplot2")
library("doBy")

#load functions created to access the Destiny SQLite database
source('~/CSCI183/DestinyBlogProject/manifestConnect.R')

#within the dataset, 0 is victory, 1 is defeat
#if we take the mean of the standing column, we get DEFEAT RATE
#we want VICTORY RATE, so subtract 1 from DEFEAT RATE
victoryRate <- function(x) {
  return(1-mean(x))
}

data <- read.csv("../datafiles/data.csv")

grouped.byWeapon <- summaryBy(X ~ mostUsedWeapon1Name, data = data, FUN=length)
grouped.byWeapon <- grouped.byWeapon[order(grouped.byWeapon$X.length), ]

topWeapons <- tail(grouped.byWeapon, 16)
topWeapons <- subset(topWeapons, topWeapons$mostUsedWeapon1Name != 'None')

#create plot for how often the top 15 weapons are used
print(ggplot(data = topWeapons, 
             aes(x=mostUsedWeapon1Name, y=X.length/nrow(data), fill=mostUsedWeapon1Name)) + 
        geom_bar(stat='identity') + 
        ggtitle("Top 15 Weapons Used") + 
        labs(x= "Weapon Name", y="Usage Rate", fill="Weapon Name")+
        theme(axis.text.x = element_text(angle = 90, hjust = 1)))

topWeapons_sub = subset(data, data$mostUsedWeapon1Name %in% topWeapons$mostUsedWeapon1Name)
topWeaponsVictory <- summaryBy(standing ~ mostUsedWeapon1Name, data = topWeapons_sub, FUN=victoryRate)
print(ggplot(data=topWeaponsVictory,
             aes(x=mostUsedWeapon1Name, y = standing.victoryRate, fill = mostUsedWeapon1Name)) +
        geom_bar(stat='identity') +
        ggtitle("Top 15 Weapons Victory Rate")+ 
        labs(x='Weapon Name', y ='Victory Rate', fill='Weapon Name')+
        theme(axis.text.x = element_text(angle = 90, hjust = 1)))


#create plot for the rate of victory using those 15 weapons
#print(ggplot(data = topWeapons, 
#             aes(x=name, y=victoryRate, fill=name)) + 
#        geom_bar(stat='identity') + 
#        ggtitle("Victory Rate using the Top 15 Weapons") + 
#        theme(axis.text.x = element_text(angle = 90, hjust = 1)))

#look at victory rate by combat rating
combatRatingHist <- hist(data$combatRating)

data$combatRatingBins <- cut(data$combatRating, combatRatingHist$breaks)
grouped.byCombatRating <- summaryBy(standing ~ combatRatingBins, data = data, FUN=victoryRate)

print(ggplot(data=grouped.byCombatRating, 
             aes(x=combatRatingBins, y=standing.victoryRate, fill=combatRatingBins)) +
        geom_bar(stat='identity') +
        ggtitle("Victory Rate by Combat Rating") +
        theme(axis.text.x = element_text(angle = 90, hjust = 1)))


#look at map data
grouped.byMap = summaryBy(standing ~ refrencedId + team, data=data, FUN=victoryRate)
grouped.byMap = subset(grouped.byMap, grouped.byMap$team != -1)
grouped.byMap$mapName <- unlist(lapply(grouped.byMap$refrencedId, 
                                       FUN = function(x){getMapName(destiny.manifest,x)}))

print(ggplot(data=grouped.byMap, 
       aes(x=mapName, y = standing.victoryRate, fill=factor(team, labels=c("Alpha","Bravo")))) + 
  geom_bar(stat="identity", position = "dodge") +
  ggtitle("Victory Rate by Map") +
  labs(fill="Teams") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)))

grouped.byMapFreq = summaryBy(X ~ refrencedId, data = data, FUN=length)
grouped.byMapFreq$freq <- grouped.byMapFreq$X.length / nrow(data)
grouped.byMapFreq$mapName <- unlist(lapply(grouped.byMapFreq$refrencedId, 
                                       FUN = function(x){getMapName(destiny.manifest,x)}))
print(ggplot(data=grouped.byMapFreq,
             aes(x=mapName, y = freq))+
        geom_bar(stat='identity',position='dodge') +
        ggtitle("Map Frequency") +
        labs(x="Map Name", y= "Frequency")+
        theme(axis.text.x = element_text(angle = 90, hjust = 1)))

#quitting data
quitters <- subset(data, data$completed == 0)
quitters <- subset(quitters, quitters$team != -1)
groupQuitters.byMap <- summaryBy(X ~ refrencedId + team, data=quitters, FUN=length)
groupQuitters.byMap$mapName <- unlist(lapply(groupQuitters.byMap$refrencedId, 
                                           FUN = function(x){getMapName(destiny.manifest,x)}))
quitMapPlot <- ggplot(data=groupQuitters.byMap, 
                      aes(x=mapName, y=X.length, fill = factor(team, labels=c('Alpha','Bravo')))) +
  geom_bar(stat='identity', position='dodge')+
  labs(x='Map Name', fill='Team', color='Team', y="Number Of Quitters") +
  ggtitle("Quiting by Map and Team")+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
print(quitMapPlot)

