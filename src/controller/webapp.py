
# ./src/agent/webapp.py
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from src.cache import picture

app = FastAPI()


@app.get("/hello")
def read_root(request: Request) -> JSONResponse:
    return JSONResponse(content={"Hello": "World"})

@app.get('/picture')
def get_picture(id: UUID) -> Response:
    # 从缓存中获取图片
    svg = picture.get(id)
    if svg:
        return Response(content=svg, media_type="image/svg+xml")
    else:
        return Response(status_code=404)