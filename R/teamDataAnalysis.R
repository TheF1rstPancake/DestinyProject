#Run some quick analysis on the teamData.csv dataset

library("ggplot2")
library("doBy")
library("caret")
library('reshape2')

rmse <- function(sim, obj) {
  error <- sim - obj
  return(sqrt(mean(error^2)))
}

teamData <- read.csv("../teamData.csv")

#split the data straight down the middle into traning and test sets
#the reason we do it this way is because we need to keep games grouped together
#and this is the easiest way to do that
print("Splitting into train and test data")
teamData.train <- teamData[1:floor(nrow(teamData)/2),]
teamData.test <- teamData[(floor(nrow(teamData)/2)+1):nrow(teamData),]

victoryByHighLow <- summaryBy(standing ~ hasHighestScoringPlayer + hasLowestScoringPlayer, 
                              data = teamData, FUN=victoryRate)

highLowPlot <- ggplot(data=victoryByHighLow, 
       aes(x=factor(hasHighestScoringPlayer, labels=c("No", "Yes")),
           y = standing.victoryRate, 
           fill=factor(hasLowestScoringPlayer, labels=c("No", "Yes")))) +
  ggtitle("Victory Rate with Highest and/or Lowest Scoring Players") +
  labs(fill="Has Lowest Scoring Player", x="Has Highest Scoring Player") + 
  geom_bar(stat="identity", position="dodge")
print(highLowPlot)

grouped.byFireTeam <- summaryBy(standing ~ numberOfFireTeams, data=teamData, FUN=victoryRate)
fireteamplot <- ggplot(data=grouped.byFireTeam, 
       aes(x=numberOfFireTeams, y=standing.victoryRate, fill=factor(numberOfFireTeams))) + 
  ggtitle("Victory Rate by Number Of Fireteams On Team") + 
  labs(fill="Number Of Fire Teams", x="Number of Fire Teams") + geom_bar(stat='identity')
print(fireteamplot)

teamData$numberOfExoticsCut <- cut(teamData$numberOfExotics, c(-Inf,seq(0,50,2),Inf))
grouped.byNumberExotic <- summaryBy(standing ~ numberOfExoticsCut, data=teamData, FUN=victoryRate)
exoticPlot <- ggplot(data=grouped.byNumberExotic, 
                       aes(x=numberOfExoticsCut, y=standing.victoryRate, fill=factor(numberOfExoticsCut))) + 
  ggtitle("Victory Rate by Number Of Exotics used By Team") + 
  labs(fill="Number of Exotics", x="Number of Exotics") + geom_bar(stat='identity')
print(exoticPlot)

teamData$numberOfLegendariesCut <- cut(teamData$numberOfLegendaries, c(-Inf,seq(0,50,2), Inf))
grouped.byNumberLegendary <- summaryBy(standing ~ numberOfLegendariesCut, data=teamData, FUN=victoryRate)
legendaryPlot <- ggplot(data=grouped.byNumberLegendary, 
                     aes(x=numberOfLegendariesCut, y=standing.victoryRate, fill=factor(numberOfLegendariesCut))) + 
  ggtitle("Victory Rate by Number Of Legendaries used By Team") + 
  labs(fill="Number of Legendaries", x="Number of Legendaries") + geom_bar(stat='identity')
print(legendaryPlot)

teamData$heavyWeaponCut <- cut(teamData$weaponKillsHeavy, c(-Inf,seq(0,20,2), Inf))
grouped.byHeavy <- summaryBy(standing ~ heavyWeaponCut, data=teamData, FUN=victoryRate)
heavyPlot <- ggplot(data=grouped.byHeavy, 
                     aes(x=heavyWeaponCut, y=standing.victoryRate, fill=factor(heavyWeaponCut))) + 
  ggtitle("Victory Rate by Heavy Weapon Kills") + 
  labs(fill="Number Of Heavy Weapon Kills", x="Number of Heavy Weapon Kills") + 
  geom_bar(stat='identity')
print(heavyPlot)

killsDeathsRatio <- hist(teamData$killsDeathsRatio)
teamData$killsDeathsRatioCut <- cut(teamData$killsDeathsRatio, c(-Inf,seq(0,2,.5),Inf))
grouped.byKDR <- summaryBy(standing ~ killsDeathsRatioCut, data = teamData, FUN=victoryRate)

#get rid of the first row.  A KDR of 0 has a 100% chance of winning because of wierd reasons
grouped.byKDR <- grouped.byKDR[2:nrow(grouped.byKDR), ]
kdrPlot <- ggplot(data=grouped.byKDR, 
                  aes(x=killsDeathsRatioCut, y=standing.victoryRate,fill=factor(killsDeathsRatioCut))) +
  ggtitle("Victory Rate by Kill Death Ratio")+
  labs(fill="Kill Death Ratio", x="Kill Death Ratio") +
  geom_bar(stat='identity')
