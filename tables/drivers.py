from helpers import write_insert
from tables.locations import write_locations
from tables.rides import write_rides, Configuration

DRIVER_TABLE = "driver"
DRIVER_TABLE_COLUMNS = "identifier, objective"

def write_driver(file, driver):
    values = f"'{driver['identifier']}', {driver['objective']}"
    write_insert(file, DRIVER_TABLE, DRIVER_TABLE_COLUMNS, values)

def write_statements(file, driver):
    config = Configuration()
    config.sample_size = driver["rides"]
    write_locations(file, driver, driver["locations"])
    write_rides(file, driver, list(range(driver["locations"])), config)