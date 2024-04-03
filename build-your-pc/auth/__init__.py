from util import Config, Token, User


async def register(
    cfg: Config, username: str, password: str, email: str
) -> tuple[User, Token]:
    return await cfg.add_user(username, password, email)
