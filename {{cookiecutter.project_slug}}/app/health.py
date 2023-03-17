from saq.worker import async_check_health as saq_check_health
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from tortoise.exceptions import DBConnectionError

from app.core.logger import logger
from app.worker import queue
from .users.models import User

router = APIRouter(prefix="/health")


class APIHealth(BaseModel):
    database_is_online: bool = True
    saq_worker_is_online: bool = True


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

    # saq worker check
    code = await saq_check_health(queue)
    if code == 1:
        health.saq_worker_is_online = False
        logger.error("SAQ worker is not online")

    if not all(health.dict().values()):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return health
