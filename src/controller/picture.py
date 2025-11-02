import json
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse


async def health_check(request: Request) -> JSONResponse:
    return JSONResponse(content={"status": "healthy"})

# 添加自定义路由
async def custom_handler(request: Request) -> Response:
    # 你的自定义逻辑
    data = await request.json()
    
    # 处理逻辑
    result = {"status": "success", "data": data}
    
    return Response(
        content=json.dumps(result),
        media_type="application/json"
    )