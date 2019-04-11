import numpy as np
import pandas as pd

df = pd.read_json("https://cdn-nfs.faireconomy.media/ff_calendar_thisweek.json")
data = pd.DataFrame(df)


data.columns = data.columns.str.replace('country', 'symbol')
data.columns = data.columns.str.replace('title', 'event')
data.columns = data.columns.str.replace('previous', 'prev_v')
data.columns = data.columns.str.replace('forecast', 'forecast_v')


data['impact'].replace(['Holiday', 'Low', 'Medium', 'High'], [0, 1, 2, 3], inplace=True)
data = data.reindex(columns=np.append(data.columns.values, ['actual_v', 'revised_v', 'FFevent_id']))
data['date'] = pd.to_datetime(data['date'])

data['time'] = data['date'].dt.time
data['date'] = data['date'].dt.date


data = data[['date', 'time', 'symbol', 'impact', 'event', 'actual_v', 'forecast_v', 'prev_v',  'revised_v', 'FFevent_id']]

try:
    data.to_csv('current.csv', index=False)
    data_old = pd.read_csv('archive.csv', index_col=False)
    print('old data found')
    pd.concat([data_old, data])
    data_old.to_csv('archive.csv', mode='a', index=False, header=False)

except(FileNotFoundError, IOError):
    data.to_csv('archive.csv', index=False)
    data_current = pd.read_csv('archive.csv', index_col=False)
    data_current.to_csv('current.csv', index=False)
    print('no old data found')




