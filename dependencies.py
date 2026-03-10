from database import db_dependency
from links_service import LinksService
from typing import Annotated
from fastapi import Depends


async def get_link_service(db: db_dependency) -> LinksService:
    return LinksService(db)


LinkServiceDependency = Annotated[LinksService, Depends(get_link_service)]
