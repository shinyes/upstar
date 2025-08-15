# version: 1.0.0

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable


class Upstar(Starlette):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.current_path = ""

    def group(self, path: str, upstar: "Upstar") -> "Upstar":
        """
        path 不要带开头的 `/`
        """
        self.mount(f"{self.current_path}/{path}", upstar)
        return self

    def use(self, middleware) -> "Upstar":
        """
        支持直接传入函数，自动包装为 Middleware。

        此外，要记得可以为 request.state.名字 进行赋值，以便于在后续处理这个request的过程中使用这个值
        ```python
        # 示例中间件函数
        async def middleware_A(request, call_next):
            print(f"[中间件A] {request.method} {request.url.path}")
            response = await call_next(request) # 将 request 传递给下一个中间件或者最终的 handler
            print(f"[中间件A] Response status: {response.status_code}")
            return response # 结束中间件处理
        ```
        """
        if callable(middleware):
            self.add_middleware(BaseHTTPMiddleware, dispatch=middleware)
        return self

    def get(self, path: str, handler: Callable, middleware=None) -> "Upstar":
        if callable(middleware):
            middleware = Middleware(BaseHTTPMiddleware, dispatch=middleware)
        self.routes.append(
            Route(
                f"/{path}",
                handler,
                methods=["GET"],
                middleware=[middleware] if middleware else [],
            )
        )
        return self

    def post(self, path: str, handler: Callable, middleware=None) -> "Upstar":
        if callable(middleware):
            middleware = Middleware(BaseHTTPMiddleware, dispatch=middleware)
        self.routes.append(
            Route(
                f"/{path}",
                handler,
                methods=["POST"],
                middleware=[middleware] if middleware else [],
            )
        )
        return self

    def put(self, path: str, handler: Callable, middleware=None) -> "Upstar":
        if callable(middleware):
            middleware = Middleware(BaseHTTPMiddleware, dispatch=middleware)
        self.routes.append(
            Route(
                f"/{path}",
                handler,
                methods=["PUT"],
                middleware=[middleware] if middleware else [],
            )
        )
        return self

    def delete(self, path: str, handler: Callable, middleware=None) -> "Upstar":
        if callable(middleware):
            middleware = Middleware(BaseHTTPMiddleware, dispatch=middleware)
        self.routes.append(
            Route(
                f"/{path}",
                handler,
                methods=["DELETE"],
                middleware=[middleware] if middleware else [],
            )
        )
        return self
