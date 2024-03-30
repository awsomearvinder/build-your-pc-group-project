from types import NoneType
from aiosqlite import Connection, Error, IntegrityError, connect
from argon2 import PasswordHasher

from pathlib import Path
from tomllib import load
from dataclasses import dataclass

from migrations import migrate


@dataclass
class User:
    username: str
    id: int


class UserAlreadyExists(Error):
    def __init__(self):
        pass


class Config:
    _db_conn: Connection
    _hasher: PasswordHasher

    def __init__(self, path: Path):
        """
        NOTE: You *must* call `init` after initializing the class
        in order to finish the startup.
        """
        with open(path, "rb") as f:
            config_raw = load(f)
            self._db_conn = connect(config_raw["db_path"])

        self._hasher = PasswordHasher()

    async def init(self):
        await self._db_conn
        await migrate(self._db_conn)

    async def add_user(self, username: str, password: str, email: str) -> User:
        hash = self._hasher.hash(password)
        try:
            result = await self._db_conn.execute(
                "INSERT INTO users (username, hash, email) VALUES (?, ?, ?) RETURNING id",
                (username, hash, email),
            )
        except IntegrityError:
            raise UserAlreadyExists()
        result = await result.fetchone()

        # The above should never fail.
        if result == None:
            raise TypeError()

        await self._db_conn.commit()

        return User(username, result[0])
