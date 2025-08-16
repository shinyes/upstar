import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from upstar import Upstar


from starlette.responses import JSONResponse, Response
from print_routes import print_routes
import uvicorn



# 示例中间件函数
async def middleware_A(request, call_next):
    print(f"[中间件A] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"[中间件A] Response status: {response.status_code}")
    return response


async def middleware_B(request, call_next):
    print(f"[中间件B] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"[中间件B] Response status: {response.status_code}")
    return response


async def middleware_C(request, call_next):
    print(f"[中间件C] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"[中间件C] Response status: {response.status_code}")
    return response


async def middleware_D(request, call_next):
    print(f"[中间件D] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"[中间件D] Response status: {response.status_code}")
    return response


app = (
    Upstar()
    .use(middleware_A)  # 全局中间件
    .group(
        "v1",
        Upstar()
        .use(middleware_B)  # v1 组中间件
        .get(
            "hello", lambda request: JSONResponse({"message": "Hello!"}), middleware_C
        )  # 路由中间件
        .get("world", lambda request: JSONResponse({"message": "World!"})),
    )
    .group(
        "v2",
        Upstar()
        .get("test", lambda request: Response("Test!"))
        .group(
            "nested",
            Upstar()
            .use(middleware_D)  # 嵌套组中间件
            .post("hello", lambda request: Response("Hello!"))
            .post("world", lambda request: Response("World!")),
        )
        .get("world", lambda request: Response("World!")),
    )
    .get("ping", lambda request: JSONResponse({"message": "pong"}))
)

print_routes(app)
if __name__ == "__main__":
    uvicorn.run("demo:app", reload=True, host="0.0.0.0", port=8000)
