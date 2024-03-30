async def run(db_conn):
    await db_conn.execute(
        """
        CREATE TABLE users (
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL,
            email TEXT NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
        """
    )
    await db_conn.commit()
