########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	takes a folder of NOAA weather station data
# 	and returns a csv that contains each station data
# 	by count id
# @usage:
#	python concatStations.py 
#		-f [header filename]
#		-d [csv files directory]
#		-o [output filename]
#######################################################


#imports
import glob
import pandas as pd
from optparse import OptionParser

'''
parse options from the command line
-f contains the header information for the DataFrame
-d contains the directory where the file is and will be saved
-o is the output filename
-q don't print 

@return opt, options that are parsed
@return args, extra unnparsed arguments
'''
def cmdLine():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
                  help="open header FILE", metavar="FILE")
	parser.add_option("-d", "--dir", dest="directory",
                  help="DIR of csv files", metavar="DIR")
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

@return filename, contains the header information
@return dir, directory of file and where to save output
@return out, output filename
'''
def setOptions():
	'''set options collected by cmd line'''

	opt, args =  cmdLine()
	#set default locs
	dir = "/Users/jasminehsu/school/green_farms/weather_county_annual_2015/"
	filename = pd.read_csv("/Users/jasminehsu/school/green_farms/weather_county_full.csv")
	out = "weather_county_final_2014.csv"

	# set of cmd line args
	dir = opt.directory if opt.directory else dir
	filename = opt.filename if opt.filename else filename
	out = opt.output if opt.output else out

	return filename, dir, out

'''
parses the txt file containing NOAA weather station
data for each COOP (station).  the file name format
is generated from running the R script that collects
the weather data

@see getNoaaStatsByCity.R
@param s, filename for the coop
@return the coop number
'''
def returnCoop(s):
	'''return the coop # from the file'''

    array = s.split("/")[-1].split("_")
    return array[2][0:-4]

'''
takes a folder of generated text files for each 
COOP number. this folder is generated from 
running the R script that collects the weather data
return final dataframe with merged stations by zipcode

@see getNoaaStatsByCity.R
@param out, the output filename
@outputfile, dataframe with merged stations by zipcode
'''
def concatStations(out):

	frame = []

	for f in files:
	    temp = pd.read_csv(f,header=0,mangle_dupe_cols=False)
	    temp = temp.groupby(level=0,axis=1).mean()
	    coop = returnCoop(f)
	    temp['Coop'] = coop
	    frame.append(temp)

	annual_sum=pd.concat(frame, axis=0).fillna("NaN")
	annual_sum.rename(columns={'$Unnamed':'Zip_Code'},inplace=True)
	df_final = reduce(lambda left,right: pd.merge(left,right,how='outer').fillna("NaN"), frame)
	df_final.to_csv(out,sep=",",index=False)

if __name__ == "__main__":
	filename, header, out = setOptions()

	files = glob.glob(filename+"*.csv")
	concatStations(files, out)

