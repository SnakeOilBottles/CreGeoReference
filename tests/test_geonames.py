from unittest import TestCase

from CreGeoReference.GeoReference import GeoReference 
import CreGeoReference
from importlib.metadata import version

#import mysecrets
#import os

class TestGeonames(TestCase):

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
        gnd = gf.parameters['geonames']
        print(gnd)
        self.assertEqual(gnd, None)

    def test_stuttgart_de(self):
        gf = GeoReference(phrase='Stuttgart', language='de')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2825297)

    def test_bonn_only(self):
        gf = GeoReference(phrase='Bonn')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2946447)

    def test_hamburg_coords(self):
        gf = GeoReference(phrase='Hamburg', longitude=10.0, latitude=53.6)
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2911297)

    def test_francese_fr(self):
        gf = GeoReference(phrase='Repubblica Francese', language='fr')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 3017382)

    def test_italy_en(self):
        gf = GeoReference(phrase='Italy', language='en')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 3175395)

    def test_munich_en(self):
        gf = GeoReference(phrase='Munich', language='en')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2867714)

    def test_freiburg_de(self):
        gf = GeoReference(phrase='Freiburg', language='de')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2925177)

    def test_frankfurt_main_de(self):
        gf = GeoReference(phrase='Frankfurt am Main', language='de')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2925533)

    def test_frankfurt_oder_de(self):
        gf = GeoReference(phrase='Frankfurt (Oder)', language='de')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2925535)

    def test_dresden_geonames(self):
        gf = GeoReference(gnd='4012995-0')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2935022)

    def test_denzlingen_de(self):
        gf = GeoReference(phrase='Denzlingen', language='de')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2938190)


    '''
    #too many results?   
    def test_frankfurt_de(self):
        gf = GeoReference(phrase='Frankfurt', language='de')
        results = gf.inq(['geonames'])
        print(gf.parameters)
        print(results)
        self.assertEqual(results['geonames'], 2925535)
    '''




