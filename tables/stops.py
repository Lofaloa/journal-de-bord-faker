from helpers import write_insert

STOP_TABLE = "stop"
STOP_TABLE_COLUMNS = "id, moment, odometer_value, location, driver_identifier"

def make_stop(id, moment, odometer, location, driver):
    return {
        "id": id,
        "moment": f"{{ts '{moment}'}}",
        "odometer": odometer,
        "location": location,
        "driver": f"'{driver}'"
    }

def write_stop(file, stop):
    values = (f"{stop['id']}, "
              f"{stop['moment']}, "
              f"{stop['odometer']}, "
              f"{stop['location']}, "
              f"{stop['driver']}"
    )
    write_insert(file, STOP_TABLE, STOP_TABLE_COLUMNS, values)