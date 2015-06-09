library("ggplot2")
library("doBy")
library('caret')

rmse <- function(sim, obj) {
  error <- sim - obj
  return(sqrt(mean(error^2)))
}

#break data into train and test sets
set.seed(17)
data <- read.csv("../datafiles/data.csv")
print("Converting some columns to factors")
#convert these columns to factors glm
#col_names <- c("characterClass")
# do do it for some names in a vector named 'col_names'
#data[,col_names] <- lapply(data[,col_names] , factor)
data$characterClass <- factor(data$characterClass)
data$standing_inverse <- (data$standing *-1) + 1

print("Splitting into train and test data")
train_ind <- sample(seq_len(nrow(data)), size=.5*nrow(data))
train <- data[train_ind,]
test <- data[-train_ind,]


formula <- standing ~ characterLevel + combatRating + characterClass + orbsGathered +
  mostUsedWeapon1 + mostUsedWeapon2 + killsDeathsRatio + defensiveKills +
  offensiveKills + objectivesCompleted + killsDeathsAssists + refrencedId + team

#fit <- glm(formula, family = "gaussian", data = train)
#predictions <- predict(fit,test,type='response')

#10 fold CV 
print("Running 10 fold CV")
fitControl <- trainControl(method='repeatedcv', 
                           number=10, 
                           repeats=1,
                           verbose=TRUE)

fit1<-train(formula,
            data=train,
            method='gbm',
            trControl = fitControl,
            verbose=FALSE
)

print("Making predicitons")
predicitons <- predict(fit1, test, type="raw")

data.predictions <- data.frame(standing= round(predictions), id = test$X)

rootMeanError <- rmse(data.predictions$standing, test$standing)
print(rootMeanError)
