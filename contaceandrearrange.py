import pandas
import numpy as np

data = pandas.read_csv('otp.csv', index_col=False)
data_old = pandas.read_csv('test.csv', index_col=False)

data.columns = data.columns.str.replace('country', 'symbol')
data.columns = data.columns.str.replace('title', 'event')
data.columns = data.columns.str.replace('previous', 'prev_v')
data.columns = data.columns.str.replace('forecast', 'forecast_v')

new = data["date"].str.split("T", n=1, expand=True)
data["Date"] = new[0]
data["time"] = new[1]
data.drop(columns =["date"], inplace=True)
new = data["time"].str.split("-", n=1, expand=True)
data["Time"] = new[0]
data.drop(columns=["time"], inplace=True)
data = data.reindex(columns=np.append(data.columns.values, ['actual_v', 'revised_v', 'FFevent_id']))

data = data[['Date', 'Time', 'symbol', 'impact', 'event', 'actual_v', 'forecast_v', 'prev_v',  'revised_v', 'FFevent_id']]

data.to_csv('otp.csv')
pandas.concat([data_old, data])
data.to_csv('test.csv', mode='a', index=False, header=False)
print(data)
