import asyncio

from .app import App
from .bootstrap import bootstrap
from .settings import load_settings


if __name__ == '__main__':
    settings = load_settings()
    app = App()

    bootstrap(app=app, settings=settings)
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(app.startapp())
        print('Started')
        loop.run_forever()
    except BaseException as e:
        print(f'{type(e)}: {e!s}.')
    finally:
        loop.run_until_complete(app.shutdown())
        print('Stopped')
