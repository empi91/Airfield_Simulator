from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class NetworkConfig(BaseSettings):
    """Config for socket conections between server and planes"""

    host: str = "127.0.0.1"
    port: int = 65432
    buffer_size: int = 1024
    max_connections: int = 100
    connection_timeout: int = 30


class DatabaseConfig(BaseSettings):
    """Config for database connections"""
    db_name: str = ""
    # db_user: str
    # db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    database_url: str = ""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        frozen=True
    )


class AppConfig(BaseSettings):
    """Managing all configs together"""

    model_config = SettingsConfigDict(
        frozen=True,
        env_file=".env",
        env_file_encoding="utf-8"
    )

    network: NetworkConfig = Field(default_factory=NetworkConfig)
    # database: DatabaseConfig = Field(default_factory=DatabaseConfig)



config = AppConfig()