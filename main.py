import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from collections import Counter

df = pd.read_csv('crashes.csv')
print(df.head())

dates = pd.to_datetime(df['Date'])

years = sorted([date.year for date in dates])
dic = Counter(years)

plt.plot(dic.keys(), dic.values())
plt.savefig('crashes_year.png')
