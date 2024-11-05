import pandas as pd
from src.stats import print_statistics

def test_print_statistics(capsys):
    """
    Tests the print_statistics function by capturing its output and comparing it to expected values
    without depending on exact spacing or alignment.
    """
    data = {
        "client_ip": ["192.168.0.1", "192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.1"],
        "host_queried": ["example.com", "example.com", "test.com", "example.com", "test.com"]
    }
    df = pd.DataFrame(data)

    print_statistics(df)
    captured = capsys.readouterr().out

    # Eliminate extra spaces for flexible matching
    captured_normalized = " ".join(captured.split())

    assert "Total Records: 5" in captured_normalized
    assert "192.168.0.1 3 60.00%" in captured_normalized
    assert "192.168.0.2 1 20.00%" in captured_normalized
    assert "192.168.0.3 1 20.00%" in captured_normalized
    assert "example.com 3 60.00%" in captured_normalized
    assert "test.com 2 40.00%" in captured_normalized