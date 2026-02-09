from datetime import date
from fastapi import APIRouter

from src.prompts.model import Prompt
from src.prompts.repository import Prompt, create_prompt, edit_prompt, get_prompts, get_todays_prompt


prompts_router = APIRouter(prefix="/prompts")


@prompts_router.get("/{today}")
async def prompt_show(today: str):
    if today != date.today().isoformat():
        raise ValueError(f"Unable to fetch for that day")

    prompt = await get_todays_prompt(today)
    if prompt == None:
        raise RuntimeError("Prompt not found")
    
    return prompt.model_dump()


# TODO: add auth for this route
@prompts_router.get("/")
async def prompt_index():
    prompts = await get_prompts()
    return [*(prompt.model_dump() for prompt in prompts)]


@prompts_router.post("/")
async def prompt_create(prompt: Prompt):
    result = await create_prompt(prompt)
    if result:
        return {
            "success": "ok"
        }
    else:
        raise RuntimeError("Failed to create prompt")


# TODO: add auth for this route
@prompts_router.put("/{prompt_id}")
async def prompt_edit(prompt_id: int, prompt: Prompt):
    if prompt_id != prompt.id:
        raise ValueError("Invalid prompt")

    result = await edit_prompt(prompt)
    if result:
        return {
            "success": "ok"
        }
    else:
        raise RuntimeError("Failed to edit prompt")


# TODO: add auth for this route
@prompts_router.delete("/")
async def prompt_delete():
    return {
        "success": "ok"
    }
