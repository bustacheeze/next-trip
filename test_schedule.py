import unittest
from schedule import Schedule
import json

class TestSchedule(unittest.TestCase):

    SAMPLE_ROUTES = json.loads('[{"route_id":"901","agency_id":0,"route_label":"METRO Blue Line"},{"route_id":"902","agency_id":0,"route_label":"METRO Green Line"},{"route_id":"906","agency_id":10,"route_label":"Airport Shuttle"},{"route_id":"903","agency_id":0,"route_label":"METRO Red Line"},{"route_id":"904","agency_id":0,"route_label":"METRO Orange Line"}]')
    SAMPLE_DIRECTIONS = json.loads('[{"direction_id":0,"direction_name":"Northbound"},{"direction_id":1,"direction_name":"Southbound"}]')
    SAMPLE_STOPS = json.loads('[{"place_code":"APNB","description":"Apple Valley Transit Station"},{"place_code":"CE47","description":"147th St Station"},{"place_code":"CE14","description":"140th St Station"},{"place_code":"CGTR","description":"Cedar Grove Transit Station"},{"place_code":"MAAM","description":"Mall of America Station"}]')

    def setUp(self):
        self.schedule1 = Schedule("METRO Red Line", "Mall of America", "North")
        self.schedule1.routes = self.SAMPLE_ROUTES

    def test_search_routes(self):
        test = self.schedule1.search_routes("Red")
        result = json.loads('{"route_id":"903","agency_id":0,"route_label":"METRO Red Line"}')
        self.assertEqual(test, result)
