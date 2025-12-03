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
    database_engine: str = "sqlite:///airport_db.db"

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", frozen=True)


class AerospaceConfig(BaseSettings):
    """Settings and requriements for aerospace"""

    X_BOUNDARY: int = 10000
    Y_BOUNDARY: int = 10000
    MAX_ALTITUDE: int = 5000


class PlanesConfig(BaseSettings):
    """Setting for types of planes"""

    FUEL_CONSUMPTION_DEFAULT: int = 10


class TestsConfig(BaseSettings):
    """Setting for testing"""

    DB_ENGINE: str = "sqlite:///test_db.db"


class AppConfig(BaseSettings):
    """Managing all configs together"""

    model_config = SettingsConfigDict(
        frozen=True, env_file=".env", env_file_encoding="utf-8"
    )

    network: NetworkConfig = Field(default_factory=NetworkConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    aerospace: AerospaceConfig = Field(default_factory=AerospaceConfig)
    planes: PlanesConfig = Field(default_factory=PlanesConfig)
    tests: TestsConfig = Field(default_factory=TestsConfig)


config = AppConfig()
