async def run(db_conn):
    await db_conn.execute(
        """
        CREATE TABLE tokens(
            username TEXT NOT NULL UNIQUE,
            token TEXT NOT NULL,
            expiration INT NOT NULL
        )
        """
    )
    await db_conn.commit()
