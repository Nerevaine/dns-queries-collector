import re
import pandas as pd

LOG_PATTERN = (
    r"(?P<date>\d+-\w+-\d+) (?P<time>\d+:\d+:\d+\.\d+) queries: info: client @(?P<client>[\da-fx]+) "
    r"(?P<client_ip>[\d.]+)#(?P<port>\d+) \((?P<host_queried>\S+)\): query: \S+ (?P<query_class>\S+)"
)
"""
Regular expression pattern to parse DNS log entries, capturing relevant fields 
like date, time, client IP, queried host, etc.
"""

def extract_data(log_entry: str) -> dict:
    """
    Extracts fields from a single DNS log entry.

    Args:
        log_entry (str): A single DNS log line.

    Returns:
        dict: Extracted fields as a dictionary if the entry matches the pattern, otherwise an empty dictionary.
    """
    match = re.search(LOG_PATTERN, log_entry)
    return match.groupdict() if match else {}

def create_dataframe(file_path: str) -> pd.DataFrame:
    """
    Parses a log file and creates a DataFrame with structured DNS log data.

    Args:
        file_path (str): Path to the DNS log file.

    Returns:
        pd.DataFrame: DataFrame with each row as a parsed log entry and columns for extracted fields.
    """
    df = pd.read_csv(file_path, header=None, names=["log_entry"])
    df = pd.concat([df["log_entry"].apply(extract_data).apply(pd.Series)], axis=1)
    return df