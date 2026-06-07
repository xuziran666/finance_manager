from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import DEBUG, HOST, PORT
from route import api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    print(f"服务启动于 http://{HOST}:{PORT}")
    uvicorn.run("app:app", host=HOST, port=PORT, reload=DEBUG)
