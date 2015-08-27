########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	takes a dataframe with fips code and returns it
#   mapped to zipcodes
# @usage:
#	python fipsToZipsMapper.py
#######################################################

#imports
import sys
import urllib
import urllib2
import simplejson as json
import csv
import pandas as pd
from set import Sets

def mapper():
    '''map zip codes to fips code'''

    weatherfile = "full_farms_dataset.csv"
    weather = pd.read_csv(weatherfile,header=0)
    fipsZipsFile = "zip_county.csv"
    fzMap = pd.read_csv(fipsZipsFile,header=0)

    weatherWithFips = pd.merge(weather,fzMap, on="Fips_Code", how="left")
    weatherWithFips.to_csv("full_farms_dataset_withZip.csv", index=None)

    print weatherWithFips.shape, weather,shape

if __name__ == "__main__":
	mapper()

