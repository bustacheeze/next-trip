import requests, time

class Schedule:
    """"Metro transit schedule class"""

    API_BASE_URL = 'https://svc.metrotransit.org/nextripv2'

    def __init__(self, route_name, direction_name, stop_name):
        self.route = None
        self.validate_route(route_name)
        self.direction = None
        self.validate_direction(self.route['route_id'] ,direction_name)
        self.stop = None
        self.validate_stop(self.route['route_id'], self.direction['direction_id'], stop_name)
    

    # Validate the given route. Set self.route and return true if able to find a matching route for the given route name
    def validate_route(self, route_name):
        route_name_lower = route_name.lower()
        route_url = f"{self.API_BASE_URL}/routes"
        route_request = requests.get(route_url, headers={'accept': 'application/json'})
        route_request.raise_for_status()
        routes = route_request.json()

        for route in routes:
            if route_name_lower in route['route_label'].lower():
                self.route = route
                return True
        return False
    

    # Validate the given direction. Set self.direction and return true if able to find a matching direction for the given route
    def validate_direction(self, route_id, direction_name):
        direction_name_lower = direction_name.lower()
        direction_url = f"{self.API_BASE_URL}/directions/{route_id}"
        direction_request = requests.get(direction_url, headers={'accept': 'application/json'})
        direction_request.raise_for_status()
        directions = direction_request.json()

        for direction in directions:
            if direction_name_lower in direction['direction_name'].lower():
                self.direction = direction
                return True
        return False


    # Validate the given stop. Set self.stop and return true if able to find a matching stop on the given route in the given direction
    def validate_stop(self, route_id, direction_id, stop_name):
        stop_lower = stop_name.lower()
        stop_url = f"{self.API_BASE_URL}/stops/{route_id}/{direction_id}"
        stop_request = requests.get(stop_url, headers={'accept': 'application/json'})
        stop_request.raise_for_status()
        stops = stop_request.json()

        for stop in stops:
            if stop_lower in stop['description'].lower():
                self.stop = stop
                return True
        return False
    

    # Get the time of the next departure in epoch seconds, None if no more stops today
    def get_next_departure_time(self):
        next_departure_url = f"{self.API_BASE_URL}/{self.route['route_id']}/{self.direction['direction_id']}/{self.stop['place_code']}"
        next_departure_request = requests.get(next_departure_url, headers={'accept': 'application/json'})
        next_departure_request.raise_for_status()
        next_departure = next_departure_request.json()

        if len(next_departure['departures']) > 0:
            return next_departure['departures'][0]['departure_time']
        else:
            return None
    

    # Returns the time to the next depature as String
    def get_next_departure(self):
        departure_time = self.get_next_departure_time()
        if departure_time:
            current_time = time.time()
            return f"{int((departure_time - current_time) // 60)} minutes"
        else:
            return None