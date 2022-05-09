import procrastinate

from .core.config import settings

app = procrastinate.App(
    connector=procrastinate.AiopgConnector(dsn=settings.DATABASE_URI),
    import_paths=["app.users.tasks"]
)


async def run_workerasync():
    async with app.open():
        await app.run_worker_async()


def run_worker():
    with app.open() as a:
        a.run_worker()
