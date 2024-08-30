import asyncio

from .app import App
from .bootstrap import bootstrap
from .settings import load_settings


if __name__ == '__main__':
    settings = load_settings()
    app = App()

    bootstrap(app=app, settings=settings)

    try:
        asyncio.run(app.startapp())
    except BaseException as e:
        print(f'{type(e)}: {e!s}.')
    finally:
        asyncio.run(app.shutdown())
