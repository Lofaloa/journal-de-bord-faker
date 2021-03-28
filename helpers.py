import random
import string

def write_insert(file, table_name, columns, values):
    file.write(f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n")

def write_sequence(file, sequence_name, value):
    file.write(f"ALTER SEQUENCE {sequence_name} RESTART WITH {value};\n")

def make_random_string(size):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(size))

def make_moment(d):
    return d.strftime("%Y-%m-%d %H:%M:%S.00")