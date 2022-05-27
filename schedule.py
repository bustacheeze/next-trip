import requests, time


class Schedule:
    """"Metro transit schedule class"""
    API_BASE_URL = 'https://svc.metrotransit.org/nextripv2'

    def __init__(self, route_name, direction_name, stop_name):
        self.route_name = route_name
        self.direction_name = direction_name
        self.stop_name = stop_name
        self.route = None
        self.routes = None
        self.direction = None
        self.directions = None
        self.stop = None
        self.stops = None

    def init_data(self):
        self.routes = self.get_routes()
        self.route = self.search_routes(self.route_name)
        if not self.route:
            print(f"ERROR: Unable to find route with name \'{self.route_name}\'")
            exit()
        
        self.directions = self.get_directions(self.route['route_id'])
        self.direction = self.search_directions(self.direction_name)
        if not self.direction:
            print(f"ERROR: Unable to find direction \'{self.direction_name}\' on route {self.route['route_label']}")
            exit()
        
        
        self.stops = self.get_stops(self.route['route_id'], self.direction['direction_id'])
        self.stop = self.search_stops(self.stop_name)
        if not self.stop:
            print(f"ERROR: Unable to find stop \'{self.stop_name}\' on route {self.route['route_label']} going {self.direction['direction_name']}")
            exit()
    
    # Common get method, return request.get data from a given URL
    def get_common(self,url):
        r = requests.get(url, headers={'accept': 'application/json'})
        r.raise_for_status()
        return r

    # Return list of routes
    def get_routes(self):
        return self.get_common(f"{self.API_BASE_URL}/routes").json()
    
    # Return list of directions for a given route
    def get_directions(self, route_id):
        return self.get_common(f"{self.API_BASE_URL}/directions/{route_id}").json()
    
    # Return list of stops for on the given route in the given direction
    def get_stops(self, route_id, direction_id):
        return self.get_common(f"{self.API_BASE_URL}/stops/{route_id}/{direction_id}").json()
    
    # Return list of departure times from the given stop on the given route in the given direction
    def get_departure_times(self,route_id, direction_id, place_code):
        return self.get_common(f"{self.API_BASE_URL}/{route_id}/{direction_id}/{place_code}").json()

    # Search through the routes and return the first route matching the given route_name or None
    def search_routes(self, route_name):
        route_name_lower = route_name.lower()
        for route in self.routes:
            if route_name_lower in route['route_label'].lower():
                return route
        return None

    # Search through the directions and return the first direction matching the given direction_name or None
    def search_directions(self, direction_name):
        direction_name_lower = direction_name.lower()
        for direction in self.directions:
            if direction_name_lower in direction['direction_name'].lower():
                return direction
        return None

    # Search through the stops and return the first stop matching the given stop_name or None
    def search_stops(self, stop_name):
        stop_lower = stop_name.lower()
        for stop in self.stops:
            if stop_lower in stop['description'].lower():
                return stop
        return None

    # Get the time of the next departure in epoch seconds, None if no more stops today
    def get_next_departure_time(self):
        departures = self.get_departure_times(self.route['route_id'], self.direction['direction_id'], self.stop['place_code'])

        if len(departures['departures']) > 0:
            return departures['departures'][0]['departure_time']
        else:
            return None

    # Return the time to the next depature as String formatted "<INT> minutes" or None
    def get_next_departure(self):
        departure_time = self.get_next_departure_time()
        if departure_time:
            current_time = time.time()
            return f"{int((departure_time-current_time)//60)} minutes"
        else:
            return None
