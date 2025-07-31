from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
import uvicorn

import os

port = int(os.environ.get("PORT", 4000))

import asyncio
from hard import get_structured_answers

app = FastAPI()

# In-memory log store
logs = []

@app.get("/")
def dead_root():
    return JSONResponse({"message": "hello there!!"})

@app.post("/hackrx/run")
async def hackrx_run(request: Request):
    data = await request.json()
    logs.append(data)
    time.sleep(5)
    results = get_structured_answers(data['documents'], data['questions']);
    if results is None:
        return JSONResponse({'answers': ["Internal Server Error" for _ in range(len(data['questions']))]})
    else:
        return JSONResponse({'answers': results})

@app.post("/process_and_upload")
async def get_logs():
    return JSONResponse(content={"logs": logs})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    uvicorn.run(app, host="0.0.0.0", port=port)