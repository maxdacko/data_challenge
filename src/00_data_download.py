import pandas as pd
import requests
import os
import json

# URLs from the Gist provided in the PDF! (i just copied the URLs from the raw elements in the Gist)
DATASETS = {
    "allowance_events": "https://gist.githubusercontent.com/DaniModak/d0cdc441bc2cab2abdc5b37e45ca5cb4/raw/13ded757082f09740a0ca351f926b74c336206ab/allowance_events",
    "allowance_backend_table": "https://gist.githubusercontent.com/DaniModak/d0cdc441bc2cab2abdc5b37e45ca5cb4/raw/13ded757082f09740a0ca351f926b74c336206ab/allowance_backend_table",
    "payment_schedule_backend_table": "https://gist.githubusercontent.com/DaniModak/d0cdc441bc2cab2abdc5b37e45ca5cb4/raw/13ded757082f09740a0ca351f926b74c336206ab/payment_schedule_backend_table",
}

def download_file(url, dest_path):
    """
    Function expected to download the files from a URL if it doesn't already exist locally.
    Args:
        url (str): The URL to download the file from.
        dest_path (str): The path to save the downloaded file.
    """
    if not os.path.exists(dest_path):
        print(f"Downloading {url} to {dest_path}...")
        response = requests.get(url)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {dest_path}.")
    else:
        print(f"{dest_path} already exists. Skipping download!")

def load_allowance_events(file_path):
    """
    Load and process the allowance_events dataset, with this being a JSON file.
    Args:
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.json_normalize(data)

def load_allowance_backend(file_path):
    """
    Load and process the allowance_backend_table dataset, this time being a CSV.
    Args:
        file_path (str): The path to the CSV file.
    """
    return pd.read_csv(file_path)

def load_payment_schedule(file_path):
    """
    Load and process the payment_schedule_backend_table dataset, again, a CSV file.
    Args:
        file_path (str): The path to the CSV file.
    """
    return pd.read_csv(file_path)

def prepare_datasets(data_dir):
    """Download datasets and load them as dataframes."""
    os.makedirs("data/input", exist_ok=True)  # check if the directory exists, if not, create it
    
    for name, url in DATASETS.items():
        dest_path = os.path.join(data_dir, f"{name}.{'json' if 'allowance_events' in url else 'csv'}") # if it's the allowance_events dataset, it's a JSON file, otherwise, it's a CSV file
        download_file(url, dest_path) # download the file using the function above

    # create the dataframes from the downloaded files
    allowance_events = load_allowance_events(os.path.join(data_dir, "allowance_events.json"))
    allowance_backend = load_allowance_backend(os.path.join(data_dir, "allowance_backend_table.csv"))
    payment_schedule = load_payment_schedule(os.path.join(data_dir, "payment_schedule_backend_table.csv"))

    return allowance_events, allowance_backend, payment_schedule

# this is the main function that will be called when running the script
if __name__ == "__main__":
    """
    Main execution flow:
    - Saves datasets url
    - Downloads datasets
    - Saves the JSON and CSV files
    """
    data_dir = "data/input"
    events, backend, schedule = prepare_datasets(data_dir)

