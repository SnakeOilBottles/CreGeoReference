from unittest import TestCase

from CreGeoReference.GeoReference import GeoReference 
import CreGeoReference
from importlib.metadata import version

#import mysecrets
#import os

class TestGnd(TestCase):

    def test_version(self):
        print(['CreGeoReference: ', version("CreGeoReference")])
        self.assertEqual('Version', 'Version')

    '''
    def test_secrets(self):
        key = os.getenv('GEONAMES_KEY')
        self.assertEqual(key, '123')
    ''' 

    def test_init_class(self):
        gf = GeoReference()
        gnd = gf.parameters['gnd']
        print(gnd)
        self.assertEqual(gnd, None)

    def test_stuttgart_de(self):
        gf = GeoReference(phrase='Stuttgart', language='de')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4058282-6')

    def test_bonn_only(self):
        gf = GeoReference(phrase='Bonn')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4007666-0')

    def test_hamburg_coords(self):
        gf = GeoReference(phrase='Hamburg', longitude=10.0, latitude=53.6)
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4023118-5')

    def test_francese_fr(self):
        gf = GeoReference(phrase='Repubblica Francese', language='fr')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4018145-5')

    def test_italy_en(self):
        gf = GeoReference(phrase='Italy', language='en')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4027833-5')

    def test_munich_en(self):
        gf = GeoReference(phrase='Munich', language='en')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4127793-4')

    def test_freiburg_de(self):
        gf = GeoReference(phrase='Freiburg', language='de')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4018272-1')

    def test_dresden_geonames(self):
        gf = GeoReference(geonames='2935022')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4012995-0')



    ''' #too many results?
    def test_frankfurt_de(self):
        gf = GeoReference(phrase='Frankfurt', language='de')
        results = gf.inq(['gnd'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['gnd'], '4058282-6')
    '''





