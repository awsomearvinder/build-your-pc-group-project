from aiosqlite import Connection

from pathlib import Path


async def migrate(conn: Connection) -> None:
    # we create a table for all the migrations
    # we've ran if the table doesn't exist yet. That
    # table contains all the migrations we've ran, and it
    # executes the ones we didn't run.
    await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS migrations (
            migration_name TEXT PRIMARY KEY
        )
        """
    )

    print("RUNNING MIGRATIONS")

    await conn.commit()

    for i in await conn.execute_fetchall("SELECT migration_name FROM migrations"):
        print(i)

    migration_folder = Path(__file__).parent / Path("scripts")
    # note: this *does* actually block the event loop technically
    # but also, this isn't really an issue since the app hasn't
    # really started yet.
    for item in migration_folder.resolve().glob("*"):
        import importlib

        file_name = item.name[: len(item.name) - len(".py")]
        cur = await conn.execute(
            "SELECT * FROM migrations WHERE migration_name = ?", [file_name]
        )
        migration = await cur.fetchone()
        if not (migration is None):
            continue

        if file_name.startswith("__"):
            continue

        print(f"RUNNING MIGRATION: {file_name}")
        module = importlib.import_module(f"migrations.scripts.{file_name}")
        await module.run(conn)
        await conn.execute_insert("INSERT INTO migrations VALUES (?)", [file_name])
        await conn.commit()
