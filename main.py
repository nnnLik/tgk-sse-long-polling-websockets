import asyncio
from datetime import datetime
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def get_sse_datetime():
    while True:
        data = str(datetime.now())
        yield f"event: custom_1\nid: unique_2\ndata: {data}\n\n"
        await asyncio.sleep(0.1)


async def get_polling_datetime():
    while True:
        data = str(datetime.now())
        yield data
        await asyncio.sleep(1)


@app.get("/")
async def home(request: Request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


@app.get("/sse-example")
async def sse():
    return StreamingResponse(get_sse_datetime(), media_type="text/event-stream")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text: {data}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6969, log_level='info')
