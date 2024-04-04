import json


async def insert_gpus(db_conn):
    with open("./build-your-pc/data/jsonl/video-card.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]
            chipset = content["chipset"]
            memory = content["memory"]
            length = content["length"]
            await db_conn.execute(
                "INSERT INTO gpus (name, chipset, memory, length) VALUES (?, ?, ?, ?)",
                (name, chipset, memory, length),
            )


async def insert_psus(db_conn):
    with open("./build-your-pc/data/jsonl/power-supply.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]
            form_factor = content["type"]
            efficiency = content["efficiency"]
            wattage = content["wattage"]
            await db_conn.execute(
                "INSERT INTO psus (name, form_factor, efficiency, wattage) VALUES (?, ?, ?, ?)",
                (name, form_factor, efficiency, wattage),
            )


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
                (name, speed, count, size, latency),
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
                (name, cores, graphics, smt),
            )


async def insert_mobo(db_conn):
    with open("./build-your-pc/data/jsonl/motherboard.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]
            socket = content["socket"]
            form_factor = content["form_factor"]
            max_memory = content["max_memory"]
            memory_slots = content["memory_slots"]
            await db_conn.execute(
                "INSERT INTO motherboards (name, socket, form_factor, max_memory, memory_slots) VALUES (?, ?, ?, ?, ?)",
                (name, socket, form_factor, max_memory, memory_slots),
            )


async def insert_cases(db_conn):
    with open("./build-your-pc/data/jsonl/case.jsonl", "r") as f:
        for i in f.readlines():
            content = json.loads(i)
            name = content["name"]
            type = content["type"]
            await db_conn.execute(
                "INSERT INTO cases (name, type) VALUES (?, ?)", (name, type)
            )


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
    await db_conn.execute(
        """
        CREATE TABLE motherboards (
            name TEXT NOT NULL,
            socket INT NOT NULL,
            form_factor INT NOT NULL,
            max_memory INT NOT NULL,
            memory_slots INT NOT NULL,
            FOREIGN  KEY (name) REFERENCES component(name)
        )
        """
    )
    await db_conn.execute(
        """
        CREATE TABLE gpus (
            name TEXT NOT NULL,
            chipset INT NOT NULL,
            memory INT NOT NULL,
            length INT, -- For some reason this isn't always provided. Rude.
            FOREIGN  KEY (name) REFERENCES component(name)
        )
        """
    )
    await db_conn.execute(
        """
        CREATE TABLE psus (
            name TEXT NOT NULL,
            form_factor TEXT NOT NULL,
            efficiency INT, -- presumably NULL here means it has no eff rating.
            wattage INT NOT NULL,
            FOREIGN  KEY (name) REFERENCES component(name)
        )
        """
    )
    await insert_cases(db_conn)
    await insert_cpu(db_conn)
    await insert_memory(db_conn)
    await insert_mobo(db_conn)
    await insert_gpus(db_conn)
    await insert_psus(db_conn)

    await db_conn.commit()
