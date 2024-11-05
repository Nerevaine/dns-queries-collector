from io import StringIO
from src.log_parser import extract_data, create_dataframe


def test_extract_data_valid_entry():
    """
    Tests extract_data with a valid DNS log entry.
    """
    log_entry = ("18-May-2021 16:34:13.003 queries: info: client "
                 "@0x55adcc672cc0 45.231.61.2#8888 (pizzaseo.com): query: "
                 "pizzaseo.com IN A")
    expected_output = {
        "date": "18-May-2021",
        "time": "16:34:13.003",
        "client": "0x55adcc672cc0",
        "client_ip": "45.231.61.2",
        "port": "8888",
        "host_queried": "pizzaseo.com",
        "query_class": "IN"
    }
    assert extract_data(log_entry) == expected_output


def test_extract_data_invalid_entry():
    """
    Tests extract_data with an invalid DNS log entry to ensure it returns an empty dictionary.
    """
    log_entry = "Invalid log entry format"
    assert extract_data(log_entry) == {}


def test_create_dataframe():
    """
    Tests create_dataframe by loading a small sample log and verifying the resulting DataFrame structure.
    """
    # Mock data to simulate a log file with two valid entries
    mock_log_data = """18-May-2021 16:34:13.003 queries: info: client @0x55adcc672cc0 45.231.61.2#8888 (pizzaseo.com): query: pizzaseo.com IN A
18-May-2021 16:35:14.004 queries: info: client @0x55adccee77d0 192.168.1.1#5353 (example.com): query: example.com IN AAAA
"""

    # Create DataFrame from the mock data
    mock_file = StringIO(mock_log_data)
    df = create_dataframe(mock_file)

    # Define expected columns and verify their presence
    expected_columns = ["date", "time", "client", "client_ip", "port", "host_queried", "query_class"]
    assert list(df.columns) == expected_columns

    # Verify row count and specific values to ensure parsing accuracy
    assert len(df) == 2  # Two rows expected
    assert df.iloc[0]["client_ip"] == "45.231.61.2"
    assert df.iloc[1]["host_queried"] == "example.com"