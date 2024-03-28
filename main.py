import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def progress_generator():
    for i in range(1, 101):
        yield f"data: {i}\n\n"
        await asyncio.sleep(0.1)


@app.get("/")
async def home(request: Request):
    template = "sse-index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


@app.get("/progress")
async def sse():
    return StreamingResponse(progress_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6969, log_level='info')
