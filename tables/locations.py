import random
from faker import Faker
from helpers import write_insert, write_sequence, make_random_string

LOCATION_TABLE = "location"
LOCATION_SEQUENCE = "location_sequence"
LOCATION_TABLE_COLUMNS = "id, name, latitude, longitude, driver_identifier"

def make_location(id, name, latitude, longitude, driver):
    return {
        "id": id,
        "name": f"'{name}'",
        "latitude": latitude,
        "longitude": longitude,
        "driver": f"'{driver}'"
    }

def random_lname_size(min, max):
    return random.randint(min, max)

def random_location_name(fake, excluded = []):
    name = fake.city()
    while name in excluded:
        name = fake.city()
    return name

def write_location(file, location):
    values = (f"{location['id']}, "
              f"{location['name']}, "
              f"{location['latitude']}, "
              f"{location['longitude']}, "
              f"{location['driver']}"
    )
    write_insert(file, LOCATION_TABLE, LOCATION_TABLE_COLUMNS, values)

def write_locations(file, driver, location_sequence = 0, count = 10):
    names = []
    fake = Faker()
    Faker.seed(0)
    for id in range(location_sequence, location_sequence + count):
        name = random_location_name(fake, names)
        write_location(file, make_location(id, name, fake.latitude(), fake.longitude(), driver))
        names.append(name)
    write_sequence(file, LOCATION_SEQUENCE, count)