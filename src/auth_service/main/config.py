from dataclasses import dataclass
from datetime import timedelta
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class JWTConfig:
    private_key: str
    public_key: str
    algorithm: str
    access_token_expire_minutes: timedelta


@dataclass(frozen=True)
class Config:
    jwt: JWTConfig


def create_config() -> Config:
    base_path: Path = Path.cwd().parent.parent

    private_key_path = getenv("PRIVATE_KEY_PATH")
    public_key_path = getenv("PUBLIC_KEY_PATH")
    algorithm = getenv("ALGORITHM")
    access_token_expire_minutes_str = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    if (
        not private_key_path
        or not public_key_path
        or not algorithm
        or not access_token_expire_minutes_str
    ):
        raise ValueError("Environment variables not loaded or missing.")

    try:
        access_token_expire_minutes = int(access_token_expire_minutes_str)
    except ValueError:
        raise ValueError(
            "ACCESS_TOKEN_EXPIRE_MINUTES must be an integer."
        ) from None

    return Config(
        jwt=JWTConfig(
            private_key=base_path.joinpath(private_key_path).read_text(),
            public_key=base_path.joinpath(public_key_path).read_text(),
            algorithm=algorithm,
            access_token_expire_minutes=timedelta(
                minutes=access_token_expire_minutes
            ),
        )
    )
