import sqlite3
import uvicorn

from contextlib import asynccontextmanager
from datetime import date
from fastapi import FastAPI
from sqlite3 import Error
from typing import List

from src.prompts.model import Prompt
from src.prompts.repository import Prompt
from src.common.postgres import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


def _create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"ERROR - connection failed: '{e}'")
    
    return connection


# TODO: figure out a different database
connection = _create_connection("./sthtdtoday.sqlite")

def _execute_query(connection, query) -> bool:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"ERROR - query failed: '{e}'")
        return False

    return True


def _execute_read_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"ERROR - query failed: '{e}'")

# TODO: move these into the approach defined here: https://www.reddit.com/r/Python/comments/1eqftsl/fastapi_without_orms_setup_migrations_testing/
# TODO: prevent SQL injection on all of these functions
def get_todays_prompt(connection, today: str) -> Prompt:
    select_prompt_by_date_query = f"""
    SELECT *
    FROM prompts
    WHERE use_date = '{today}'
"""
    
    result = _execute_read_query(connection, select_prompt_by_date_query)
    return Prompt(**result)

def get_prompts(connection) -> List[Prompt]:
    select_prompts_query = """
    SELECT *
    FROM prompts
"""

    results = _execute_read_query(connection, select_prompts_query)
    prompts = [Prompt(**result) for result in results]

    return [
        *prompts
    ]


def create_prompt(connection, prompt: Prompt) -> bool:
    create_prompt_query = f"""
    INSERT INTO
        prompts (text, use_date, created_timestamp, updated_timestamp)
    VALUES
        ({prompt.text}, null, NOW(), NOW())
"""

    return _execute_query(connection, create_prompt_query)


def edit_prompt(connection, prompt: Prompt) -> bool:
    create_prompt_query = f"""
    UPDATE
        prompts
    SET
        text = {prompt.text},
        use_date = {prompt.use_date}
        updated_timestamp = NOW()
    WHERE
        id = {prompt.id}
"""

    return _execute_query(connection, create_prompt_query)


@app.get("/prompt/{today}")
def prompt_show(today: str):
    if today != date.today().isoformat():
        raise ValueError(f"Unable to fetch for that day")

    prompt = get_todays_prompt(connection, today)
    return prompt.model_dump()


# TODO: add auth for this route
@app.get("/prompt")
def prompt_index():
    prompts = get_prompts(connection)
    return [*(prompt.model_dump() for prompt in prompts)]


@app.post("/prompt")
def prompt_create(prompt: Prompt):
    result = create_prompt(connection, prompt)
    if result:
        return {
            "success": "ok"
        }
    else:
        raise RuntimeError("Failed to create prompt")


# TODO: add auth for this route
@app.put("/prompt/{prompt_id}")
def prompt_edit(prompt_id: int, prompt: Prompt):
    if prompt_id != prompt.id:
        raise ValueError("Invalid prompt")

    result = edit_prompt(connection, prompt)
    if result:
        return {
            "success": "ok"
        }
    else:
        raise RuntimeError("Failed to edit prompt")


# TODO: add auth for this route
@app.delete("/prompt")
def prompt_delete():
    return {
        "success": "ok"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")