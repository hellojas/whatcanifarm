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

'''
fetch the json from the url using urllib
to open the connection and retrieve 
the data

@params method, the urllib method
@params params, parameters for urllib encoder
@return js, json object
'''
def fetchJson(method, params):

    uri = DOMAIN + '%s?%s&username=%s' % (method, urllib.urlencode(params), USERNAME)
    resource = urllib2.urlopen(uri).readlines()
    js = json.loads(resource[0])
    return js

'''
fetchJson for a specific geonameId
see geoname API for detailed exp

@params geonameID, see geoname API
@params kwargs, param for urllib
@return js, json object
'''
def get(geonameId, **kwargs):

    method = 'getJSON'
    valid_kwargs = ('lang',)
    params = {'geonameId': geonameId}
    for key in kwargs:
        if key in valid_kwargs:
            params[key] = kwargs[key]
    return fetchJson(method, params)

'''
fetchJson for a specific geonameId
but return the children
see geoname API for detailed exp

@params geonameID, see geoname API
@params kwargs, param for urllib
@return js, json object
'''
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

'''
search based on valid parameters
for the geoname API

@params kwargs, param for urllib
@return js, json object
'''
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

'''
fetch the json data for this 
postal code query

@params kwargs, param for urllib
@return js, json object
'''
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

'''
fetch the json data for nearby 
postal codes based on this 
postal code query

@params kwargs, param for urllib
@return js, json object
'''
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


'''
find nearby postal codes for a given zipcode

@params zc, zipcode to query
@params r, the current list for that zipcode
@outputfile nearby zipcodes for each zipcode
'''
def runZip(zc, r): 

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

'''
find nearby postal codes for all zipcodes
at a set radius limit

@params radius, limit of nearby zipcodes
@outputfile nearby zipcodes for each zipcode
@outputfile nearby zipcodes for each zipcode, 
simplified file
'''
def getNearbyZips(radius):

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
	getNearbyZips(30) 

