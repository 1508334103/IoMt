import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="智能军事装备管理与作战部署系统",
    description="为明朝军队提供装备管理、作战任务分配与态势感知的综合平台",
    version="0.1.0"
)


@app.get("/")
async def read_root():
    return {"msg": "Backend Initialized"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
