
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import date
from collections import Counter
import geopy as gp
from geopy import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pycountry_convert as pc
import numpy as np

df = pd.read_csv('expeditions.csv')

def get_timespan(datetime, timespan_name):
    if timespan_name  == 'month':
        return datetime.month
    return datetime.year


    for i, expedition in df.iterrows():
        timespan = get_timespan(pd.to_datetime(expedition['basecamp_date']), timespan_name)
        if timespan not in all_results:
            all_results[timespan] = 1
        else:
            all_results[timespan] += 1

def get_success_percentage(timespan_name):
    succ_results = {}
    all_results = {}
    per_results = {}

    for i, expedition in df.iterrows():
        timespan = get_timespan(pd.to_datetime(expedition['basecamp_date']), timespan_name)
        if timespan not in all_results:
            all_results[timespan] = 1
        else:
            all_results[timespan] += 1

        if expedition['termination_reason'].split()[0] == 'Success':
            if timespan not in succ_results:
                succ_results[timespan] = 1
            else:
                succ_results[timespan] += 1

    for key in all_results:
        if isinstance(key, int) and key in succ_results:
            per_results[key] = succ_results[key] / all_results[key]
        elif isinstance(key, int):
            per_results[key] = 0
    return dict(sorted(per_results.items(), key=lambda x: x[0]))


per_results = get_success_percentage('month')

plt.plot(per_results.keys(), per_results.values())
plt.savefig(f'success_per_month.png', dpi=300)
plt.clf()


per_results = get_success_percentage('year')
plt.plot(per_results.keys(), per_results.values())
plt.savefig(f'success_per_year.png', dpi=300)
