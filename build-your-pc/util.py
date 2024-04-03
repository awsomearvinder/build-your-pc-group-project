from aiosqlite import Connection, Error, IntegrityError, connect
from argon2 import PasswordHasher

from pathlib import Path
from tomllib import load
from dataclasses import dataclass
import uuid
import time

from migrations import migrate


@dataclass
class User:
    username: str
    id: int


class UserAlreadyExists(Error):
    def __init__(self):
        pass


@dataclass
class Token:
    token: uuid.UUID


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

        self.expiration_time = int(config_raw.get("expiration_time") or 3600)

        self._hasher = PasswordHasher()

    async def init(self):
        await self._db_conn
        await migrate(self._db_conn)

    async def add_user(
        self, username: str, password: str, email: str
    ) -> tuple[User, Token]:
        hash = self._hasher.hash(password)
        try:
            user_id = await self._db_conn.execute(
                "INSERT INTO users (username, hash, email) VALUES (?, ?, ?) RETURNING id",
                (username, hash, email),
            )
            user_id = await user_id.fetchone()

        except IntegrityError:
            raise UserAlreadyExists()

        id = uuid.uuid4()
        token = await self._db_conn.execute(
            "INSERT INTO tokens (username, token, expiration) VALUES (?, ?, ?)",
            (username, str(id), int(time.time()) + self.expiration_time),
        )
        token = await token.fetchone()
        # The user *should* be generated at this point.
        if user_id == None:
            raise TypeError()

        await self._db_conn.commit()

        return (User(username, user_id[0]), Token(id))
