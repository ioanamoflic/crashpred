import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('expeditions.csv')


def get_timespan(datetime, timespan_name):
    if timespan_name == 'month':
        return datetime.month
    return datetime.year


def get_success_percentage(feature: str, df):
    succ_results = {}
    all_results = {}
    per_results = {}

    for i, expedition in df.iterrows():
        if feature == 'month' or feature == 'year':
            feature_value = get_timespan(pd.to_datetime(expedition['basecamp_date']), feature)
        else:
            feature_value = expedition[feature]

        if feature_value not in all_results:
            all_results[feature_value] = 1
        else:
            all_results[feature_value] += 1

        if expedition['termination_reason'].split()[0] == 'Success':
            if feature_value not in succ_results:
                succ_results[feature_value] = 1
            else:
                succ_results[feature_value] += 1

    for key in all_results:
        if (isinstance(key, int) or isinstance(key, bool)) and key in succ_results:
            per_results[key] = succ_results[key] / all_results[key]
        elif isinstance(key, int) or isinstance(key, bool):
            per_results[key] = 0

    # print(dict(sorted(all_results.items(), key=lambda x: x[0])))
    return dict(sorted(per_results.items(), key=lambda x: x[0]))


def save_plot(feature, df):
    per_results = get_success_percentage(feature, df)
    plt.plot(per_results.keys(), per_results.values())
    plt.savefig(f'success_per_{feature}.png', dpi=300)
    plt.clf()


peaks = ['Everest', 'Ama Dablam', 'Cho Oyu']
df_peaks = df[df["peak_name"].isin(peaks)]
df_peaks_subset = df_peaks[df_peaks['hired_staff'] < 20]
df_peaks_subset['year'] = pd.to_datetime(df_peaks_subset['basecamp_date']).map(lambda x: x.year)

df_peaks_subset['success'] = df_peaks_subset['termination_reason'].map(lambda x: ('Success' in x) is True)
df_peaks_subset = df_peaks_subset[df_peaks_subset['year'] >= 1981]

left_q = df_peaks_subset.groupby(['year', 'oxygen_used']).count().rename(columns={'expedition_id': 'attempts'})
right_q = df_peaks_subset[df_peaks_subset['success'] == True].groupby(['year', 'oxygen_used']).count()
merged_q = pd.merge(left_q, right_q, how='left', left_on=['year', 'oxygen_used'], right_on=['year', 'oxygen_used'])
merged_q = merged_q[['attempts', 'success_y']]
merged_q.fillna(0, inplace=True)
merged_q.reset_index(inplace=True)
merged_q = merged_q.astype(int)
merged_q.to_csv('out.csv', index=False)

# save_plot('month', df_peaks_subset)
# save_plot('year', df_peaks_subset)
# save_plot('oxygen_used', df_peaks_subset)
# save_plot('hired_staff', df_peaks_subset)
