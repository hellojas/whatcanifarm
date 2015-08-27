########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	takes a folder of NOAA weather station data
# 	and returns a csv that contains each station data
# 	by count id
# @usage:
#	python concatStations.py 
#		-f [weather filename]
#		-z [nearby zips filename]
#		-o [output filename]
#######################################################


#imports
import sys
import urllib
import urllib2
import simplejson as json
import csv
import pandas as pd
import numpy as np

'''
parse options from the command line
-f contains the header information for the DataFrame
-z contains the nearby zipcodes for each zipcode
-o is the output filename
-q don't print 

@return opt, options that are parsed
@return args, extra unnparsed arguments
'''
def cmdLine():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
                  help="open header FILE", metavar="FILE")
	parser.add_option("-z", "--zip", dest="zip",
                  help="file of nearby zips", metavar="ZIP")
	parser.add_option("-o", "--out", dest="output",
                  help="OUT of final dataframe", metavar="OUT")
	parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
	(opt, args) = parser.parse_args()

	return opt, args

'''
starts with hardcoded default arguments which
you can replace or you can simply run the script
with the proper option arguments to replace them 
in the cmd line

@return weatherfile, contains feature values
@return zipsfile, contains the nearby zipcodes
@return out, output filename
'''
def setOptions():

	opt, args =  cmdLine()
	#set default locs
	weatherfile = "weather_county_full_zip_and_county.csv"
	zipsfile = "nearbyZips_simp_30miles.csv"
	out = "nearbyZips_avg_2014.csv"

	# set of cmd line args
	weatherfile = opt.filename if opt.filename else weatherfile
	zipsfile = opt.zip if opt.zip else zipsfile
	out = opt.output if opt.output else out

	return weatherfile, zipsfile, out

'''
impute values for a zipcode by averaging
the values for zipcodes within 30 miles
then replace empty values in the weather
data file with these averages

@param weather, the weather file
@param zips, the nearby zipcodes
@param out, output filename

@outputfile, weather values updated
by custom imputer method
'''
def runZips(weather, zips, out):

    c = 0
    for i, zip in enumerate(zips.values):
        nearbyZips=  [int(z) for z in zip[1].split(",")]
        nearbyZipsData =  weather.loc[weather['Zip_Code'].isin(nearbyZips)]
        header = list(nearbyZipsData.mean().keys())
        nearbyZipsAvg = list(nearbyZipsData.mean().values)
        if c == 0:
            zipWriter.writerow(["Query"] + header)
        zipWriter.writerow([zip[0]] + nearbyZipsAvg)
        #print("zip %s = %d" %(z, nearbyZipsAvg.count(not int)))
        c = c+1
        if (c%25==0):
            print("%d zips parsed" %c)

	f = open(out,"wb")
	zipWriter = csv.writer(f)
	# zipWriter.writerow(["Query"] + header)
	# zipWriter.writerow([z] + nearbyZipsAvg)
	runZips()
	f.close()

if __name__ == "__main__":
	w, z, o = setOptions()

	weather = pd.read_csv(w,header=0)
	zips = pd.read_csv(z)

	runZips(weather, zips, o)

