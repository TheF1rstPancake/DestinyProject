#connect to the local copy of the destiny manifest

library("RSQLite")
library("RJSONIO")
sqlite <- dbDriver("SQLite")
destiny.manifest <- dbConnect(sqlite, "manifest/world_sql_content_5c414893dac0deb1f473b74243454790.content")
dbListTables(destiny.manifest)

getMapInfo <- function(database, hash) {
  queryString = paste("select * from DestinyActivityBundleDefinition where id = '", 
                      hash, "'", sep="")
  response <- dbGetQuery(database, queryString)
  
  return (response)

}

getMapName <- function(database,hash) {
  mapInfo <- getMapInfo(database,hash)
  if (length(mapInfo$json) == 0){
    json <- fromJSON(paste("http://www.bungie.net/Platform/Destiny/Manifest/activity/",
                           hash,"/", sep=""))
    return (json$Response$data$activity$activityName)
  }
  json <- fromJSON(mapInfo$json)
  
  return (json$activityName)
  
}