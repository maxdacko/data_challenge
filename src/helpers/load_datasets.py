import pandas as pd
import json

def load_datasets(data_dir="data/input"):
    """
    This funciton loads the three datasets downloaded in the step before
    Args:
        data_dir (str): Path to the directory containing the input files.
    Returns:
        allowance_events (DataFrame): Normalized event data from the JSON file.
        allowance_backend (DataFrame): Backend table data.
        payment_schedule (DataFrame): Payment schedule data.
    """
    with open(f"{data_dir}/allowance_events.json", 'r') as f:
        allowance_events_data = json.load(f)
    allowance_events = pd.json_normalize(allowance_events_data)
    allowance_backend = pd.read_csv(f"{data_dir}/allowance_backend_table.csv")
    payment_schedule = pd.read_csv(f"{data_dir}/payment_schedule_backend_table.csv")
    return allowance_events, allowance_backend, payment_schedule