import pandas as pd
import datetime as dt
import numpy as np

class TrendGradientCalculator:
    def __init__(self, dataframe):
        self.dataframe = dataframe
    
    def calculate_gradient(self):
        # Convert the 'datetime' column to pandas datetime format
        self.dataframe['datetime'] = pd.to_datetime(self.dataframe['datetime'])
        
        # Sort the DataFrame by datetime in ascending order
        self.dataframe.sort_values('datetime', inplace=True)
        
        # Set the 'datetime' column as the DataFrame index
        self.dataframe.set_index('datetime', inplace=True)
        
        # Calculate the difference in seconds between the last and first timestamps
        time_diff = (self.dataframe.index[-1] - self.dataframe.index[0]).total_seconds()
        
        # Filter the DataFrame for the last minute of data
        start_time = self.dataframe.index[-1] - dt.timedelta(minutes=3)
        last_minute_df = self.dataframe[start_time:]
        
        # Calculate the gradient using NumPy's polyfit function
        x = (last_minute_df.index - last_minute_df.index[0]).total_seconds()
        y = last_minute_df['A Current'].str.replace(' mA', '').astype(float)
        gradient = np.polyfit(x, y, 1)[0]
        
        return gradient