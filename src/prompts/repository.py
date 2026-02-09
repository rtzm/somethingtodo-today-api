from typing import List, Optional
from src.common.postgres import database
from src.prompts.model import Prompt

async def get_todays_prompt(today: str) -> Optional[Prompt]:
    query = """
    SELECT *
    FROM prompt
    WHERE use_date = $1
"""
    
    async with database.pool.acquire() as connection:
        row = await connection.fetchrow(query, today)
        if row is not None:
            user = Prompt(**row)
            return user
        return None


async def get_prompts() -> List[Prompt]:
    query = """
    SELECT *
    FROM prompt
"""

    async with database.pool.acquire() as connection:
        rows = await connection.fetch(query)
        prompts = [Prompt(**row) for row in rows]
        return [
            *prompts
        ]


async def create_prompt(prompt: Prompt):
    query = f"""
    INSERT INTO
        prompt (text, use_date, created_timestamp, updated_timestamp)
    VALUES
        ($1, null, NOW(), NOW())
"""
    async with database.pool.acquire() as connection:
        await connection.execute(query, prompt.text)

async def edit_prompt(prompt: Prompt):
    query = f"""
    UPDATE
        prompt
    SET
        text = $1,
        use_date = $2
        updated_timestamp = NOW()
    WHERE
        id = $3
"""
    async with database.pool.acquire() as connection:
        await connection.execute(query, prompt.text, prompt.use_date, prompt.id)

