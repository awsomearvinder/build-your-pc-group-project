import json

async def insert_memory(db_conn):
    with open("./build-your-pc/data/jsonl/memory.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]

            # the schema isn't consistent here, ugh.
            try:
                speed = content["speed"][1]
            except:
                speed = content["speed"]
            count = content["modules"][0]
            size = content["modules"][1]
            latency = content["cas_latency"]
            await db_conn.execute(
                "INSERT INTO memory (name, speed, count, size, latency) VALUES (?, ?, ?, ?, ?)",
                (name, speed, count, size, latency)
            )

async def insert_cpu(db_conn):
    with open("./build-your-pc/data/jsonl/cpu.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]
            cores = content["core_count"]
            smt = content["smt"]
            graphics = content["graphics"]
            await db_conn.execute(
                "INSERT INTO cpus (name, core_count, graphics, smt) VALUES (?, ?, ?, ?)",
                (name, cores, graphics, smt)
            )
async def insert_cases(db_conn):
    with open("./build-your-pc/data/jsonl/case.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]
            type = content["type"]
            await db_conn.execute("INSERT INTO cases (name, type) VALUES (?, ?)", (name, type))

async def run(db_conn):
    await db_conn.execute(
        """
        CREATE TABLE component (
            name TEXT NOT NULL PRIMARY KEY
        );
        """
    )
    await db_conn.execute(
        """
        CREATE TABLE cases (
            name TEXT NOT NULL,
            type TEXT NUT NULL,
            FOREIGN  KEY (name) REFERENCES component(name)
        );
        """
    )
    await db_conn.execute(
        """
        CREATE TABLE cpus (
            name TEXT NOT NULL,
            core_count INT NOT NULL,
            graphics TEXT,
            smt BOOLEAN,
            FOREIGN  KEY (name) REFERENCES component(name)
        )
        """
    )
    await db_conn.execute(
        """
        CREATE TABLE memory (
            name TEXT NOT NULL,
            size INT NOT NULL,
            count INT NOT NULL,
            speed INT NOT NULL,
            latency INT NOT NULL,
            FOREIGN  KEY (name) REFERENCES component(name)
        )
        """
    )
    await insert_cases(db_conn)
    await insert_cpu(db_conn)
    await insert_memory(db_conn)

    await db_conn.commit()
