from helpers import write_insert
from tables.locations import write_locations
from tables.rides import write_rides, Configuration

DRIVER_TABLE = "driver"
DRIVER_TABLE_COLUMNS = "identifier, objective"

def write_driver(file, driver):
    values = f"'{driver['identifier']}', {driver['objective']}"
    write_insert(file, DRIVER_TABLE, DRIVER_TABLE_COLUMNS, values)

def write_statements(file, driver, sequences, syntax):
    config = Configuration()
    config.stop_id_sequence = sequences["stop"]
    config.ride_id_sequence = sequences["ride"]
    config.sample_size = driver["rides"]
    config.syntax = syntax
    write_driver(file, driver)
    write_locations(file, driver["identifier"], sequences["location"], driver["locations"])
    write_rides(file, driver["identifier"], list(range(driver["locations"])), config)
    sequences["location"] += driver["locations"]
    sequences["stop"] += driver["rides"] * 2
    sequences["ride"] += driver["rides"]