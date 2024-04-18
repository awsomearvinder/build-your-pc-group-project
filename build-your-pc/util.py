from aiosqlite import Connection, Error, IntegrityError, connect
import aiosqlite
from argon2 import PasswordHasher

from pathlib import Path
from tomllib import load
from dataclasses import dataclass
import uuid
import time
from typing import Literal

from migrations import migrate


@dataclass
class User:
    username: str
    id: int


class UserAlreadyExists(Error):
    def __init__(self):
        pass


class WrongUsernameOrPassword(Error):
    def __init__(self):
        pass


class InvalidComponentType(Error):
    def __init__(self):
        pass


@dataclass
class Token:
    token: uuid.UUID


class Config:
    _db_conn: Connection
    _hasher: PasswordHasher
    app_secret: str
    debug_mode: bool

    def __init__(self, path: Path):
        """
        NOTE: You *must* call `init` after initializing the class
        in order to finish the startup.
        """
        with open(path, "rb") as f:
            config_raw = load(f)
            self.debug_mode = bool(config_raw["debug_mode"])
            self._db_conn = connect(config_raw["db_path"])
            self.app_secret = config_raw["app_secret"]

        self.expiration_time = int(config_raw.get("expiration_time") or 3600)

        self._hasher = PasswordHasher()

    async def init(self):
        await self._db_conn
        await self._db_conn.execute("ATTACH 'components.db' AS pc")
        self._db_conn.row_factory = aiosqlite.Row
        await migrate(self._db_conn)

    async def _generate_token(self, username: str) -> Token:
        id = uuid.uuid4()
        token = await self._db_conn.execute(
            "INSERT INTO tokens (username, token, expiration) VALUES (?, ?, ?)",
            (username, str(id), int(time.time()) + self.expiration_time),
        )
        token = await token.fetchone()
        await self._db_conn.commit()

        return Token(id)

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

        token = await self._generate_token(username)

        # The user *should* be generated at this point.
        if user_id == None:
            raise TypeError()

        await self._db_conn.commit()

        return (User(username, user_id[0]), token)

    async def login_user(self, username: str, password: str) -> tuple[User, Token]:
        user = await self._db_conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        user = await user.fetchone()
        if user == None:
            raise WrongUsernameOrPassword()  # We do not let *anyone* know whether a user exists or not
            # via login attempts.

        if not self._hasher.verify(user["hash"], password):
            raise WrongUsernameOrPassword()

        # set a new hash if we updated our password config.
        if self._hasher.check_needs_rehash(user["hash"]):
            hash = self._hasher.hash(password)
            await self._db_conn.execute(
                "UPDATE users SET hash = ? WHERE username  = ?", (hash, username)
            )
            await self._db_conn.commit()

        user = User(user["username"], user["id"])
        token = await self._generate_token(username)
        return (user, token)

    async def get_components(
        self, kind: Literal["cpu", "gpu", "psu", "memory", "chassis", "motherboard"]
    ):
        if kind not in [
            "cpu",
            "memory",
            "gpu",
            "case",
            "motherboard",
            "psu",
        ]:
            raise InvalidComponentType()
        results = await self._db_conn.execute(f"SELECT * FROM pc.{kind}")
        return [dict(item) for item in await results.fetchall()]
