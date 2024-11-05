import json
import pytest
from unittest.mock import patch, Mock
from src.lumu_api_client import LumuAPIClient


@pytest.fixture
def sample_data():
    return json.dumps([
        {"client_ip": "192.168.0.1", "name": "example.com", "timestamp": "2024-11-05T17:33:53.945Z"},
        {"client_ip": "192.168.0.2", "name": "test.com", "timestamp": "2024"
                                                                      "-11-05T17:35:53.945Z"}
    ])

@patch("src.lumu_api_client.requests.post")
def test_send_data_in_batches_success(mock_post, sample_data):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_post.return_value = mock_response

    client = LumuAPIClient(batch_size=1)
    client.send_data_in_batches(sample_data)
    assert mock_post.call_count == 2

