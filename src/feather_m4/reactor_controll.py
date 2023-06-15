import pandas as pd
import datetime as dt
import numpy as np
import time
import math
import json
import os
from enum import Enum


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


# class Control:
#     def __init__(self):
#         self.feedrate = 0.1
#         self.startup = True
#         self.feedrate_min = 0.14
#         self.feedrate_max = 0.4
#         self.feedrate_file = 'feedrate.json'

#         # check if the feedrate json file exists
#         if os.path.exists(self.feedrate_file):
#             with open(self.feedrate_file, 'r') as f:
#                 data = json.load(f)
#                 if 'feedrate' in data:
#                     self.feedrate = data['feedrate']
#             self.startup = False


    # def SetPump(self, current_now: float, latest_gradient: float) -> float:
    #     """
    #     This method calculates and sets the new feedrate based on the current and the latest gradient.
        
    #     Parameters:
    #     current_now (float): The current value.
    #     latest_gradient (float): The latest gradient value.

    #     Returns:
    #     float: The updated feedrate.
    #     """
    #     print('current now', current_now)
    #     print('latest gradient', latest_gradient)

    #     current_min = 25.00
    #     feedrate_step = 0.0001

    #     sign = int(math.copysign(1, latest_gradient))
    #     print('sign is', sign)



    #     if self.startup:
    #         print('System in start up phase')
    #         # self.feedrate = self.feedrate_min

            


    #         if current_now > current_min:
    #             self.feedrate += feedrate_step
    #             self.startup = False
    #     else:
    #         if (sign == 1 or sign == 0) and self.feedrate < self.feedrate_max:
    #             self.feedrate += feedrate_step
    #             print('System healthy increasing feed')

    #         elif (sign == -1) and self.feedrate >= self.feedrate_min:
    #             self.feedrate -= feedrate_step
    #             print('System overfed reducing feed')
    #         elif (sign == -1) and self.feedrate <= self.feedrate_min:
    #             self.feedrate += feedrate_step
    #             print('System starved increasing feed')
    #     print('Feedrate is', self.feedrate)

    #     with open(self.feedrate_file, 'w') as f:
    #         json.dump({'feedrate': self.feedrate}, f)


    #     return self.feedrate



class State(Enum):
    STARTUP = 1
    HEALTHY = 2
    OVERFED = 3
    STARVED = 4

class Control:
    def __init__(self):
        self.state = State.STARTUP
        self.feedrate_min = 0.13
        self.feedrate_max = 0.4
        self.feedrate = 0.1
        self.gradient_limit = -1.5
        self.feedrate_file = 'feedrate.json'
        # check if the feedrate json file exists
        if os.path.exists(self.feedrate_file):
            with open(self.feedrate_file, 'r') as f:
                data = json.load(f)
                if 'feedrate' in data:
                    self.feedrate = data['feedrate']
            self.startup = False




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

        current_min = 25.00
     
        feedrate_step = 0.0001

        sign = int(math.copysign(1, latest_gradient))
        print('sign is', sign)

        if self.state == State.STARTUP:
            # system has been running by previous manual operation / batch
            # current should be stable but low 

            print('System in start up phase')
            if current_now > current_min:
                self.feedrate += feedrate_step
                self.state = State.HEALTHY


        elif self.state == State.HEALTHY:
            if latest_gradient > self.gradient_limit and self.feedrate < self.feedrate_max:
            # The current monitred in the system has not shown a gradient drop above the set limit
            # the maximum feedrate has not been reached we infer the system is health and feeding should continue to be incresed 
                self.feedrate += feedrate_step
                print('State: Healthy')
                print('Increasing feedrate')
            elif(sign == -1):
                print('State: Overfed')
                print('Sginificant reduction in current has been detected, indicating the system to be overfed, feedrate will now reduce')
                self.state = State.OVERFED


        elif self.state == State.OVERFED:
            if self.feedrate >= self.feedrate_min and latest_gradient < self.gradient_limit:
                self.feedrate -= feedrate_step
                print('State: Overfed')
                print('System will reduce feedrate at high rate to recover')
            elif(sign == 1):
                print('State: Healthy')
                print('System has responded to feedrate reduction and will start to increase feeding again')
                self.state = State.HEALTHY
            else:
                self.state = State.STARVED


        elif self.state == State.STARVED:
            if self.feedrate <= self.feedrate_min:
                self.feedrate += 0.05
                print('State: Healthy')
                print('Feedrate instanuously stepped up to ovecome the effects of underfeeding')
                self.state = State.HEALTHY

        print('Feedrate is', self.feedrate)

        with open(self.feedrate_file, 'w') as f:
            json.dump({'feedrate': self.feedrate}, f)

        return self.feedrate