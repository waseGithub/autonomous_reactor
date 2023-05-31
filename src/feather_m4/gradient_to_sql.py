#!/usr/bin/env python
# coding: utf-8

import sqlite3
from google.cloud import storage
import pandas as pd 
import numpy as np
from datetime import datetime
import mysql.connector 
import sys 
import os
import pandas as pd





colnames = ['datetime','gradient_caluclated']
# data = pd.read_csv ('/home/harvey/Documents/PlatformIO/Projects/autonomous reactor feed/data.csv',  names=colnames, skiprows=  1)

data = pd.read_csv ('/home/wase/autonomous_reactor/src/feather_m4/gradient_data.csv', names=colnames, skiprows=  1)
#data = pd.read_csv (r'/home/farscopestudent/Documents/WASE/wase-cabinet/flowmeter_push.csv')  
data = pd.DataFrame(data)

def resample_mean(df, time, cols, round_val):
  df.dropna(inplace=True)
  df =  df[(df.astype(float) >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime')])[cols].mean() 
  df = df.round(round_val)
  return df

def resample_sum(df, time, cols, round_val):
  df.dropna(inplace=True)
  df= df[(df.astype(float) >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime')])[cols].sum()
  df = df.round(round_val)
  return df

def resample_max(df, time, cols, round_val):
  df.dropna(inplace=True)
  print(df)
  df= df[(df.astype(float) >= 0.0).all(1)]
  df = df.groupby([pd.Grouper(freq=time, level='datetime')])[cols].max()
  df = df.round(round_val)
  return df



data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
data.set_index(['datetime'], inplace=True)
data.reset_index(inplace=True)
data['datetime'] = data['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

print(data)



cnx = mysql.connector.connect(user='root', password='wase2022', host='34.89.81.147', database='autonomous_reactor')


 
cursor = cnx.cursor()
cols = "`,`".join([str(i) for i in data.columns.tolist()])
for i,row in data.iterrows():
    sql = "INSERT INTO `gradient_current` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))
    cnx.commit()


cnx.close()