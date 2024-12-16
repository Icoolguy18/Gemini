from data_opener import data_handler
import os

data_path = input(r'Input your path:').strip('"')
data_path = rf"{data_path}" 
absolute_path = os.path.abspath(data_path)
print(absolute_path)
handler = data_handler()
data = data_handler.handle_external_dataset(absolute_path)

data = data['metadata']
print(data)

#till here, the data provided, we are able to export the metadata 

file_info = {
 'file_path': 'C:\\Users\\ojas2\\OneDrive\\Desktop\\TUF\\b.tech\\data sciences\\practice workbook\\google-stock-dataset-Daily.csv', 
 'type': 'tabular', 
 'metadata': {'num_rows': 2510, 'columns': ['Unnamed: 0', 'Date', 'Price', 'High', 'Low', 'Close', 'Volume', 'Adj Close']}, 
 'examples': [{'Unnamed: 0': 0, 'Date': '2013-04-15', 'Price': 19.67, 'High': 19.94, 'Low': 19.44, 'Close': 19.57, 'Volume': 98025876, 'Adj Close': 19.57}, 
              {'Unnamed: 0': 1, 'Date': '2013-04-16', 'Price': 19.68, 'High': 19.92, 'Low': 19.62, 'Close': 19.85, 'Volume': 69610320, 'Adj Close': 19.85}, 
              {'Unnamed: 0': 2, 'Date': '2013-04-17', 'Price': 19.69, 'High': 19.79, 'Low': 19.47, 'Close': 19.58, 'Volume': 81398520, 'Adj Close': 19.58}, 
              {'Unnamed: 0': 3, 'Date': '2013-04-18', 'Price': 19.65, 'High': 19.66, 'Low': 19.05, 'Close': 19.17, 'Volume': 132767100, 'Adj Close': 19.17}, 
              {'Unnamed: 0': 4, 'Date': '2013-04-19', 'Price': 19.25, 'High': 20.11, 'Low': 19.18, 'Close': 20.02, 'Volume': 231895872, 'Adj Close': 20.02}]
 }