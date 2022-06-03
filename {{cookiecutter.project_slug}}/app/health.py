from arq.worker import async_check_health as arq_check_health
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from tortoise.exceptions import DBConnectionError

from app.core.logger import logger
from .users.models import User
from .worker import WorkerSettings

router = APIRouter(prefix="/health")


class APIHealth(BaseModel):
    database_is_online: bool = True
    arq_worker_is_online: bool = True


@router.get(
    "/",
    response_model=APIHealth,
    responses={
        503: {"description": "Some or all services are unavailable", "model": APIHealth}
    },
)
async def check_health(response: Response):
    """Check availability of several's service to get an idea of the api health."""
    # TODO: you can make this a bit more complete and detailed and add more checks
    #  like trying to insert a record in the db
    logger.info("Health Check⛑")
    health = APIHealth()
    # database check
    try:
        list(await User.all())
    except DBConnectionError:
        health.database_is_online = False
        logger.exception("Database connection failed")
    # arq worker check
    health_check_key = getattr(WorkerSettings, "health_check_key", None)
    queue_name = getattr(WorkerSettings, "queue_name", None)
    code = await arq_check_health(
        redis_settings=WorkerSettings.redis_settings,
        health_check_key=health_check_key,
        queue_name=queue_name,
    )
    if code == 1:
        health.arq_worker_is_online = False
        logger.error("ARQ worker is not online")

    if not all(health.dict().values()):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return health
