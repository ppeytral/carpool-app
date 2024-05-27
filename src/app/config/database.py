from config.config import get_setting
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

name = get_setting("test_db_username")
password = get_setting("test_db_password")

engine = create_engine(
    f"postgresql://{name}:{password}@localhost/carpool",
    echo=True,
    client_encoding="utf8",
)


def get_session():
    return Session(engine)
