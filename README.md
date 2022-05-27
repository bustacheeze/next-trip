# Next-Trip
Next-Trip will tell you how long until the next departure time for a Metro Transit line from a given stop and direction of travel. Next-Trip uses real-time data provided by the NexTrip API v2.
https://svc.metrotransit.org


## Installation
Clone the repository and run nextdeparture.py with Python. Next-Trip requires the requests module which can be installed with pip manually or with the requirements file.
```
git clone https://github.com/bustacheeze/next-trip.git
cd next-trip
python -m pip install -r requirements.txt
```

### Quick Start
```
# Syntax
python nextdeparture.py <METRO_LINE> <STATION> <DIRECTION>
    
# Example
python nextdeparture.py "METRO Blue Line" "Mall of America" "North"
```

Next-Trip will output the the time until the next departure formatted as 'X minutes' where X is an integer. If there are no more departures from the stop for the day, then there will be no output.
