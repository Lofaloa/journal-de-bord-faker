#!/usr/bin/env python3

import sys

from helpers import make_random_string, make_moment, write_insert
from tables.locations import make_location, write_location, write_locations
from tables.rides import make_ride, write_ride, write_rides, Configuration

# Table names
DRIVER_TABLE = "driver"

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

        locations_count = 300
        write_locations(file, driver_identifier, locations_count)

        config = Configuration()
        config.sample_size = 100

        write_rides(file, driver_identifier, list(range(0, locations_count)), config)

        file.close()
    else:
        print(f"Usage: {sys.argv[0]} <file name> <driver identifier>")

if __name__ == "__main__":
    main()
