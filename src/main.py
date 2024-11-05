import logging
import pandas as pd
from log_parser import create_dataframe
from stats import print_statistics
from lumu_api_client import LumuAPIClient
from utils.logger_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def main(file_path: str = "data/queries") -> None:
    """
    Processes the DNS log file, generates statistics, and sends data to the Lumu API.

    Args:
        file_path (str): Path to the DNS log file. Defaults to "data/queries".
    """
    logger.info("Starting DNS Queries Collector")

    df = create_dataframe(file_path)
    if df.empty:
        logger.error("No records found in the log file.")
        return

    print_statistics(df)

    print("\nSend data in batches\n" + "-" * 26)

    lumu_client = LumuAPIClient()
    json_data = df.to_json(orient="records")
    lumu_client.send_data_in_batches(json_data)

    logger.info("Data successfully sent to the Lumu API.")

if __name__ == "__main__":
    main()