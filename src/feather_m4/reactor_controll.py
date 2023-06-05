import pandas as pd
import datetime as dt
import numpy as np
import time
import math




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

    

class TimeCheck:
    """
    A class used to track the time elapsed since a particular event.

    Attributes:
    last_event_time (float): The time of the last event, in seconds since the epoch.

    Methods:
    has_passed_minutes(minutes): Returns True if the specified number of minutes has elapsed since the last event.
    reset(): Resets the last event time to the current time.
    """
    
    def __init__(self):
        """
        Initializes the TimeCheck with the current time as the last event time.
        """
        self.last_event_time = time.time()
        
    def has_passed_minutes(self, minutes: float) -> bool:
        """
        Checks if the specified number of minutes has elapsed since the last event.

        Parameters:
        minutes (float): The number of minutes to check.

        Returns:
        bool: True if the specified number of minutes has elapsed since the last event, False otherwise.
        """
        current_time = time.time()
        elapsed_time = (current_time - self.last_event_time) / 60  # convert to minutes
        return elapsed_time >= minutes

    def reset(self):
        """
        Resets the last event time to the current time.
        """
        self.last_event_time = time.time()


class Control:
    def __init__(self):
        self.feedrate = 0.0

    def SetPump(self, current_now: float, latest_gradient: float) -> float:
        """
        This method calculates and sets the new feedrate based on the current and the latest gradient.
        
        Parameters:
        current_now (float): The current value.
        latest_gradient (float): The latest gradient value.

        Returns:
        float: The updated feedrate.
        """
        print('current now', current_now)
        print('latest gradient', latest_gradient)
        sign = int(math.copysign(1, latest_gradient))
        sign_text = {
                        1: 1,
                        -1: -1,
                        0: 0
                    }
        
        feedrate_step = 0.005
        current_min = 25.00

        if current_now > current_min: 
            if sign_text[sign] == 1 or sign_text[sign] == 0:
                self.feedrate += feedrate_step
            else :
                self.feedrate = 0
        else :
            self.feedrate = 0
        
        return self.feedrate

    