########################################################
# @author: jasmine hsu
# @contact: jch550@nyu.edu
# @description:
# 	gets the nearby zipcodes given an set raidus
#	this is used to impute values for nearby zipcodes
#	this uses geonames API and requies a username
# @usage:
#	python nearbyZipCodes.py
#######################################################

#imports
import sys
import urllib
import urllib2
import simplejson as json
import csv
import pandas as pd
from set import Sets

DOMAIN = 'http://api.geonames.org/'
USERNAME = 'hellojas' #enter your geonames username here

def fetchJson(method, params):
	'''fetch json from domain using urllib'''

    uri = DOMAIN + '%s?%s&username=%s' % (method, urllib.urlencode(params), USERNAME)
    resource = urllib2.urlopen(uri).readlines()
    js = json.loads(resource[0])
    return js

def get(geonameId, **kwargs):
	'''fetch json by geonam params'''

    method = 'getJSON'
    valid_kwargs = ('lang',)
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    return fetchJson(method, params)

def children(geonameId, **kwargs):
    method = 'childrenJSON'
    valid_kwargs = ('maxRows', 'lang',)
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None

def search(**kwargs):
    method = 'searchJSON'
    valid_kwargs = ('q', 'name', 'name_equals', 'name_startsWith', 'maxRows', 'startRow', 'country', 'countryBias', 'continentCode', 'adminCode1', 'adminCode2', 'adminCode3', 'featureClass', 'featureCode', 'lang', 'type', 'style', 'isNameRequired', 'tag', 'operator', 'charset',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None

def postalCodeSearch(**kwargs):
	'''fetch json by zipcode'''

    method = 'postalCodeSearchJSON'
    valid_kwargs = ('postalcode', 'postalcode_startsWith', 'placename', 'placename_startsWith', 'maxRows', 'country', 'countryBias', 'style', 'operator', 'isReduced', 'charset',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('postalCodes' in results):
        return results['postalCodes']
    else:
        return None

def findNearbyPostalCodes(**kwargs):
	'''fetch nearby zipcodes'''

    method = 'findNearbyPostalCodesJSON'
    valid_kwargs = ('postalcode', 'placename', 'maxRows', 'country', 'localCountry', 'lat', 'lng', 'radius', 'style',)
    params = {}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('postalCodes' in results):
        return results['postalCodes']
    else:
        return None

def hierarchy(geonameId, **kwargs):
    method = 'hierarchyJSON'
    valid_kwargs = ('lang')
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    results = fetchJson(method, params)

    if('geonames' in results):
        return results['geonames']
    else:
        return None

def runZip(zc, r): 
	'''write out nearby zipcodes'''

    result = findNearbyPostalCodes(postalcode=zc,radius=r,country="US",maxRows=100)

    if result == None:
        missing.append(zc)
        print("missing query = %s" %zc)

    else:
        for r in result:
            zipWriter.writerow([zc] + r.values())
            
        nearby = []
        for r in result:
            nearby.append(r["postalCode"])
        zipWriter2.writerow([zc] + [",".join(nearby[1:])])

def getNearbyZips(radius):
	'''get nearby zipcodes with set radius (30 max)'''

	missing = []

	f = open("nearbyZips_%dmiles.csv" %radisu,"wb")
	zipWriter = csv.writer(f)
	zipWriter.writerow(["query"] + r.keys())

	f2 = open("nearbyZips_simp_%dmiles.csv" %radius,"wb")
	zipWriter2 = csv.writer(f2)
	zipWriter2.writerow(["query","nearby"])

	zcount = 0
	for z in zips:
	    runZip(format(z, '05d'))
	    zcount = zcount+1
	    if zcount % 10==0:
	        print("...%d zipcodes parsed" %zcount)
	
	f.close()
	f2.close()

if __name__ == "__main__":
	getNearbyZips(30) # 30 is max for geonames

