import random
from datetime import datetime, timedelta
from helpers import write_insert, make_moment
from tables.stops import make_stop, write_stop

RIDE_TABLE = "ride"
RIDE_TABLE_COLUMNS = "id, departure_id, arrival_id, comment, traffic_condition, driver_identifier"

def make_ride(id, departure, arrival, comment, traffic, driver):
    return {
        "id": id,
        "departure": departure,
        "arrival": arrival,
        "comment": f"'{comment}'",
        "traffic": traffic,
        "driver": f"'{driver}'"
    }

def write_ride(file, ride):
    values = (f"{ride['id']}, "
              f"{ride['departure']}, "
              f"{ride['arrival']}, "
              f"{ride['comment']}, "
              f"{ride['traffic']}, "
              f"{ride['driver']}"
    )
    write_insert(file, RIDE_TABLE, RIDE_TABLE_COLUMNS, values)

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