import unittest
from schedule import Schedule
import json


class TestSchedule(unittest.TestCase):

    SAMPLE_ROUTES = json.loads('[{"route_id":"901","agency_id":0,"route_label":"METRO Blue Line"},{"route_id":"902","agency_id":0,"route_label":"METRO Green Line"},{"route_id":"906","agency_id":10,"route_label":"Airport Shuttle"},{"route_id":"903","agency_id":0,"route_label":"METRO Red Line"},{"route_id":"904","agency_id":0,"route_label":"METRO Orange Line"},{"route_id":"921","agency_id":0,"route_label":"METRO A Line"},{"route_id":"923","agency_id":0,"route_label":"METRO C Line"}]')
    SAMPLE_DIRECTIONS = json.loads('[{"direction_id":0,"direction_name":"Northbound"},{"direction_id":1,"direction_name":"Southbound"}]')
    SAMPLE_STOPS = json.loads('[{"place_code":"MAAM","description":"Mall of America Station"},{"place_code":"28AV","description":"28th Ave Station"},{"place_code":"BLCT","description":"Bloomington Central Station"},{"place_code":"AM34","description":"American Blvd Station"},{"place_code":"HHTE","description":"MSP Airport Terminal 2 - Humphrey Station"},{"place_code":"LIND","description":"MSP Airport Terminal 1 - Lindbergh Station"},{"place_code":"FTSN","description":"Fort Snelling Station"},{"place_code":"VAMC","description":"VA Medical Center Station"},{"place_code":"50HI","description":"50th St/ Minnehaha Park Station"},{"place_code":"46HI","description":"46th St Station"},{"place_code":"38HI","description":"38th St Station"},{"place_code":"LAHI","description":"Lake St/ Midtown Station"},{"place_code":"FRHI","description":"Franklin Ave Station"},{"place_code":"CDRV","description":"Cedar-Riverside Station"},{"place_code":"USBA","description":"U.S. Bank Stadium Station"},{"place_code":"GOVT","description":"Government Plaza Station"},{"place_code":"5SNI","description":"Nicollet Mall Station"},{"place_code":"WARE","description":"Warehouse District/ Hennepin Ave Station"},{"place_code":"TF1","description":"Target Field Station Platform 1"},{"place_code":"TF2","description":"Target Field Station Platform 2"}]')

    def setUp(self):
        self.schedule1 = Schedule("METRO Blue Line", "Mall of America", "North")
        self.schedule1.routes = self.SAMPLE_ROUTES
        self.schedule1.directions = self.SAMPLE_DIRECTIONS
        self.schedule1.stops = self.SAMPLE_STOPS

    def test_search_routes(self):
        test = self.schedule1.search_routes("Blue")
        result = json.loads('{"route_id":"901","agency_id":0,"route_label":"METRO Blue Line"}')
        self.assertEqual(test, result)

        test = self.schedule1.search_routes("A")
        result = json.loads('{"route_id":"906","agency_id":10,"route_label":"Airport Shuttle"}')
        self.assertEqual(test, result)

        test = self.schedule1.search_routes("A Line")
        result = json.loads('{"route_id":"921","agency_id":0,"route_label":"METRO A Line"}')
        self.assertEqual(test, result)

    def test_search_stops(self):
        test = self.schedule1.search_stops("Mall of America")
        result = json.loads('{"place_code":"MAAM","description":"Mall of America Station"}')
        self.assertEqual(test, result)

        test = self.schedule1.search_stops("MSP")
        result = json.loads('{"place_code":"HHTE","description":"MSP Airport Terminal 2 - Humphrey Station"}')
        self.assertEqual(test, result)
        
        test = self.schedule1.search_stops("MSP Airport Terminal 1")
        result = json.loads('{"place_code":"LIND","description":"MSP Airport Terminal 1 - Lindbergh Station"}')
        self.assertEqual(test, result)

    def test_search_directions(self):
        test = self.schedule1.search_directions("north")
        result = json.loads('{"direction_id":0,"direction_name":"Northbound"}')
        self.assertEqual(test, result)

        test = self.schedule1.search_directions("nOrTh")
        result = json.loads('{"direction_id":0,"direction_name":"Northbound"}')
        self.assertEqual(test, result)

        test = self.schedule1.search_directions("bound")
        result = json.loads('{"direction_id":0,"direction_name":"Northbound"}')
        self.assertEqual(test, result)
