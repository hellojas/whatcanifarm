########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	takes the organic farms list with zipcodes and 
#	returns a mapping for a crop to each zipcode
# @usage:
#	python cleanCrops.py 
#		-f [farms filename]
#		-d [file directory]
#		-o [output filename]
#######################################################

#imports
import sys, os
import re as re
import pandas as pd


def cmdLine():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
                  help="open header FILE", metavar="FILE")
	parser.add_option("-d", "--dir", dest="directory",
                  help="DIR of file", metavar="DIR")
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
	dir = "/Users/jasminehsu/school/green_farms/"
	filename = "organic_farms_list_with_county.csv"
	out = "crop_to_zip_map.csv"

	# set of cmd line args
	filename = opt.filename if opt.filename else filename
	dir = opt.dir if opt.dir else dir
	out = opt.output if opt.output else out

	return filename, header, out


def clean(s, rep):
	'''clean crop strings'''

	# removeWords = dict({"handling ":"","products ":"","marketing/trading of \"organic\" ":"","brokering of organic products - ":" "})
	# removeWords = dict({"handling ":"","products ":"","trading ":"","brokering ":""})
    regex = re.compile("(%s)" % "|".join(map(re.escape,removeWords.keys())))
    s = s.strip().lower()
    rep = dict((re.escape(k),v) for k,v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    s = pattern.sub(lambda m: rep[re.escape(m.group(0))],s)
    
    return s.lower().strip()

def generateCropToZipMap(myfile,myfilesize,output):
	'''generate a crop to zip code mapping'''

	crops = dict()
	for row in range(0,myfileSize)[0:50]:
    products = str(myfile['Products_Produced'].iloc[row])
    split = re.split(':|,|;|/',products)
    for item in split:
        item = clean(item,removeWords)
        if item:
            if item in crops.keys():
                crops[item].append(myfile['Zip_Code'].iloc[row])
            else:
                crops[item] = [myfile['Zip_Code'].iloc[row]]

	df = pd.DataFrame()
	i = 0;
	for crop, zips in crops.iteritems():
	    df = df.append([[crop,z] for z in set(zips)])
	df.columns = ["Crop","Zip_Code"]
	df.to_csv(output,index=False)

if __name__ == "__main__":
	filename, header, out = setOptions()

	myfile = pd.read_csv(dir+filename)
	myfileSize = len(myfile)

	generateCropToZipMap(myfile,myfilesize,out)

	

