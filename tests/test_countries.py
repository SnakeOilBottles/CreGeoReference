from unittest import TestCase

from CreGeoReference.geoTools import geoTools
import CreGeoReference
from importlib.metadata import version

class TestCountries(TestCase):

    def test_version(self):
        print(['CreGeoReference: ', version("CreGeoReference")])
        self.assertEqual('Version', 'Version')

    def test_country_remote(self):
        gf = geoTools(local=False)
        countries = gf.getCountriesNameByCoords(48,7.85)
        print(countries)
        self.assertEqual(len(countries), 1)
        self.assertEqual(countries[0], 'Germany')

    def test_country_local(self):
        gf = geoTools(local=True)
        countries = gf.getCountriesNameByCoords(48,7.85)
        print(countries)
        self.assertEqual(len(countries), 1)
        self.assertEqual(countries[0], 'Germany')


    def test_language(self):
        gf = geoTools()
        countries = gf.getCountriesNameByLanguage('de')
        print(countries)
        self.assertTrue(len(countries)>0)
        self.assertEqual(len(countries), 11)
        self.assertEqual(countries['Germany'], 0.99)



