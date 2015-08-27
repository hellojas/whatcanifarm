library("rnoaa")
setwd("~/school/green_farms")

##################################### 
# merge data by zip and county and fips
##################################### 
farms <- read.csv("organic_farms_list.csv", header=TRUE, sep=",")
zipToCounty <- read.csv("zip_county.csv", header=TRUE, sep=",")
countyToFips <- read.csv("SameCode.txt", header=FALSE, sep=",")
# merge farms and county
farmsWithCounty <- merge(farms, zipToCounty, by.x="Zip_Code",by.y="ZIP",all=FALSE)
write.csv(farmsWithCounty, "organic_farms_list_with_county.csv")


##################################### 
# start with new farms with fips county
##################################### 

farms <- read.csv("organic_farms_list_with_county.csv",header=TRUE,sep=",")
countiesAll <- farms$County
data <- ncdc_stations(datasetid='GHCND', locationid=paste("FIPS:",farms$County[123],sep=""))

##################################### 
# get annual weather data for each
# fips code and sae it to csv
##################################### 
counties <- unique(farms$County)
setwd("~/school/green_farms/weather_county_annual_2015")

err <- list()
# get negative -(1:lastEnd)
for(fips in counties) { 
  print(fips)
  annual <- ncdc(datasetid='ANNUAL',locationid=paste("FIPS:",fips,sep=""),startdate = '2015-01-01', enddate = '2015-12-30', limit=1000)
  data <- annual$data
  if (is.null(data)) {
    err<-c(err,fips)
  } else {
    splitByStation <- split(data, data$station)
    
    for (station in splitByStation) {
      keys<-paste(substr(annual$data$date,1,10),annual$data$datatype,sep="_")
      vals <-paste(annual$data$value)
      valDf <- as.data.frame(t(vals))
      colnames(valDf) <- keys
      row.names(valDf) <- c(fips)
      write.csv(valDf,paste(fips,"_",gsub(":","_",station$station[1]),".csv",sep=""))
    }
  }
  Sys.sleep(5)
}


##################################### 
# test
##################################### 

ncdcLocs <- ncdc_locs(locationcategoryid='CITY', sortfield='name', sortorder='desc')
ncdc_locs(locationcategoryid='ZIP', sortfield='name', sortorder='desc')

locationId <- paste("FIPS",farmsWithCounty)
ncdc_stations(datasetid='GHCND', locationid='FIPS:12017')

zip_91344 <- ncdc(datasetid = 'PRECIP_HLY', locationid = 'ZIP:28801', datatypeid = 'HPCP', limit = 5)
ncdc_datacats(locationid='CITY:US91344')

out <- ncdc(datasetid='NORMAL_DLY', stationid='GHCND:USW00014895', datatypeid='dly-tmax-normal', startdate = '2014-01-01', enddate = '2014-12-30')
out <- ncdc(datasetid='NORMAL_DLY', stationid='GHCND:USW00014895', datatypeid='dly-tmax-normal', startdate = '2010-05-01', enddate = '2010-05-10')
ncdc(datasetid='ANNUAL',stationid='GHCND:USC00300961', startdate = '2010-01-01', enddate = '2010-12-30')
ncdc(datasetid='ANNUAL',stationid='GHCND:USC00300961', startdate = '2014-01-01', enddate = '2014-12-30')


ncdc_datacats(locationid=paste("FIPS:",farms$County[123],sep=""))


