import pandas as pd
import glob
import json

def read_json_files(directory_path):
    # Corrected to use the provided path with the wildcard for JSON files
    file_paths = glob.glob(directory_path)
    data = []
    
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data.append(json.load(file))
    
    return data

# Example usage with the specified path including the wildcard for JSON files
directory_path = 'C:\\json\\*.json'
data = read_json_files(directory_path)
print(f"Total JSON files read: {len(data)}")

# Assuming 'data' is the list of JSON objects you've loaded
first_report = data[0]
print(first_report.keys())