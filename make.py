#!/usr/bin/env python3

import sys
import json

from properties import read_properties, PropertyError
from tables.drivers import write_statements

DEFAULT_PROPERTIES_FILE = "properties.json"

def file_name_specified():
    return len(sys.argv) == 2

def is_valid(syntax):
    return syntax == "h2" or syntax == "postgresql"

def read_syntax(properties):
    if "syntax" in properties and is_valid(properties["syntax"]):
        return properties["syntax"]
    elif "syntax" in properties and not is_valid(properties["syntax"]):
        return "h2"
    else:
        raise PropertyError(f"Invalid syntax name: {properties['syntax']}")


def main():
    try:
        properties_file_name = sys.argv[1] if file_name_specified() else DEFAULT_PROPERTIES_FILE
        properties = read_properties(properties_file_name)
        syntax = read_syntax(properties)
        sequences = { "location": 0, "stop": 0, "ride": 0 }
        with open(properties["output"], "w+") as sql_script:
            for driver in properties["drivers"]:
                print((f"About to write {driver['rides']} rides and "
                       f"{driver['locations']} locations for driver"
                       f" with id \"{driver['identifier']}\"."))
                write_statements(sql_script, driver, sequences, syntax)
                print((f"\nSequences updates:\n"
                       f"\tLocation table sequence: {sequences['location']}.\n"
                       f"\tStop table sequence: {sequences['stop']}.\n"
                       f"\tRide table sequence: {sequences['ride']}.\n"))
                print("Done!\n")
            print(f"SQL statements written to \"{properties['output']}\".")
    except PropertyError as e:
        print(f"Failed to read properties: {str(e)}")

if __name__ == "__main__":
    main()
