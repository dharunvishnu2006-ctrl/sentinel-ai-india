import asyncio
import logging
import re
from src.models import Task
from pydantic import ValidationError

logger = logging.getLogger(f"sentinel.{__name__}")

NAME_PATTERN = re.compile(r"^[A-Za-z0-9 _-]{1,50}$")


def validate_agent_name(name: str) -> str:
    if not NAME_PATTERN.match(name):
        raise ValueError(f"Invalid agent name: {name!r}")
    return name


class BaseAgent:
    def __init__(self, name: str):
        self.name = validate_agent_name(name)
        self.inbox: asyncio.Queue = asyncio.Queue()

    async def receive(self):
        raw = await self.inbox.get()
        try:
            task = Task(**raw)
            return task
        except ValidationError as e:
            logger.warning(f"REJECTED message: {e}")
            return None

    def handle(self, message):
        raise NotImplementedError

    def __repr__(self):
        return f"{type(self).__name__}({self.name})"


class CloudShieldAgent(BaseAgent):
    def handle(self, message):
        logger.info(f"[{self.name}] Security alert: {message}")


class AutoPilotAgent(BaseAgent):
    def handle(self, message):
        logger.info(f"[{self.name}] Dataset event: {message}")
