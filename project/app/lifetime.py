from app.initial_data import create_superuser


async def startup():
    await create_superuser()
