import json

REQUIRED_DRIVER_PROPERTIES = ["identifier", "objective", "locations", "rides"]

class PropertyError(Exception):
    pass

def has_properties(data, properties = []):
    return all([p in data for p in properties])

def require(data, property, prefix = ""):
    if property not in data:
        raise PropertyError(f"the \"{prefix}{property}\" property could not be found.")

def validate_driver(driver):
    for property in REQUIRED_DRIVER_PROPERTIES:
        require(driver, property, "drivers.")

def checked(properties):
    require(properties, "drivers")
    require(properties, "output")
    drivers = []
    for driver in properties["drivers"]:
        if driver["identifier"] in drivers:
            raise PropertyError(f"Duplicate driver: {driver['identifier']}")
        validate_driver(driver)
        drivers.append(driver["identifier"])
    return properties

def read_properties(file_name):
    with open(file_name) as proporties_file:
        return checked(json.load(proporties_file))