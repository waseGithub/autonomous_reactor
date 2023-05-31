import pandas as pd
import datetime as dt
import numpy as np
import time




# class TrendGradientCalculator:
#     def __init__(self, dataframe):
#         self.dataframe = dataframe
    
#     def calculate_gradient(self):
#         # Convert the 'datetime' column to pandas datetime format
#         self.dataframe['datetime'] = pd.to_datetime(self.dataframe['datetime'])
            
#         # Sort the DataFrame by datetime in ascending order
#         self.dataframe.sort_values('datetime', inplace=True)
            
#         # Set the 'datetime' column as the DataFrame index
#         self.dataframe.set_index('datetime', inplace=True)
            
#         # Filter the DataFrame for the last three minutes of data
#         start_time = self.dataframe.index[-1] - dt.timedelta(minutes=60)
#         last_minute_df = self.dataframe[start_time:]
            
#         # Convert the 'A Current' column to float
#         last_minute_df['A Current'] = last_minute_df['A Current'].str.replace(' mA', '').astype(float)
        
#         # # Calculate the rolling mean with a window size of 10
#         # last_minute_df['A Current'] = last_minute_df['A Current'].rolling(window=20).mean()

#         # Calculate the gradient using NumPy's polyfit function
#         x = (last_minute_df.index - last_minute_df.index[0]).total_seconds()
#         y = last_minute_df['A Current']
#         gradient = np.polyfit(x, y, 1)[0]
            
#         return gradient

    

class time_check:
    def __init__(self):
        self.last_event_time = time.time()
        
    def has_passed_minutes(self, minutes):
        current_time = time.time()
        elapsed_time = (current_time - self.last_event_time) / 60  # convert to minutes
        return elapsed_time >= minutes

    def reset(self):
        self.last_event_time = time.time()