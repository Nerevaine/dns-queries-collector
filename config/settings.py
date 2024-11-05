import os
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    """
    Settings for configuring the DNS Queries Collector.
    Loads environment variables and provides default values where necessary.
    """

    lumu_client_key: str = os.getenv("LUMU_CLIENT_KEY")
    collector_id: str = os.getenv("COLLECTOR_ID")
    batch_size: int = int(os.getenv("BATCH_SIZE",500))
    log_level: str = os.getenv("LOG_LEVEL","INFO")
    log_file: str = os.getenv("LOG_FILE","app.log")

    @property
    def api_url(self) -> str:
        """
        Dynamically constructs the API URL using collector_id and lumu_client_key.
        """
        return (f"https://api.lumu.io/v1/collectors/{self.collector_id}/dns"
                f"/queries?key={self.lumu_client_key}")

    class Config:
        env_file = ".env"


settings = Settings()