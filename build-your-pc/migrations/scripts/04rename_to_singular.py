import re


async def run(db_conn):
    await db_conn.execute(
        """
        ATTACH DATABASE 'components.db' as pc
        """
    )
    await db_conn.commit()
    for i in ["cpus", "cases", "motherboards", "gpus", "psus", "memory"]:
        create_tbl_stmt_preprocessed = await db_conn.execute(
            """
            SELECT sql FROM sqlite_master WHERE type='table' AND name=?
            """,
            (i,),
        )

        _new_table_name = r"\1\2" if i != "cases" else "chassis"

        create_tbl_stmt = re.sub(
            r"CREATE TABLE (?:(\S*)s|(memory)) \(",
            f"CREATE TABLE pc.{_new_table_name} (",
            (await create_tbl_stmt_preprocessed.fetchone())[0],
        )

        await db_conn.execute(
            # make it singular if you can, and recreate the table that was in the main db until now.
            create_tbl_stmt
        )
        await db_conn.execute(
            f"""
            INSERT INTO pc.{ i if i == "memory" else
                             "chassis" if i == "cases" 
                             else i[:-1] } SELECT * FROM {i}
            """
        )

        await db_conn.execute(
            f"""
            DROP TABLE {i}
            """
        )
    await db_conn.commit()
