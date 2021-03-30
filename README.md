# Journal de bord faker
This is a simple utility script that I use to bootstrap the Journal de bord database with fake data.

## Installation
The script uses the [joke2k/faker](https://github.com/joke2k/faker) library. You should install it. You can do that using `pip install Faker`.

## Configuration

### Fields
- `drivers`: The list of drivers to write SQL statements for.
    - `identifier`: This is the user identifier.
    - `objective`: This is the number of kilometers the driver wants to complete.
    - `locations`: This is the number of random locations to generate.
    - `rides`: This is the number of random rides to generate.
- `output`: This is the path to the generated script.
- `syntax` (optional): This specifies the database syntax to use. This matters for the stop table statements. The moment field has a different syntax using H2 or PostgreSQL. It accepts two values: `h2` or `postgresql`. 

### Example

```json
{
    "drivers": [
        {
            "identifier": "bed1007d-84e9-4baf-adc2-f2a5504091af",
            "objective": 1500,
            "locations": 50,
            "rides": 1500
        },
        {
            "identifier": "e4cedd58-a3aa-4161-b578-f0c958ca5f03",
            "objective": 3000,
            "locations": 100,
            "rides": 1000
        }
    ],
    "output": "/home/user/Desktop/my_generated_script.sql"
}
```

## Usage

You run the `make` script. It accepts an optional command line argument. It is a path to the properties file to use. If no path is provided then the script search for `properties.json`.

```bash
> ./make [path to the properties file]

```