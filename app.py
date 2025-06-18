import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import markdown
from pydantic import BaseModel
import aiofiles

app = FastAPI()


class Note(BaseModel):
    title: str
    content: str

@app.post("/notes")
async def add(
        note: Note
):
    try:
        output_html = markdown.markdown(note.content)
        uid = uuid.uuid4()
        async with aiofiles.open(f'notes/{uid}.md', mode='w') as f:
            await f.write(output_html)
        return uid
    except Exception as e:
        print(e)
        return HTTPException(status_code=500)

@app.get("/notes/{uid}")
async def get_note(uid: str):
    try:
        async with aiofiles.open(f'notes/{uid}.md', mode='r') as f:
            content = await f.read()
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError as e:
        return HTTPException(status_code=404, detail=f'Note {uid} not found')
    except Exception as e:
        print(e)
        return HTTPException(status_code=500)

