from pathlib import Path
import os

from quart import Quart, render_template, send_from_directory, request
from jsonschema import ValidationError, validate
from typing import Tuple, Dict

import auth
import util

app = Quart(__name__, static_folder=None, static_url_path=None)

# Look in BYPC_CONFIG envvar first, otherwise load config.toml
cfg = util.Config(Path(os.getenv("BYPC_CONFIG") or "config.toml"))


@app.before_serving
async def init():
    await cfg.init()


@app.route("/")
async def hello():
    return await render_template("index.html")


@app.route("/store/<path:path>")
async def store(path):
    return await send_from_directory("store", path)


REGISTER_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["username", "password", "email"],
}


@app.route("/register", methods=["POST"])
async def register() -> Tuple[Dict[str, str], int]:
    content = await request.json
    try:
        validate(content, REGISTER_SCHEMA)
    except ValidationError as e:
        return (
            {
                "cause": e.message,
                "error": e.__class__.__name__,
            },
            400,
        )

    try:
        await auth.register(
            cfg, content["username"], content["password"], content["email"]
        )
    except util.UserAlreadyExists as e:
        return (
            {
                "cause": f"User {content['username']} already exists",
                "error": e.__class__.__name__,
            },
            400,
        )
    return ({}, 200)


@app.route("/static/<path:path>")
async def static(path):
    return await send_from_directory("static", path)


if __name__ == "__main__":
    app.run()
