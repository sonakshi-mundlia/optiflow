import asyncio

from .db import (
    engine,
    Base
)

from .models.query_model import QueryLog


async def init_db():

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )


if __name__ == "__main__":

    asyncio.run(
        init_db()
    )