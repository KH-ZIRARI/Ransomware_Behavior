import glob
import json
import pandas as pd
import matplotlib.pyplot as plt

# Path to the folder containing the JSON files
folder_path = r'C:\json\*.json'

def extract_data_from_json(data):
    # Your extraction logic here
    return {
        "processes": [],  
        "network": {
            "udp": [],
            "http": [],
            "tcp": [],
            "hosts": []
        },
        "signatures": [],
        "marks": [],
        "behavior": {
            "generic": [],
            "apistats": [],
            "processes": [],
            "processtree": [],
            "summary": []
        }
    }

extracted_features_list = []

for file_path in glob.glob(folder_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        
        extracted_data = extract_data_from_json(data)
        
        extracted_features = {
            "file_name": file_path.split("\\")[-1],
            "duration": data["info"]["duration"],
            "score": data["info"]["score"],
            "signatures_count": len(data.get("signatures", [])),
            "tcp_connections_count": len(data.get("network", {}).get("tcp", [])),
            "udp_connections_count": len(data.get("network", {}).get("udp", [])),
            "http_connections_count": len(data.get("network", {}).get("http", [])),
            "files_created_count": len(data.get("behavior", {}).get("summary", {}).get("files_created", [])),
            "total_processes_created": len(data.get("behavior", {}).get("processes", [])),
            "total_api_calls_count": sum(len(stats) for stats in data.get("behavior", {}).get("apistats", {}).values()),
            "unique_signatures_triggered": len({sig["name"] for sig in data.get("signatures", [])})
        }
        
        extracted_features_list.append(extracted_features)

df = pd.DataFrame(extracted_features_list)

# Charts
plt.figure(figsize=(10, 6))

# Scatter plot for duration and score
plt.figure(figsize=(8, 6))
plt.scatter(df["duration"], df["score"], color='red', alpha=0.5)
plt.title("Scatter Plot: Duration vs. Score")
plt.xlabel("Duration")
plt.ylabel("Score")
plt.show()

