from CreGeoReference.geoTools import geoTools

import os
import os.path

import requests
import json

import geocoder
#import mysecretes

class GeoReference():

    #geonamesAll = None
    #ipccRegions = None
    gT = None
    allParameters = ['phrase','language','latitude','longitude','gnd','geonames','geotype','country','ipcc','continent']

    def __init__(self, phrase=None, language=None, latitude=None, longitude=None, geonames=None, local=False):
        # https://stackoverflow.com/questions/1270951/how-to-refer-to-relative-paths-of-resources-when-working-with-a-code-repository
        # https://stackoverflow.com/questions/918154/relative-paths-in-python 
        ## TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'test.txt')
        # package_dir = os.path.dirname(os.path.abspath(__file__))
        # thefile = os.path.join(package_dir,'test.cvs') 
        creVersion = '20.04'
        
        GeoReference.gT = geoTools(local)    
 
        self.parameters = {'phrase':phrase,'language':language,
                           'latitude':latitude,'longitude':longitude,
                           'geonames':geonames}
        self.initializeParameters()

    def initializeParameters(self):
        for param in GeoReference.allParameters:
          if(not param in self.parameters):
            self.parameters[param] = None

    def checkParameters(self, parameters=['phrase','language','latitude','longitude','gnd','geonames','geotype','country','ipcc','continent']):
        allFound = True
        for param in parameters:
          if(not self.parameters[param]):
            allFound = False
        return allFound

    def expandParameters(self, parameters=['phrase','language','latitude','longitude','gnd','geonames','geotype','country','ipcc','continent']):
        noChange = True

        if(self.parameters['geonames']): #no costs
          result = searchGndByGeonamesId(self.parameters['geonames'])
          if(('gndId' in result) and (not self.parameters['gnd'])):
            self.parameters['gnd'] = result['gndId']
            noChange = False
          if(('latitude' in result) and (not self.parameters['latitude'])):
            self.parameters['latitude'] = result['latitude']
            noChange = False
          if(('longitude' in result) and (not self.parameters['longitude'])):
            self.parameters['longitude'] = result['longitude']
            noChange = False  
          if(('preferredName' in result) and (not self.parameters['phrase'])):
            self.parameters['phrase'] = result['preferredName']
            noChange = False  
          # 'variantName' 

        if(self.parameters['phrase'] and self.parameters['latitude'] and self.parameters['longitude']): #no costs
          result = searchGndByNameAndGeo(self.parameters['phrase'], self.parameters['latitude'], self.parameters['longitude'])
          if(result):
            if(('gndId' in result) and (not self.parameters['gnd'])):
              self.parameters['gnd'] = result['gndId']
              noChange = False
            # 'preferredName'

        if(self.parameters['phrase']): #no costs
          result = searchGndWithCoordsAndGeonamesByName(self.parameters['phrase'])
          print(result)
          if(result): 
            if(('gndId' in result) and (not self.parameters['gnd'])):
              self.parameters['gnd'] = result['gndId']
              noChange = False
            if(('geonames' in result) and (not self.parameters['geonames'])):
              self.parameters['geonames'] = result['geonames']
              noChange = False
            if(('latitude' in result) and (not self.parameters['latitude'])):
              self.parameters['latitude'] = result['latitude']
              noChange = False
            if(('longitude' in result) and (not self.parameters['longitude'])):
              self.parameters['longitude'] = result['longitude']
              noChange = False  
            # 'variantName' & 'preferredName'



        if(('gnd' in parameters) and (not self.parameters['gnd'])):
          todo = 1 # searchGeonamesByNameAndLanguage #limited

        if(self.parameters['latitude'] and self.parameters['longitude'] and GeoReference.gT): 
          if(('country' in parameters) and (not self.parameters['country'])):
            countries = GeoReference.gT.getCountriesNameByCoords(48,7.85)
            print(countries)
            if(len(countries) > 0):
              self.parameters['country'] = countries[0]
              noChange = False              

        
        return noChange      


    def inq(self, parameters=['phrase','language','latitude','longitude','gnd','geonames','geotype','country','ipcc','continent']):
        result = {}
        checkParameters = parameters
        noChange = False
        while((not self.checkParameters(parameters)) and (not noChange)):
          noChange = self.expandParameters(checkParameters)
          checkParameters = GeoReference.allParameters
        for param in GeoReference.allParameters:
          if(param in parameters):
            result[param] = self.parameters[param]
        #result['gnd'] = '555'
        return result

