import asyncio
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def get_sse_datetime():
    while True:
        data = str(datetime.now())
        # yield f"id: unique_1 \n event: update \n data: {data} \n"
        yield f"event: custom_1\nid: unique_2\ndata: {data}\n"
        yield f"event: custom_2\nid: unique_1\ndata: +1\n\n"
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

@app.get("/long-polling")
async def long_polling():
    async for data in get_polling_datetime():
        yield data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6969, log_level='info')
