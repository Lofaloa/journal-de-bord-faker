import random
from faker import Faker
from datetime import datetime, timedelta
from helpers import write_insert, write_sequence, make_moment
from tables.stops import make_stop, write_stop

RIDE_TABLE = "ride"
RIDE_SEQUENCE = "ride_sequence"
RIDE_TABLE_COLUMNS = "id, departure_id, arrival_id, comment, traffic_condition, driver_identifier"
STOP_SEQUENCE = "stop_sequence"

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

def random_ride_duration(max_hours = 5, max_minutes = 60):
    return timedelta(
        hours=random.randrange(max_hours),
        minutes=random.randrange(max_minutes)
    )

def random_time_step(max_hours = 72, max_minutes = 60):
    return timedelta(hours=random.randrange(max_hours))

class Configuration:
    sample_size = 10
    stop_id_sequence = 0
    stop_id_step = 1
    ride_id_sequence = 0
    ride_id_step = 1
    min_odometer_start = 1_000
    max_odometer_start = 10_000
    min_ride_distance = 10
    max_ride_distance = 200
    max_comment_size = 255
    traffic_condition_values = 5

def write_rides(file, driver, locations, config = Configuration()):
    fake = Faker()
    Faker.seed(0)
    stop_id = config.stop_id_sequence
    current_moment = fake.date_time_between(start_date="-1y", end_date="now")
    odometer = random.randrange(config.min_odometer_start, config.max_odometer_start)

    for i in range(config.ride_id_sequence, config.ride_id_sequence + config.sample_size, config.ride_id_step):
        moment = make_moment(current_moment)
        location = random.choice(locations)

        departure = stop_id
        write_stop(file, make_stop(stop_id, moment, odometer, location, driver))

        ride_duration = random_ride_duration()
        current_moment = current_moment + ride_duration
        moment = make_moment(current_moment)
        odometer += random.randrange(config.min_ride_distance, config.max_ride_distance)
        stop_id += config.stop_id_step

        arrival = stop_id
        write_stop(file, make_stop(stop_id, moment, odometer, location, driver))

        traffic = random.randrange(config.traffic_condition_values)
        comment = fake.text(max_nb_chars=config.max_comment_size)

        write_ride(file, make_ride(i, departure, arrival, comment, traffic, driver))

        current_moment = current_moment - ride_duration
        current_moment = current_moment + random_time_step()
        stop_id += config.stop_id_step

    write_sequence(file, RIDE_SEQUENCE, config.sample_size)
    write_sequence(file, STOP_SEQUENCE, stop_id)