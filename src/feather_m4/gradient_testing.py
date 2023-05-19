
from reactor_controll import TrendGradientCalculator
import csv
import pandas as pd

df = pd.read_csv('data.csv')

trend_calculator = TrendGradientCalculator(df)
gradient = trend_calculator.calculate_gradient()
print("Gradient of A Current over the last minute:", gradient)
