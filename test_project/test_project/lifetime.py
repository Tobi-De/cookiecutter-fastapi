from test_project.initial_data import create_superuser



async def startup() -> None:
    await create_superuser()
