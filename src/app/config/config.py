from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    test_db_username: str
    test_db_password: str


def get_setting(name: str):
    settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

    return dict(settings)[name]
