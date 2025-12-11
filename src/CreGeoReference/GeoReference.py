import pandas as pd
import geopandas as gpd
#import geojsonio
from shapely.geometry import Point, Polygon

import pkg_resources
#from pathlib import Path
import os
import os.path

#https://geopandas.org/
###geojsonio                 0.0.3                    pypi_0    pypi
#geopandas                 0.6.0                    pypi_0    pypi
#shapely                   1.5.17                   pypi_0    pypi

## pip3 install geopandas==0.6
## https://geopandas.org/en/v0.6.0/projections.html

GEONAMES_PATH = pkg_resources.resource_filename('CreGeoReference', 'geonames/')
IPCC_PATH = pkg_resources.resource_filename('CreGeoReference', 'ipcc/')

class GeoReference():

    geonamesAll = None
    ipccRegions = None

    continentsGeonames = {'AF':'Africa', 'AS':'Asia', 'EU':'Europe', 'OC':'Oceania', 'SA':'South-America', 'NA':'North-America', 'AN':'Antarctica'}
    continentsIpcc = {'AFRICA':'Africa', 'ASIA':'Asia', 'EUROPE':'Europe', 'OCEANIA':'Oceania', 'SOUTH-AMERICA':'South-America', 'NORTH-AMERICA':'North-America',
                      'PACIFIC':'Pacific Ocean', 'ATLANTIC':'Atlantic Ocean', 'INDIAN':'Indian Ocean', 'SOUTHERN':'Antarctica', 'ARCTIC':'Arctica'}
                     ## needs , 'CENTRAL-AMERICA':'North-America,South-America', 'EUROPE-AFRIKA':'Europe,Africa'
                     ## done: 'POLAR':'Antarctica,Grönland'

    def __init__(self, local=False):
        # https://stackoverflow.com/questions/1270951/how-to-refer-to-relative-paths-of-resources-when-working-with-a-code-repository
        # https://stackoverflow.com/questions/918154/relative-paths-in-python 
        ## TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'test.txt')
        # package_dir = os.path.dirname(os.path.abspath(__file__))
        # thefile = os.path.join(package_dir,'test.cvs') 
        creVersion = '20.04'
        countryInfoFile  = 'https://github.com/creDocker/creAssets/blob/main/cre/versions/u'+creVersion+'/assets/public/geonames/countryInfo.csv?raw=true'
        countryShapeFile = 'https://github.com/creDocker/creAssets/blob/main/cre/versions/u'+creVersion+'/assets/public/geonames/shapes_countries.json?raw=true'
        ipccRegionsFile  = 'https://github.com/creDocker/creAssets/blob/main/cre/versions/u'+creVersion+'/assets/public/ipcc/IPCC-WGI-reference-regions-v4.geojson?raw=true' 
        languageCodesFile = 'https://github.com/creDocker/creAssets/blob/main/cre/versions/u20.04/assets/public/geonames/iso-languagecodes.csv?raw=true'
        if(local):
          print(['GEONAMES_PATH',GEONAMES_PATH])
          countryInfoFile  = GEONAMES_PATH + 'countryInfo.csv'
          countryShapeFile = GEONAMES_PATH + 'shapes_countries.json'
          ipccRegionsFile  = IPCC_PATH + 'IPCC-WGI-reference-regions-v4.geojson'
          #languageCodesFile

        geonamesData = pd.read_csv(countryInfoFile, keep_default_na=False)
        geonamesData = geonamesData.rename(columns={"geonameid": "geoNameId"})
        geonamesData['geoNameId']=geonamesData['geoNameId'].astype(str)
        ## print(geonamesData)
        geonamesShapes = gpd.read_file(countryShapeFile) 
        ## print(geonamesShapes.head())
        geonamesShapes.to_crs(epsg=4326, inplace=True)
        ## print(geonamesShapes.crs)
        self.geonamesAll = geonamesShapes.merge(geonamesData, on='geoNameId')
        ## print(self.geonamesAll)
        self.ipccRegions = gpd.read_file(ipccRegionsFile)
        ## print(self.ipccRegions)
        return None

    def getGeoDataByCoords(self, latitude, longitude):
        if(latitude and longitude): 
          coords_geo = gpd.GeoDataFrame({
             'geometry': gpd.points_from_xy([longitude], [latitude])
          }, crs={'init': 'epsg:4326', 'no_defs': True})
          ## coords_geo = gpd.GeoDataFrame({
          ##    'geometry': gpd.points_from_xy([longitude], [latitude])
          ## }, crs='epsg:4326')
          joined = gpd.sjoin(self.geonamesAll, coords_geo, how='inner')
          return joined
        else:
          return pd.DataFrame(None)

    def getCountriesNameByCoords(self, latitude, longitude, countries=[]):
        countryData = self.getGeoDataByCoords(latitude, longitude)
        if(not countryData.empty):
            return (countries+list(countryData['Country']))
        return countries

    def getCountriesNameByLanguage(self, language):
        countries={}
        for index, column in self.geonamesAll.iterrows():
            languages = column['Languages'].split(';')
            languageValue = 0.99
            for countryLanguage in languages:
                 if('-' in countryLanguage):
                     countryLanguage = countryLanguage.split('-')[0]
                 if(language == countryLanguage):
                     countries[column['Country']] = languageValue
                 languageValue *= 0.9
        return countries

    def getCountryNameByIso(self, iso):
        country = None
        rowName = 'ISO'
        if(3==len(iso)):
            rowName = 'ISO3'
        countryData = self.geonamesAll[self.geonamesAll[rowName]==iso]
        if(not countryData.empty):
           countries = list(countryData['Country'])
           country = countries[0]
        return country 

    def getCoordinatesByCountryName(self, country):
        longitude = None
        latitude = None
        countryData = self.geonamesAll[self.geonamesAll['Country']==country]
        if(not countryData.empty):
           geos = list(countryData['geometry'])
           longitude = geos[0].centroid.x
           latitude = geos[0].centroid.y
        return (latitude, longitude)   

    def getContinentsNameByCoords(self, latitude, longitude, continents=[]):
        gnContinents = self.getGeonamesContinentsNameByCoords(latitude, longitude, [])
        if(len(gnContinents)>0):
           continents = (continents+gnContinents)
        else:
          ipccContinents = self.getIpccContinentsNameByCoords(latitude, longitude, [])
          if(len(ipccContinents)>0):
            continents = (continents+ipccContinents)
        return continents

    def getGeonamesContinentsNameByCoords(self, latitude, longitude, continents=[]):
        continentData = self.getGeoDataByCoords(latitude, longitude)
        if(not continentData.empty):
          for gnCont in list(continentData['Continent']):
            if(gnCont in self.continentsGeonames):
              continents.append(self.continentsGeonames[gnCont])      
        return continents
 
    def getIpccContinentsNameByCoords(self, latitude, longitude, continents=[]):
        continentData = self.getIpccDataByCoords(latitude, longitude)
        if(not continentData.empty):
          for ipccCont in list(continentData['Continent']):
            if(ipccCont in self.continentsIpcc):
              continents.append(self.continentsIpcc[ipccCont])    
            else:
              if(('POLAR' == ipccCont) and (latitude>70)):
               continents.append('Arctica')   
              if(('POLAR' == ipccCont) and (latitude<-70)):
               continents.append('Antarctica')
              if(('CENTRAL-AMERICA' == ipccCont) and (latitude>11)):
               continents.append('North-America')   
              if(('CENTRAL-AMERICA' == ipccCont) and (latitude<11)):
               continents.append('South-America')             
        return continents

    def getIpccDataByCoords(self, latitude, longitude):
        if(latitude and longitude): 
          coords_geo = gpd.GeoDataFrame({
             'geometry': gpd.points_from_xy([longitude], [latitude])
          }, crs={'init': 'epsg:4326', 'no_defs': True})
          ## coords_geo = gpd.GeoDataFrame({
          ##    'geometry': gpd.points_from_xy([longitude], [latitude])
          ## }, crs='epsg:4326')
          joined = gpd.sjoin(self.ipccRegions, coords_geo, how='inner')
          return joined
        else:
          return pd.DataFrame(None)

    def getIpccAreaByCoords(self, latitude, longitude, ipcc=[]):
        ipccData = self.getIpccDataByCoords(latitude, longitude)
        if(not ipccData.empty):
            return (ipcc+list(ipccData['Acronym']))
        return ipcc
       
## testIt = GeoReference()
## print(testIt.getCountriesNameByCoords(48,7.85))
