from fastapi import BackgroundTasks, Depends, FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.post("/test")
async def register_user(name: str = Form(...)):
    try:
        return PlainTextResponse(content=f"Hello {name}", status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
