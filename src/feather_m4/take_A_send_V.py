import serial.tools.list_ports
import pandas as pd
from datetime import datetime
import os 
from reactor_controll import TrendGradientCalculator
from reactor_controll import time_check

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
csv_file = 'data.csv'

# Read data from Arduino
data_dict = {}
time_checker1 = time_check()
time_checker2 = time_check()

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

    

        data_log_time_check = 1
        if time_checker1.has_passed_minutes(data_log_time_check):
            time_checker1.reset()
            print(data_dict)
  
            if len(data_dict) == 7:

                df = pd.DataFrame(data_dict, index=[data_dict['datetime']])
                df = df.drop('datetime', axis=1)
                df = df.rename_axis('datetime') 
                
                

                # Append DataFrame to CSV if the file is empty
                if not os.path.isfile(csv_file) or os.stat(csv_file).st_size == 0:
                    df.to_csv(csv_file, mode='w', header=True)
                else:
                    df.to_csv(csv_file, mode='a', header=False)
        


        gradient_time_check = 3
        if time_checker2.has_passed_minutes(gradient_time_check):
            time_checker2.reset()

            try:
                df_live = pd.read_csv('data.csv')
        
            except FileNotFoundError:
                pass

            try:
                trend_calculator = TrendGradientCalculator(df_live)
                
            except NameError:
                pass

            try:
                gradient = trend_calculator.calculate_gradient()
                print("Gradient of A Current over the last minute:", gradient)
            except ValueError:
                pass




        