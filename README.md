# Journal de bord faker
This is a simple utility script that I use to bootstrap the Journal de bord database with fake data.

## Installation
The script uses the [joke2k/faker](https://github.com/joke2k/faker) library. You should install it. You can do that using `pip install Faker`.

## Usage
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