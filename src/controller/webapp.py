# ./src/agent/webapp.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/hello")
def read_root(request: Request) -> JSONResponse:
    return JSONResponse(content={"Hello": "World"})
