setwd("~/Dropbox/Projects.priv/dht")

require(data.table)
require(ggplot2)
require("RSQLite")

## Get season from dates
# https://stackoverflow.com/a/9501225/1898713
getSeason <- function(DATES) {
  WS <- as.Date("2012-12-21", format = "%Y-%m-%d") # Winter Solstice
  SE <- as.Date("2012-3-20",  format = "%Y-%m-%d") # Spring Equinox
  SS <- as.Date("2012-6-21",  format = "%Y-%m-%d") # Summer Solstice
  FE <- as.Date("2012-9-22",  format = "%Y-%m-%d") # Fall Equinox
  
  # Convert dates from any year to 2012 dates
  d <- as.Date(strftime(DATES, format="2012-%m-%d"))
  
  ifelse (d >= WS | d < SE, "Winter",
          ifelse (d >= SE & d < SS, "Spring",
                  ifelse (d >= SS & d < FE, "Summer", "Fall")))
}

## connect to db
con <- dbConnect(drv=RSQLite::SQLite(), dbname="dhtlog.db")

## list all tables
tables <- dbListTables(con)

## exclude sqlite_sequence (contains table information)
tables <- tables[tables != "sqlite_sequence"]

lDataFrames <- vector("list", length=length(tables))

## create a data.frame for each table
for (i in seq(along=tables)) {
  lDataFrames[[i]] <- as.data.table(dbGetQuery(conn=con, statement=paste("SELECT * FROM '", tables[[i]], "'", sep="")))
}

dt = lDataFrames[[1]]
dt[, season := getSeason(timestamp)]

summary(dt)
dt[humid < 50]
dt[temp < 10]

dt = dt[temp > 10 & humid < 100]

ggplot(dt, aes(x = temp, y = humid)) +
  geom_point(alpha = 0.1, aes(fill = season, colour = season)) +
  geom_path(alpha = .01)
