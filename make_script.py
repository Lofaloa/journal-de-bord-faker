#!/usr/bin/env python3

import sys
import string
import random
from datetime import datetime, timedelta

# Table names
DRIVER_TABLE = "driver"
RIDE_TABLE = "ride"
STOP_TABLE = "stop"
LOCATION_TABLE = "location"

# Table columns
RIDE_TABLE_COLUMNS = "id, departure_id, arrival_id, comment, traffic_condition, driver_identifier"
STOP_TABLE_COLUMNS = "id, moment, odometer_value, location, driver_identifier"
LOCATION_TABLE_COLUMNS = "id, name, latitude, longitude, driver_identifier"

# SQL statements
INSERT_INTO = "INSERT INTO"
VALUES = "VALUES"

def make_location(id, name, latitude, longitude, driver):
    return {
        "id": id,
        "name": f"'{name}'",
        "latitude": latitude,
        "longitude": longitude,
        "driver": f"'{driver}'"
    }

def make_stop(id, moment, odometer, location, driver):
    return {
        "id": id,
        "moment": f"{{ts '{moment}'}}",
        "odometer": odometer,
        "location": location,
        "driver": f"'{driver}'"
    }

def make_ride(id, departure, arrival, comment, traffic, driver):
    return {
        "id": id,
        "departure": departure,
        "arrival": arrival,
        "comment": f"'{comment}'",
        "traffic": traffic,
        "driver": f"'{driver}'"
    }

def write_insert(file, table_name, columns, values):
    file.write(f"{INSERT_INTO} {table_name} ({columns}) {VALUES} ({values});\n")

def make_random_string(size):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(size))

def make_moment(d):
    return d.strftime("%Y-%m-%d %H:%M:%S.00")

def write_location(file, location):
    values = (f"{location['id']}, "
              f"{location['name']}, "
              f"{location['latitude']}, "
              f"{location['longitude']}, "
              f"{location['driver']}"
    )
    write_insert(file, LOCATION_TABLE, LOCATION_TABLE_COLUMNS, values)

def write_stop(file, stop):
    values = (f"{stop['id']}, "
              f"{stop['moment']}, "
              f"{stop['odometer']}, "
              f"{stop['location']}, "
              f"{stop['driver']}"
    )
    write_insert(file, STOP_TABLE, STOP_TABLE_COLUMNS, values)

def write_ride(file, ride):
    values = (f"{ride['id']}, "
              f"{ride['departure']}, "
              f"{ride['arrival']}, "
              f"{ride['comment']}, "
              f"{ride['traffic']}, "
              f"{ride['driver']}"
    )
    write_insert(file, RIDE_TABLE, RIDE_TABLE_COLUMNS, values)

def write_locations(file, driver, sample_count = 10):
    names = []
    for i in range(0, sample_count + 1):
        name = make_random_string(10)
        while name in names:
            name = make_random_string(10)
        names.append(name)
        write_location(file, make_location(i, name, 0.0, 0.0, driver))
    file.write(f"alter sequence location_sequence restart with {sample_count + 1};\n")

def write_rides(file, driver, locations, sample_count = 10):
    names = []
    stop_id = 0
    current_moment = datetime.now()
    odometer = 1000
    for i in range(0, sample_count + 1):
        moment = make_moment(current_moment)
        location = random.choice(locations)

        # departure
        departure = stop_id
        write_stop(file, make_stop(stop_id, moment, odometer, location, driver))

        # update
        current_moment = current_moment + timedelta(hours=1)
        moment = make_moment(current_moment)
        odometer += random.randrange(100)
        stop_id += 1

        # arrival
        arrival = stop_id
        write_stop(file, make_stop(stop_id, moment, odometer, location, driver))

        write_ride(file, make_ride(i, departure, arrival, "comment", 1, driver))

        # One ride a day!
        current_moment = current_moment - timedelta(hours=1)
        current_moment = current_moment + timedelta(days=1)
        stop_id += 1

    file.write(f"alter sequence ride_sequence restart with {sample_count + 1};\n")
    file.write(f"alter sequence stop_sequence restart with {stop_id + 1};\n")

def write_driver(file, identifier):
    write_insert(file, "driver", "identifier, objective", f"'{identifier}', 1000")

def main():

    if len(sys.argv) == 3:
        file_name = sys.argv[1]
        driver_identifier = sys.argv[2]

        print(f"About to open the '{file_name}' file and write the script...\n")
        file = open(file_name, "w+");
        
        print(f"Writing driver with id {driver_identifier}.")
        write_driver(file, driver_identifier)

        locations_count = 15
        write_locations(file, driver_identifier, locations_count)
        write_rides(file, driver_identifier, list(range(0, locations_count + 1)), 100)

        file.close()
    else:
        print(f"Usage: {sys.argv[0]} <file name> <driver identifier>")

if __name__ == "__main__":
    main()