print(kdrPlot)

#look at secondary as related to map
secondaryWeaponBreaks = c(-Inf, seq(0,20,5), Inf)

teamData$weaponKillsFusionRifleCut <- cut(teamData$weaponKillsFusionRifle, secondaryWeaponBreaks)
teamData$weaponKillsShotgunCut <- cut(teamData$weaponKillsShotgun, secondaryWeaponBreaks)
teamData$weaponKillsSniperCut <- cut(teamData$weaponKillsSniper, secondaryWeaponBreaks)

grouped.byMapAndSecondary <- summaryBy(standing ~ refrencedId +
                                         weaponKillsShotgunCut +
                                         weaponKillsSniperRifleCut, data=teamData, FUN=victoryRate)

####################
#Do predictions
formula <- standing ~ characterLevel + combatRating + killsDeathsRatio + defensiveKills +
  offensiveKills + objectivesCompleted + killsDeathsAssists + refrencedId + team + 
  hasHighestScoringPlayer + hasLowestScoringPlayer + weaponKillsSuper + numberOfFireTeams +
  numberOfExotics + numberOfLegendaries + combatRatingStd + weaponKillsHeavy + players

#10 fold CV 
print("Running 10 fold CV")
fitControl <- trainControl(method='repeatedcv', 
                           number=10, 
                           repeats=1,
                           verbose=TRUE)

fit1<-train(formula,
            data=teamData.train,
            method='gbm',
            trControl = fitControl,
            verbose=FALSE
)

print("Making predictions")
predictions <- predict(fit1, teamData.test, type="raw")

data.predictions <- data.frame(standing= predictions, id = teamData.test$X, gameId = teamData.test$gameId)

rootMeanError <- rmse(data.predictions$standing, teamData.test$standing)
print(rootMeanError)

write.csv(data.predictions, "predictions_raw.csv", row.names=FALSE)


#look at kill ratios per map
#basically take the total number of kills with one type of weapon versus the total number of kills
#group them by map and victory and look for trends

#get the total number of kills per map and standing (0 for victory, 1 for defeat)
killsPerMap <- summaryBy(kills ~ refrencedId + standing, data= teamData, FUN=sum)

#sniper usage
sniperUsageByMap <- summaryBy(weaponKillsSniper ~ refrencedId + standing, data = teamData, FUN=sum)
sniperUsageByMap$mapName <- unlist(lapply(sniperUsageByMap$refrencedId, 
                                          FUN = function(x){getMapName(destiny.manifest,x)}))
sniperUsagePlot <- ggplot(data=sniperUsageByMap, 
                          aes(x=mapName, y=weaponKillsSniper.sum/killsPerMap$kills.sum, fill=factor(standing, labels=c('Winner', 'Loser')))) +
  geom_bar(stat='identity', position='dodge') +
  labs(x='Map Name', fill='Team', y="Number Of Sniper Kills / Total Kills") +
  ggtitle("Sniper Ratio by Map and Team")+
  theme(axis.text.x = element_text(angle = 90, hjust = 1))
plot(sniperUsagePlot)

#hand cannon usage
handCannonUsage <- summaryBy(weaponKillsHandCannon ~refrencedId + standing, data = teamData, FUN=sum)
handCannonUsage$mapName <- unlist(lapply(handCannonUsage$refrencedId, 
                                          FUN = function(x){getMapName(destiny.manifest,x)}))

print(ggplot(data=handCannonUsage, 
             aes(x=mapName, y=weaponKillsHandCannon.sum / killsPerMap$kills.sum, fill=factor(standing,labels=c('Winners','Loosers'))))+
        geom_bar(stat='identity', position = 'dodge') +
        labs(x='Map Name', y = 'Hand Cannon Kills / Total Kills', fill='Standing') + 
        ggtitle('Victory Rate by Hand Cannon Usage')+
        theme(axis.text.x = element_text(angle = 90, hjust = 1)))

pulseRifleUsage <- summaryBy(weaponKillsPulseRifle ~ refrencedId + standing, data = teamData, FUN=sum)
pulseRifleUsage$mapName <- unlist(lapply(pulseRifleUsage$refrencedId, 
                                         FUN = function(x){getMapName(destiny.manifest,x)}))

print(ggplot(data=pulseRifleUsage, 
             aes(x=mapName,
                 y=weaponKillsPulseRifle.sum/killsPerMap$kills.sum, 
                 fill=factor(standing,labels=c('Winners','Losers'))))+
        geom_bar(stat='identity', position='dodge') +
        ggtitle('Victory Rate by Pulse Rifle Usage') +
        labs(x='Map Name', y = 'Pulse Rifle Kills / Total Kills', fill='Standing') + 
        theme(axis.text.x = element_text(angle = 90, hjust = 1)))

