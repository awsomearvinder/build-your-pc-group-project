from pathlib import Path
import os

from quart import Quart, render_template, send_from_directory, request

import util

app = Quart(__name__, static_folder=None, static_url_path=None)

# Look in BYPC_CONFIG envvar first, otherwise load config.toml
cfg = util.Config(Path(os.getenv("BYPC_CONFIG") or "config.toml"))

@app.route("/")
async def hello():
    return await render_template("index.html")


@app.route("/store/<path:path>")
async def store(path):
    return await send_from_directory("store", path)


@app.route("/static/<path:path>")
async def static(path):
    return await send_from_directory("static", path)


if __name__ == "__main__":
    app.run()
