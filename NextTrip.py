import requests


BUS_ROUTE = "METRO Blue Line"
BUST_STOP_NAME = "Target Field Station Platform 1"
DIRECTION = "south"


API_BASE_URL = 'https://svc.metrotransit.org/nextripv2'


# Get route
def GetRoute(route):
    RouteLower = route.lower()
    GetRouteURL = f"{API_BASE_URL}/routes"
    GetRouteRequest = requests.get(GetRouteURL, headers={'accept': 'application/json'})
    GetRouteRequest.raise_for_status()
    Routes = GetRouteRequest.json()

    # Return 
    for Route in Routes:
        if RouteLower in Route['route_label'].lower():
            return Route
    
    print(f"ERROR: Route \'{route}\' not found")
    return None

# Get direction
def GetDirection(route_id, direction):
    DirectionLower = direction.lower()
    GetDirectionURL = f"{API_BASE_URL}/directions/{route_id}"
    GetDirectionRequest = requests.get(GetDirectionURL, headers={'accept': 'application/json'})
    GetDirectionRequest.raise_for_status()
    Directions = GetDirectionRequest.json()

    for Direction in Directions:
        if DirectionLower in Direction['direction_name'].lower():
            return Direction

    print(f"ERROR: Direction \'{direction}\' not found")
    return None

# Get stops
def GetStop(route_id, direction_id, stop):
    StopLower = stop.lower()
    GetStopURL = f"{API_BASE_URL}/stops/{route_id}/{direction_id}"
    GetStopRequest = requests.get(GetStopURL, headers={'accept': 'application/json'})
    GetStopRequest.raise_for_status()
    Stops = GetStopRequest.json()

    for Stop in Stops:
        if StopLower in Stop['description'].lower():
            return Stop

    print(f"ERROR: Stop \'{stop}\' not found")
    return None

def GetTimeToNextTrip(route_id,direction_id,place_code):
    GetTimeToNextTripURL = f"{API_BASE_URL}/{route_id}/{direction_id}/{place_code}"
    GetTimeToNextTripRequest = requests.get(GetTimeToNextTripURL, headers={'accept': 'application/json'})
    GetTimeToNextTripRequest.raise_for_status()
    NextTime = GetTimeToNextTripRequest.json()

    if len(NextTime['departures']) > 0:
        return NextTime['departures'][0]['departure_time']
    else:
        return None

if __name__ == "__main__":
    route = GetRoute(BUS_ROUTE)
    print(route)
    
    direction = GetDirection(
        route['route_id'],
        DIRECTION
    )
    print(direction)

    stop = GetStop(
        route['route_id'],
        direction['direction_id'],
        BUST_STOP_NAME
    )
    print(stop)
    
    nexttime = GetTimeToNextTrip(
        route['route_id'],
        direction['direction_id'],
        stop['place_code']
    )
    print(nexttime)
