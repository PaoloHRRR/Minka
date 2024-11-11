from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import time
import sys
from os import getenv
from loguru import logger
from app.router.api import api_router
from app.common.constants import Env
logger.remove()
logger.add(sys.stdout,
           format="<green>{time}</green> <level>{level: <8}</level> <cyan>{name}</cyan> -"
                  " <level>{message}</level>",
           colorize=True)
app = FastAPI(title=getenv(Env.APP.name))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:0.4f} sec"
    return response
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(getenv(Env.APP.port)), log_level="info")
