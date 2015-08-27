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

def setOptions():
	'''set options collected by cmd line'''

	opt, args =  cmdLine()
	#set default locs
	filename = "/Users/jasminehsu/school/green_farms/weather_county_annual_2015/"
	header = pd.read_csv("/Users/jasminehsu/school/green_farms/weather_county_full.csv")
	out = "weather_county_final_2014.csv"

	# set of cmd line args
	filename = opt.directory if opt.directory else filename
	header = opt.filename if opt.filename else header
	out = opt.output if opt.output else out

	return filename, header, out

def returnCoop(s):
	'''return the coop # from the file'''

    array = s.split("/")[-1].split("_")
    return array[2][0:-4]

def concatStations(out):
	'''return final dataframe with merged stations by zipcode'''

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

