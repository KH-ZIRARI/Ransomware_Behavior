import glob
import json
from collections import Counter
import matplotlib.pyplot as plt
import os
import pandas as pd

def analyse_json_files(folder_path):
    registry_changes = Counter()
    ransomware_registry_changes = Counter()
    
    for file_path in glob.glob(os.path.join(folder_path, '*.json')):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Assume that each file represents a distinct ransomware
                ransomware_name = os.path.basename(file_path)
                if 'behavior' in data and 'summary' in data['behavior']:
                    regkeys = data['behavior']['summary'].get('regkey_written', [])
                    for key in regkeys:
                        registry_changes[key] += 1
                        ransomware_registry_changes[ransomware_name] += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return registry_changes, ransomware_registry_changes

# Replace with the path to the folder containing your JSON files
folder_path = r'C:\json'
try:
    registry_changes, ransomware_registry_changes = analyse_json_files(folder_path)

    # Display the most frequent registry modifications
    print("Top registry modifications:")
    for change, count in registry_changes.most_common(10):
        print(f"{change}: {count}")

    # Create a DataFrame for the top modifications
    top_changes = registry_changes.most_common(10)
    df_top_changes = pd.DataFrame(top_changes, columns=['Registry Modification', 'Frequency'])

    # Display the table of registry modifications
    print(df_top_changes)

    # Statistics and graphs
    # Number of registry changes for each ransomware
    plt.figure(figsize=(14, 10))
    plt.bar(ransomware_registry_changes.keys(), ransomware_registry_changes.values())
    plt.xlabel('Ransomware', fontsize=12)
    plt.ylabel('Number of Registry Modifications', fontsize=12)
    plt.xticks(rotation=90, fontsize=10)
    plt.title('Number of Registry Changes by Ransomware', fontsize=14)
    plt.grid(True)
    plt.tight_layout(pad=3.0)
    plt.subplots_adjust(bottom=0.4)  # Adjust bottom margin to fit x labels
    plt.show()

    # Top registry modifications using a horizontal bar chart
    changes, counts = zip(*top_changes)
    plt.figure(figsize=(14, 10))
    plt.barh(changes, counts, color='skyblue', edgecolor='black')
    plt.ylabel('Registry Modification', fontsize=12)
    plt.xlabel('Frequency', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.title('Top Registry Modifications', fontsize=14)
    plt.grid(axis='x', linestyle='--', linewidth=0.7)
    plt.tight_layout(pad=3.0)
    plt.subplots_adjust(left=0.35, right=0.95, top=0.9, bottom=0.1)  # Adjust margins to fit y labels
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")