import uuid

from fastapi import FastAPI, HTTPException
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
