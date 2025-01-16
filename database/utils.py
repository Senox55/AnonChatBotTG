import asyncpg


async def get_pg_pool(
        db_name: str,
        host: str,
        port: int,
        user: str,
        password: str,

) -> asyncpg.pool:
    db_pool = await asyncpg.create_pool(
        database=db_name,
        host=host,
        port=port,
        user=user,
        password=password,
        min_size=1,
        max_size=3,
    )

    return db_pool