#geonames & secrets or env
geonamesKey = os.getenv('GEONAMES_KEY')

#geonames
def searchGeonamesByNameAndLanguage(phrase, lang):
    result = {}
    gn = geocoder.geonames(phrase, lang=lang, key=geonamesKey)
    print([phrase,gn,gn.geonames_id]) 
    if(gn.geonames_id):  
      result['geonames'] = int(gn.geonames_id)
      result['latitude'] = float(gn.lat)
      result['longitude'] = float(gn.lng)
      result['geotype'] = gn.feature_class
      ##df.loc[index,'country'] = gn.country  #localized!
      gne = geocoder.geonames(phrase, lang=lang, key=geonamesKey)
      if(gne.country):
        result['country'] = gne.country
        print(gne.country)
        print(['geo',gn.lat,gn.lng, gn.geonames_id, gn])
    return result

#gnd
def searchGndWithCoordsAndGeonamesByName(locationName, strict=True):
    gndUrl = 'https://explore.gnd.network/search?term='+locationName+'&f.satzart=Geografikum&rows=1'
    gndurl = 'https://lobid.org/gnd/search?q='+locationName+'&filter=type%3APlaceOrGeographicName&format=json'   #hasGeometry
    gndurl = 'https://lobid.org/gnd/search?q='+locationName+'&filter=type%3APlaceOrGeographicName&size=100&format=json'   #size!
    if(strict):
      gndurl = 'https://lobid.org/gnd/search?q='+locationName+'&filter=type%3APlaceOrGeographicName&size=1000&format=json'
    page = requests.get(gndurl, timeout=60)
    if page.status_code == 200:
      content = page.content
      #print(content)
      if(content):
        #print(content)
        jsonData = json.loads(content)
        #print(jsonData)      #'variantName' !
        if('member' in jsonData):
          for member in jsonData['member']:
           #print(25*"=*")
           #print(member)  
           if('gndIdentifier' in member):
             #print(member['gndIdentifier']) 
             result = {'gndId':member['gndIdentifier']} 

             geonameFound = False 
             if('sameAs' in member):
               for same in member['sameAs']:
                 #print(25*"##")
                 #print(same)
                 if('id' in same):
                   if('https://sws.geonames.org/' in same['id']):
                     geonameFound = True
                     geonamesId = same['id'].replace('https://sws.geonames.org/','')
                     result['geonames'] = int(geonamesId) 
             geoFound = False
             if('hasGeometry' in member):
               #print(member['hasGeometry']) 
               latitude = None
               longitude = None
               for geo in member['hasGeometry']:  
                 if('asWKT' in geo and 'type' in geo and geo['type']=='Point'):
                    point = geo['asWKT'][0]
                    point = point.replace('Point ','').strip().strip('()').strip()
                    #print(point)
                    coords = point.split(" ")
                    #print(coords)
                    result['longitude'] = float(coords[0])
                    result['latitude'] = float(coords[1])
                    geoFound = True
             found = False
             if('variantName' in member):
               #print(member['variantName']) 
               result['variantNames'] = member['variantName']  
               found = locationName in member['variantName'] 
             if('preferredName' in member):
               #print(member['preferredName'])
               result['preferredName'] = member['preferredName']
               found = found or (member['preferredName'] == locationName)
             if(strict and found and geoFound and geonameFound): 
               return result
             if(not strict and found): 
               return result
             if(not strict):
               return searchGndWithCoordsAndGeonamesByName(locationName, False)
    return None

