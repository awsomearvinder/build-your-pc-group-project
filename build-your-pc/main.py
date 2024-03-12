from quart import Quart, render_template, websocket, send_from_directory

app = Quart(__name__, static_folder = None, static_url_path = None)

@app.route("/")
async def hello():
    return await render_template("index.html")

@app.route("/store/<path:path>")
async def store(path):
    return await send_from_directory('store', path)

@app.route("/static/<path:path>")
async def static(path):
    return await send_from_directory('static', path)

if __name__ == "__main__":
    app.run()
