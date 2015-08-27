########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	preproceses the file needed for target input into
#	the multilable binarizer 
# @usage:
#	python multilabelFormat.py -f [farms filename]
########################################################
from optparse import OptionParser
import pandas as pd
import numpy as np
import csv, sys

def cmdLine():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename",
                  help="open FILE", metavar="FILE")
	parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

	(opt, args) = parser.parse_args()

	return opt, args

def getFarms(filename):
	'''retrieve farms file and drop duplicates'''

	print "getting farms file..."
	farms = pd.read_csv(filename)
	header = list(farms.columns)
	farms.pop("Zip_Code")
	farms = farms.drop_duplicates()
	return farms

def generateCropsAndFeatures(farms):
	'''collect unique crops by zipcode'''

	print "generating crops and features..."

	# crop and feature file
	newfile = open("crops_list_2014.txt",'wb')
	csvwriter = csv.writer(newfile)

	newfile2 = open("features_list_2014.csv",'wb')
	csvwriter2 = csv.writer(newfile2)
	csvwriter2.writerow(farms.columns[2:])

	# get all unique crops for a single zip code
	for count,zip in enumerate(farms['Coop'].unique()):
	    allCropsWithZip = farms[farms['Coop'] == zip]
	    crops =list(allCropsWithZip["Crop"].unique())
	    if np.NaN in crops:
	        crops.remove(np.NaN)
	    if len(crops)==0:
	        crops.append("crop")
	    values = list(allCropsWithZip.ix[:,1:].iloc[[0]].values[0])
	    crop_str = str(crops).replace('[','').replace(']','').replace('\n','').replace('-','').replace('oz','').replace("%","").translate(None, digits)
	    csvwriter.writerow([crop_str])
	    csvwriter2.writerow(values[1:])
	    if (count % 250 == 0):
	        print ("processed %d zips" %count)
	print count

	newfile.close()
	newfile2.close()

if __name__ == "__main__":
	opt, args =  cmdLine()
	farms = getFarms(opt.filename) #"full_farms_dataset_impAvg_2014.csv"
	generateCropsAndFeatures(farms)


