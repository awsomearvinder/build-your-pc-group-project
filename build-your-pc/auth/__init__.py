from util import Config


async def register(cfg: Config, username: str, password: str, email: str):
    user = await cfg.add_user(username, password, email)
    print(user)
