from pathlib import Path
import os

from quart import Quart, render_template, send_from_directory, request, session, redirect, Response
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
    app.secret_key = cfg.app_secret
    app.debug = cfg.debug_mode


@app.route("/")
async def hello():
    return await render_template("index.html")

@app.route("/auth")
async def openLogin():
    return await render_template('auth.html')

@app.route("/registration")
async def openRegister():
    return await render_template('register.html')

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
        _, token = await auth.register(
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
    
    session['token'] = token.token.hex
    return ({"token": token.token.hex}, 200)


LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
}

@app.route("/logout", methods=["GET"])
async def logout() -> Response:
    try:
        session.pop("token")
    except:
        pass
    resp = redirect("/")
    return resp

@app.route("/login", methods=["POST"])
async def login() -> Tuple[Dict[str, str], int]:
    content = await request.json
    try:
        validate(content, LOGIN_SCHEMA)
    except ValidationError as e:
        return (
            {
                "cause": e.message,
                "error": e.__class__.__name__,
            },
            400,
        )

    try:
        _, token = await auth.login(
            cfg,
            content["username"],
            content["password"],
        )
    except util.WrongUsernameOrPassword as e:
        return (
            {
                "cause": f"Wrong Username or Password!",
                "error": e.__class__.__name__,
            },
            401,
        )


    session['token'] = token.token.hex
    return ({"token": token.token.hex}, 200)


@app.route("/static/<path:path>")
async def static(path):
    return await send_from_directory("static", path)


@app.route("/components/<kind>")
async def get_components(kind: str):
    try:
        print(kind.strip())
        # NOTE: This would normally be unsafe, but since we validate
        # component above it's fine to directly concatenate the component
        # into the SQL string.
        return await cfg.get_components(kind.strip())
    except util.InvalidComponentType as e:
        return (
            {
                "cause": f"Invalid pc component type given.",
                "error": e.__class__.__name__,
            },
            404,
        )


if __name__ == "__main__":
    app.run()
