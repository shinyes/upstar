def print_routes(app, prefix=""):
    def _print(app, prefix, level):
        indent = "  " * level
        if level == 0:
            print("\n==== Registered Routes ====")
        for route in getattr(app, "routes", []):
            if isinstance(route, Route):
                methods = ",".join(sorted(route.methods))
                print(
                    f"{indent}- [ROUTE] {prefix}{route.path:<20} | Methods: {methods:<10} | Name: {route.name}"
                )
            elif isinstance(route, Mount):
                print(f"{indent}- [MOUNT] {prefix}{route.path}/")
                _print(route.app, prefix + route.path, level + 1)
            else:
                print(f"{indent}- [OTHER] {route}")

    from starlette.routing import Route, Mount

    routes_info = []

    def _collect_routes(app, prefix):
        for route in getattr(app, "routes", []):
            if isinstance(route, Route):
                methods = ",".join(sorted(route.methods))
                routes_info.append([f"{prefix}{route.path}", methods, route.name])
            elif isinstance(route, Mount):
                _collect_routes(route.app, prefix + route.path)

    _collect_routes(app, prefix)

    # 输出表头
    print("\n{:<30} {:<15} {:<20}".format("Path", "Methods", "Name"))
    print("-" * 70)
    for path, methods, name in routes_info:
        print(f"{path:<30} {methods:<15} {name:<20}")
