import requests
import json
import logging
from config.settings import settings
from requests.exceptions import HTTPError,RequestException
from typing import List,Dict,Any

logger = logging.getLogger(__name__)


class LumuAPIClient:
    """
    Manages interaction with the Lumu Custom Collector API for sending DNS queries data.
    Uses batch processing with configurable retry logic for robustness.
    """

    def __init__(self,
                 api_url: str = f"https://api.lumu.io/v1/collectors/{settings.collector_id}/dns/queries",
                 batch_size: int = settings.batch_size):
        self.api_url = api_url
        self.batch_size = batch_size

    def send_data_in_batches(self,data: str,max_retries: int = 3) -> None:
        """
        Sends DNS query data to the Lumu API in batches with retry logic.

        Args:
            data (str): JSON string of DNS queries to be sent.
            max_retries (int): Maximum retry attempts per batch if a request fails.
        """
        json_data = json.loads(data)
        total_records = len(json_data)

        for start in range(0,total_records,self.batch_size):
            batch = json_data[start:start + self.batch_size]
            for attempt in range(max_retries):
                try:
                    response = self._send_batch(batch)
                    if response.status_code == 200:
                        print(
                            f"Batch sent. Response: {{'status_code': {response.status_code}, 'reason': '{response.reason}', 'json': {response.json()}}}")
                        break
                    else:
                        print(
                            f"Batch sent. Response: {{'status_code': {response.status_code}, 'reason': '{response.reason}', 'json': None}}")
                except (HTTPError,RequestException) as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    raise ValueError(
                        "Failed to send batch after multiple attempts")

    def _send_batch(self,batch: List[Dict[str,Any]]) -> requests.Response:
        """
        Sends a single batch of data to the API. Raises HTTPError if unsuccessful.
        """
        headers = {"Content-Type":"application/json",
                   "Authorization":f"Bearer {settings.lumu_client_key}"}

        response = requests.post(self.api_url,headers=headers,json=batch)
        response.raise_for_status()
        return response
