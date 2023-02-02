# Development uvicorn configuration that allows us to terminate open socket
# connections during reload in development. ONLY USE IN DEVELOPMENT.

import uvicorn
from uvicorn.supervisors import ChangeReload

if __name__ == "__main__":
    config = uvicorn.Config(
        "{{ cookiecutter.project_slug }}.asgi:application",
        port=8000,
        reload=True,
        debug=True,
        reload_includes=["*.py", "*.html"],
        host="0.0.0.0",
    )
    server = uvicorn.Server(config)
    server.force_exit = True

    sock = config.bind_socket()
    supervisor = ChangeReload(config, target=server.run, sockets=[sock])
    supervisor.run()
