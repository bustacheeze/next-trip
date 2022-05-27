import sys
from schedule import Schedule


if __name__ == "__main__":
    # Check for valid argument count
    if (len(sys.argv) < 4):
        print(f"ERROR: Invalid arguments, expected 3 and got {len(sys.argv)-1}.\nCorrect syntax: \'python NextTrip.py <ROUTE> <STOP> <DIRECTION>\'")
        exit()
    
    s = Schedule(sys.argv[1], sys.argv[3], sys.argv[2])
    s.init_data()
    next_departure = s.get_next_departure()
    if next_departure:
        print(next_departure)
