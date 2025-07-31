from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time

app = FastAPI()

# In-memory log store
logs = []

@app.post("/hackrx/run")
async def hackrx_run(request: Request):
    data = await request.json()
    logs.append(data)
    time.sleep(5)
    return JSONResponse(["Internal Server Error" for _ in range(len(data['questions']))])

@app.post("/process_and_upload")
async def get_logs():
    return JSONResponse(content={"logs": logs})