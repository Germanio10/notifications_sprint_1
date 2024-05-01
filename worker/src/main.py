import asyncio
import contextlib

from connection.conn import connection
from core.config import settings


async def main() -> None:
    db, broker = await connection()

    try:
        await asyncio.Future()
    finally:
        await db.close()
        await broker.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
