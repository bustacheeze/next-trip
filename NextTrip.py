from asyncio import current_task
import requests, sys, time


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

    # Check for valid argument count
    if (len(sys.argv) < 4):
        print(f"ERROR: Invalid arguments, expected 3 and got {len(sys.argv)-1}.\nCorrect syntax: \'python NextTrip.py <ROUTE> <STOP> <DIRECTION>\'")
        exit()



    route = GetRoute(sys.argv[1])
    if (route):
        print(route)
    else:
        print(f"ERROR: Route \'{sys.argv[1]}\' was not found")
        exit()



    direction = GetDirection(
        route['route_id'],
        sys.argv[3]
    )
    if (direction):
        print(direction)
    else:
        print(f"ERROR: Direction \'{sys.argv[3]}\' was not valid for Route \'{sys.argv[1]}\'")
        exit()
    


    stop = GetStop(
        route['route_id'],
        direction['direction_id'],
        sys.argv[2]
    )
    if (stop):
        print(stop)
    else:
        print(f"ERROR: Stop \'{sys.argv[2]}\' was not valid for Route \'{sys.argv[1]}\' in Direction \'{sys.argv[3]}\'")
        exit()


    
    nexttime = GetTimeToNextTrip(
        route['route_id'],
        direction['direction_id'],
        stop['place_code']
    )
    if (nexttime):
        current_time = time.time()
        print(f"{int((nexttime - current_time) // 60)} minutes")
