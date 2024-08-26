from fastapi import FastAPI

from notes.handlers import router as notes_router


app = FastAPI()
app.include_router(notes_router)
