import serial.tools.list_ports
import pandas as pd
from datetime import datetime
import os 
# from reactor_controll import TrendGradientCalculator
from reactor_controll import TimeCheck
from reactor_controll import set_pump
import numpy as np
import json
import math


board_serial_number = 'D81E4C5053374E4D4C202020FF0F1631'  
port = None

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p.serial_number)
    if p.serial_number == board_serial_number:
        port = p.device
        break

if port is None:
    print(f"Arduino board with serial number {board_serial_number} not found.")
    exit()

board_baud_rate = 115200
ser = serial.Serial(port, board_baud_rate)

# CSV file path
csv_file = 'adalogger_data.csv'


# Read data from Arduino
data_dict = {}
gradient_dict = {}
time_checker1 = time_check()
time_checker2 = time_check()
latest_gradient = 0 
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()

        lines = line.split('\n')
        for line in lines:
            line = line.strip()
      
            if line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                data_dict[key] = value
            
        
        data_dict['datetime'] = str(datetime.now())

        
            

        # print(data_dict)
        

        


        
       



        

    

        data_log_time_check = 0.1
        if time_checker1.has_passed_minutes(data_log_time_check):
            time_checker1.reset()


            try:
                with open('gradient_data.json', 'r') as file:
                    data = json.load(file)
                    latest_gradient = data['latest_gradient']
            except json.decoder.JSONDecodeError:
                pass
            print(data_dict)
            print("Latest Gradient:", latest_gradient)
  
            if len(data_dict) == 5:

                df = pd.DataFrame(data_dict, index=[data_dict['datetime']])
                df = df.drop('datetime', axis=1)
                df = df.rename_axis('datetime') 
                
                
                if not os.path.isfile(csv_file) or os.stat(csv_file).st_size == 0:
                    df.to_csv(csv_file, mode='w', header=True)
                else:
                    df.to_csv(csv_file, mode='a', header=False)

            

                # Extract the data value
            

            df = pd.read_csv('adalogger.csv')
            
            df['A Current'] = df['A Current'].str.replace(' mA', '').astype(float)
            if len(df) >= 30:
                current_now = df['A Current'].tail(30).mean()
            else: 
                current_now = 0

            response_voltage = set_pump(current_now, latest_gradient)
            # response_voltage = str(sign_text[sign]) 
            ser.write(str(response_voltage).encode())
        


        # gradient_time_check = 10
        # if time_checker2.has_passed_minutes(gradient_time_check):
        #     time_checker2.reset()

        #     try:
        #         df_live = pd.read_csv('adalogger_data.csv')
        #         print(df_live.tail(10))
        #         trend_calculator = TrendGradientCalculator(df_live)
        
        #     except FileNotFoundError:
        #         pass

         
                
     
            # try:
            #     gradient = trend_calculator.calculate_gradient()
            #     gradient_dict['datetime'] = str(datetime.now())
            #     gradient_dict['gradient_caluclated'] = gradient

            #     df = pd.DataFrame(gradient_dict, index=[gradient_dict['datetime']])
            #     df = df.drop('datetime', axis=1)
            #     df = df.rename_axis('datetime') 

            #     if not os.path.isfile(csv_file2) or os.stat(csv_file2).st_size == 0:
            #         df.to_csv(csv_file2, mode='w', header=True)
            #     else:
            #         df.to_csv(csv_file2, mode='a', header=False)
        

            #     print("Gradient of A Current over the last minute:", gradient)
            # except ValueError:
            #     pass
            # except np.linalg.LinAlgError:
            #     pass




        