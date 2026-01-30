from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import registry, relationship, column_property
from dishka.integrations.fastapi import setup_dishka


from src.domain.entities import *
from src.infra.tables import chats, messages
from src.container import container
from src.interfaces.http import chat_couter
from src.application.errors import ChatNotFound


def map_tables():
    mapper_registry = registry()
    mapper_registry.map_imperatively(Message, messages)
    mapper_registry.map_imperatively(Chat, chats, properties={
        "messages": relationship(Message, lazy="raise")
    })
    mapper_registry.configure()


@asynccontextmanager
async def lifespan(app: FastAPI):
    map_tables()
    setup_routers(app)
    yield
    await container.close()


app = FastAPI(lifespan=lifespan)
setup_dishka(container, app)


@app.exception_handler(ChatNotFound)
async def handle_not_fount(r: Request, e: ChatNotFound):
    return JSONResponse({"detail": str(e)}, 404)


def setup_routers(app: FastAPI):
    app.include_router(chat_couter)
