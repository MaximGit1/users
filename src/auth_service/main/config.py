from dataclasses import dataclass
from datetime import timedelta
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

BASE_PATH = Path.cwd().parent.parent

if BASE_PATH is None:
    raise ValueError("BASE_PATH must not be None")

load_dotenv()


@dataclass
class JWTSettings:
    private_key: str
    public_key: str
    algorithm: str
    access_token_expire_minutes: timedelta


def create_jwt_env() -> JWTSettings:
    private_key_path_env = getenv("PRIVATE_KEY_PATH")
    public_key_path_env = getenv("PUBLIC_KEY_PATH")

    if not private_key_path_env or not public_key_path_env:
        raise ValueError(
            "Both PRIVATE_KEY_PATH and PUBLIC_KEY_PATH must not be None"
        )

    private_key_path = BASE_PATH.joinpath(private_key_path_env)
    public_key_path = BASE_PATH.joinpath(public_key_path_env)


    expire_variable = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    if expire_variable is not None:
        access_token_expire_minutes = int(expire_variable)
    else:
        raise ValueError("expire_variable must not be None")

    algorith = getenv("ALGORITHM")

    if algorith is None:
        raise ValueError("ALGORITHM must not be None")



    return JWTSettings(
        algorithm=algorith,
        private_key=Path(private_key_path).read_text(),
        public_key=Path(public_key_path).read_text(),
        access_token_expire_minutes=timedelta(
            minutes=access_token_expire_minutes
        ),
    )


jwt_settings = create_jwt_env()

__all__ = ("jwt_settings",)
