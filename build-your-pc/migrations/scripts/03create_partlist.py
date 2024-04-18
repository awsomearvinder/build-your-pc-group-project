async def run(db_conn):
    await db_conn.execute(
        """
        CREATE TABLE part_list (
            id INTEGER PRIMARY KEY,
            components_name TEXT ,
            users_id INTEGER,
            FOREIGN KEY (components_name) REFERENCES component (name),
            FOREIGN KEY (users_id) REFERENCES users (id)
        )
        """
    )
    await db_conn.execute(
        """
        ALTER TABLE component
        ADD COLUMN kind TEXT NOT NULL
        """
    )
    for i in ["cpu", "case", "motherboard", "gpu", "psu"]:
        await db_conn.execute(
            f"""
            UPDATE component
            SET kind = '{i}'
            WHERE name = (SELECT name FROM {i}s)
            """
        )
    await db_conn.execute(
        """
        UPDATE component
        SET kind = 'memory'
        WHERE name in (SELECT name FROM memory)
        """
    )

    await db_conn.commit()
