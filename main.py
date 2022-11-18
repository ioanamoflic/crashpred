from typing import Tuple

import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from collections import Counter
import geopy as gp
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pycountry_convert as pc
import numpy as np

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
    "Kentucky": "USA",
    "Louisiana": "USA",
    "Maine": "USA",
    "Maryland": "USA",
    "Massachusetts": "USA",
    "Michigan": "USA",
    "Minnesota": "USA",
    "Mississippi": "USA",
    "Missouri": "USA",
    "Montana": "USA",
    "Nebraska": "USA",
    "Nevada": "USA",
    "New Hampshire": "USA",
    "New Jersey": "USA",
    "New Mexico": "USA",
    "New York": "USA",
    "North Carolina": "USA",
    "North Dakota": "USA",
    "Ohio": "USA",
    "Oklahoma": "USA",
    "Oregon": "USA",
    "Pennsylvania": "USA",
    "Rhode Island": "USA",
    "South Carolina": "USA",
    "South Dakota": "USA",
    "Tennessee": "USA",
    "Texas": "USA",
    "Utah": "USA",
    "Vermont": "USA",
    "Virginia": "USA",
    "Washington": "USA",
    "West Virginia": "USA",
    "Wisconsin": "USA",
    "Wyoming": "USA",
    "District of Columbia": "USA",
    "American Samoa": "USA",
    "Guam": "USA",
    "Northern Mariana Islands": "USA",
    "Puerto Rico": "USA",
    "United States Minor Outlying Islands": "USA",
    "U.S. Virgin Islands": "USA",
    "England": "Europe",
    "USSR": "Asia",
    "Soviet Union": "Asia",
    "Czechoslovakia": "Europe",
    "Yugoslavia": "Europe"
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
        if country in us_state_to_abbrev:
            return us_state_to_abbrev[country]
        words = country.split()
        if len(words) > 1:
            # print(words[-1])
            return get_continent(words[-1])
        return "Continent not found"


df = pd.read_csv('crashes.csv')
dates = pd.to_datetime(df['Date'])
addresses = df['Location']

continents = [get_continent(str(address).split(',')[-1].strip()) for address in addresses]
locations = [str(address).split(',')[-1].strip() for address in addresses]
con_loc = [tup for tup in zip(locations, continents) if tup[1] == "Continent not found"]

new_dict = {}
for (key,value) in con_loc:
    if key not in new_dict:
        new_dict[key] = 1
    else:
        new_dict[key] += 1

print(new_dict)

new_dict = dict((key, value) for (key,value) in con_loc)
#print(*zip(locations, continents))

# years = sorted([date.year for date in dates])
# dic = Counter(years)
#
# plt.plot(dic.keys(), dic.values())
# plt.savefig('crashes_year.png')

#print(len(np.where(np.array(continents)=="Continent not found")[0]))