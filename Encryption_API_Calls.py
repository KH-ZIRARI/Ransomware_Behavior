
import json
import os
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Path to the folder containing JSON files
json_folder_path = 'C:\\json\\'

# Encryption-related keywords extended to include specific API names
encryption_keywords = [
    'encrypt', 'crypt', 'aes', 'rsa', 'cipher', '3des', 'blowfish', 'twofish',
    'ecdsa', 'sha256', 'ssl', 'tls', 'cryptlib', 'bcrypt', 'gpg', 'pgp',
    'decrypt', 'signature', 'certificate', 'public key', 'private key',
    'encryption key', 'hashing', 'md5', 'hmac', 'salsa20', 'chacha20',
    'writefile', 'readfile', 'openfile', 'secure delete', 'wipe data',
    'keygen', 'keylogger', 'obfuscate', 'scramble', 'secure storage',
    'ransomnote', 'bitlocker', 'diskcryptor', 'pay decrypt', 'key exchange',
    'data leak', 'file locker', 'password protected', 'digital signature',
    # Specific API calls known for encryption tasks
    'CryptEncrypt', 'CryptDecrypt', 'CryptAcquireContext', 'CryptGenKey',
    'CryptDeriveKey', 'CryptHashData', 'CryptCreateHash', 'CryptExportKey',
    'CryptImportKey', 'WriteFile', 'ReadFile', 'CreateFile', 'DeleteFile',
    'MoveFile', 'SetFileAttributes', 'RegSetValue', 'RegCreateKey',
    'RegDeleteKey', 'VirtualAlloc', 'VirtualProtect', 'WSASend', 'WSARecv',
    'Connect'
]

# Function to load a JSON file
def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while loading {file_path}: {str(e)}")
    return {}

# Function to extract encryption-related activities
def extract_encryption_activities(json_data):
    activities = {'api_calls': Counter(), 'loaded_dlls': Counter()}
    behavior_data = json_data.get('behavior', {})

    # Handle API statistics
    api_stats = behavior_data.get('apistats', {})
    for process, apis in api_stats.items():
        for api, count in apis.items():
            api_lower = api.lower()  # Convert to lowercase once per API call
            if any(keyword in api_lower for keyword in encryption_keywords):
                activities['api_calls'][api] += count

    # Handle DLL imports
    pe_imports = json_data.get('static', {}).get('pe_imports', [])
    for dll_info in pe_imports:
        dll_name = dll_info.get('dll', '').lower()  # Convert to lowercase once per DLL
        if any(keyword in dll_name for keyword in encryption_keywords):
            activities['loaded_dlls'][dll_name] += 1

    return activities

# Analyze all JSON files in the specified folder
def analyze_folder(folder_path):
    all_activities = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            json_data = load_json(file_path)
            activities = extract_encryption_activities(json_data)
            if activities:
                all_activities.append(activities)
    return all_activities

# Analysis of files
encryption_activities = analyze_folder(json_folder_path)

# Prepare data for statistics and graphics
api_calls = Counter()
loaded_dlls = Counter()

for activity in encryption_activities:
    api_calls.update(activity['api_calls'])
    loaded_dlls.update(activity['loaded_dlls'])

# Export API call data to a CSV file
df_api_calls = pd.DataFrame.from_dict(api_calls, orient='index', columns=['Count'])
df_api_calls.to_csv('encryption_api_calls_liste.csv')

# Plotting API calls related to encryption by sample
plt.figure(figsize=(10, 6))
plt.bar(api_calls.keys(), api_calls.values())
plt.xlabel('API Calls')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.title('API Calls Related to Encryption by Sample')
plt.tight_layout()
plt.show()

# Plotting "top API" calls related to encryption
top_apis = api_calls.most_common(5)
top_apis_names = [api[0] for api in top_apis]
top_apis_counts = [api[1] for api in top_apis]

plt.figure(figsize=(10, 6))
plt.bar(top_apis_names, top_apis_counts)
plt.xlabel('API Calls')
plt.ylabel('Count')
plt.title('Top API Calls Related to Encryption')
plt.tight_layout()
plt.show()