#gnd
def searchGndByGeonamesId(geonamesId):
    gndurl = 'https://lobid.org/gnd/search?q='+str(geonamesId)+'&filter=type%3APlaceOrGeographicName&size=100&format=json'   
    gndurl = 'https://lobid.org/gnd/search?q='+str(geonamesId)+'+AND+_exists_:sameAs&filter=type%3APlaceOrGeographicName&size=100&format=json' #sameAs

    page = requests.get(gndurl, timeout=60)
    if page.status_code == 200:
      content = page.content
      #print(content)
      if(content):
        #print(content)
        jsonData = json.loads(content)
        #print(jsonData)      #'variantName' !
        if('member' in jsonData):
          for member in jsonData['member']:
           if('sameAs' in member):
             for same in member['sameAs']:
               #print(25*"##")
               #print(same)
               if('id' in same):
                 if(same['id']=="https://sws.geonames.org/"+str(geonamesId)):
                   if('gndIdentifier' in member):
                     result = {'gndId':member['gndIdentifier']} 
                     #print(member['gndIdentifier']) 
                     #print(25*"=*")
                     #print(member)  
                     if('hasGeometry' in member):
                       #print(member['hasGeometry']) 
                       latitude = None
                       longitude = None
                       for geo in member['hasGeometry']:  
                         if('asWKT' in geo and 'type' in geo and geo['type']=='Point'):
                            point = geo['asWKT'][0]
                            point = point.replace('Point ','').strip().strip('()').strip()
                            #print(point)
                            coords = point.split(" ")
                            #print(coords)
                            result['longitude'] = float(coords[0])
                            result['latitude'] = float(coords[1])
                     if('variantName' in member):
                       #print(member['variantName']) 
                       result['variantNames'] = member['variantName']  
                     if('preferredName' in member):
                       #print(member['preferredName'])
                       result['preferredName'] = member['preferredName']
                     return result
    return None

def searchGndByGeonamesIdAndGeo(geonamesId, latitude, longitude, maxDistance=10):
    return None

def searchGndByNameAndGeo(locationName, latitude, longitude, maxDistance=10):
    gndUrl = 'https://explore.gnd.network/search?term='+locationName+'&f.satzart=Geografikum&rows=1'
    gndurl = 'https://lobid.org/gnd/search?q='+locationName+'&filter=type%3APlaceOrGeographicName&size=100&format=json'   
    gndurl = 'https://lobid.org/gnd/search?q='+locationName+'+AND+_exists_:hasGeometry&filter=type%3APlaceOrGeographicName&size=100&format=json' #hasGeometry 

    page = requests.get(gndurl, timeout=60)
    if page.status_code == 200:
      content = page.content
      #print(content)
      if(content):
        #print(content)
        jsonData = json.loads(content)
        #print(jsonData)      #'variantName' !
        if('member' in jsonData):
          minDistance2 = 10E9
          result = None
          for member in jsonData['member']:
           #print(25*"=*")
           #print(member)  
           if('hasGeometry' in member):
            #print(member['hasGeometry']) 
            for geo in member['hasGeometry']: 
             if('asWKT' in geo and 'type' in geo and geo['type']=='Point'):
               point = geo['asWKT'][0]
               point = point.replace('Point ','').strip().strip('()').strip()
               #print(point)
               coords = point.split(" ")
               #print(coords)
               currLongitude = float(coords[0])
               currLatitude = float(coords[1])
               distance2 = (currLongitude-longitude)**2+(currLatitude-latitude)**2
               #print(distance2)
               if(distance2<minDistance2):
                 minDistance = distance2 
                 if('gndIdentifier' in member):
                   #print(member['gndIdentifier']) 
                   result = {'longitude':currLongitude, 'latitude':currLatitude, 'distance':distance2**0.5}
                   result['gndId'] = member['gndIdentifier']
                   if('preferredName' in member):
                     #print(member['preferredName']) 
                     result['preferredName'] = member['preferredName']
          #print(result)
          if(minDistance2<maxDistance**2):
            return result
        return None           


 
        
