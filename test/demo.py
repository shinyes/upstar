import time
import sys
import os
from print_routes import print_routes
import uvicorn

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from upstar import Upstar, Request, JSONResponse, Response


async def middleware_A(request: Request, call_next):
    print(f"[中间件A] {request.method} {request.url.path}")
    time_a = time.perf_counter()
    response = await call_next(request)
    time_b = time.perf_counter()
    print(
        f"[中间件A] Response status: {response.status_code} 耗时: {time_b - time_a:.4f}秒"
    )
    return response


async def middleware_B(request: Request, call_next):
    print(f"[中间件B] {request.method} {request.url.path}")
    json_data = await request.json()
    request.state._state.update(json_data)
    print(f"[中间件B] Request state: {request.state._state}")
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


async def middleware_E(request, call_next):
    print(f"[中间件E] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"[中间件E] Response status: {response.status_code}")
    return response


app = (
    Upstar()
    .use(middleware_A)  # 全局中间件
    .get(
        "login",
        lambda request: JSONResponse(
            {
                "msg": "登录成功",
                "name": request.state.name,
                "password": request.state.password,
            }
        ),
        middleware_B,
    )
    .group(
        "g",
        Upstar()
        .use(middleware_C)  # v1 组中间件
        .get("1", lambda request: JSONResponse({"message": "1!"}))
        .get(
            "2", lambda request: JSONResponse({"message": "2!"}), middleware_D
        )  # 路由中间件
        .group(
            "nested",
            Upstar()
            .use(middleware_E)  # 嵌套组中间件
            .post("3", lambda request: Response("3!"))
            .post("4", lambda request: Response("4!")),
        ),
    )
)

print_routes(app)
if __name__ == "__main__":
    # 在这里面的脚本不会热重载
    uvicorn.run("demo:app", reload=True, host="0.0.0.0", port=50080)
