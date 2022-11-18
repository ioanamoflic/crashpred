from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from collections import Counter
import geopy as gp
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pycountry_convert as pc


us_state_to_abbrev = {
    "Alabama": "USA",
    "Alaska": "USA",
    "Arizona": "USA",
    "Arkansas": "USA",
    "California": "USA",
    "Colorado": "USA",
    "Connecticut": "USA",
    "Delaware": "USA",
    "Florida": "USA",
    "Georgia": "USA",
    "Hawaii": "USA",
    "Idaho": "USA",
    "Illinois": "USA",
    "Indiana": "USA",
    "Iowa": "USA",
    "Kansas": "USA",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

def get_continent_name(continent_code: str) -> str:
    continent_dict = {
        "NA": "North America",
        "SA": "South America",
        "AS": "Asia",
        "AF": "Africa",
        "OC": "Oceania",
        "EU": "Europe",
        "AQ": "Antarctica"
    }
    return continent_dict[continent_code]


def get_continent(country: str) -> str:
    try:
        country_code = pc.country_name_to_country_alpha2(country, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = get_continent_name(continent_code)
        return continent_name
    except:
        return 'fuck you stan'


df = pd.read_csv('crashes.csv')
dates = pd.to_datetime(df['Date'])
addresses = df['Location']

continents = [get_continent(str(address).split(',')[-1].strip()) for address in addresses]
locations = [str(address).split(',')[-1].strip() for address in addresses]
print(*zip(locations, continents))

# years = sorted([date.year for date in dates])
# dic = Counter(years)
#
# plt.plot(dic.keys(), dic.values())
# plt.savefig('crashes_year.png')
