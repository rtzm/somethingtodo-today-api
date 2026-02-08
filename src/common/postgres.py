import asyncpg

# TODO: update to pull from env vars
DATABASE_URL = "postgresql://admin:secret@localhost:5432/somethingtodo-today"

class Postgres:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def disconnect(self):
        await self.pool.close()

database = Postgres(DATABASE_URL)