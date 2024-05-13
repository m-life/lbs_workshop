from typing import Optional
from dotenv import load_dotenv
from functools import lru_cache
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """
    This class provides general settings into the app.
    The following properties default values will be overwritten if envs are set
    """

    # General app Info
    app_title: str = 'LBS'

    # AWS connections
    aws_access_key_id: str = '<KEY>'
    aws_secret_access_key: SecretStr = '<KEY>'

    # Database connection
    # db_host: str
    # db_port: int
    # postgres_db: str
    # postgres_user: str
    # postgres_password: SecretStr
    db_pool_size: Optional[int] = None
    db_max_connections: int = 80
    web_concurrency: int = 1

    def __init__(self, **data):
        super().__init__(**data)
        # set the db pool size if not set
        if not self.db_pool_size:
            self.db_pool_size = max(1, self.db_max_connections // self.web_concurrency)

    def get_db_connection_string(self):
        _postgres_password = self.postgres_password.get_secret_value()
        _credentials = f"{self.postgres_user}:{_postgres_password}"
        return f"postgresql://{_credentials}@{self.db_host}:{self.db_port}/{self.postgres_db}"

    def __getattr__(self, name):
        """Handle accessing capitalized attributes,
        returning the lower case version if the former is not available
        this offers a migration paths from apps that use all caps settings
        variables, in every case the env variable is still the same
        """
        # Check if the attribute has capitalized version
        if name in self.__dict__:
            return self.__dict__[name]
        # Check if the attribute has lower case version
        if name.isupper() and name.lower() in self.__dict__:
            return self.__dict__[name.lower()]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


@lru_cache()
def get_settings():
    load_dotenv('dev.env')
    return Settings()
