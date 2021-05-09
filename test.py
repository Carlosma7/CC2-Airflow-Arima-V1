import unittest
import json
import sys, os.path
from servidor import *

class Test_V1(unittest.TestCase): 

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_24h_v1(self):
        response = self.app.get('/servicio/v1/prediccion/24horas')
        self.assertEqual(response.status_code, 200)

    def test_48h_v1(self):
        response = self.app.get('/servicio/v1/prediccion/48horas')
        self.assertEqual(response.status_code, 200)

    def test_72h_v1(self):
        response = self.app.get('/servicio/v1/prediccion/72horas')
        self.assertEqual(response.status_code, 200)