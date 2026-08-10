import asyncio
from src.models import Task
from pydantic import ValidationError


class Agent:
    def __init__(self, name: str):
        self.name = name
        self.inbox: asyncio.Queue = asyncio.Queue()

    async def receive(self):
        raw = await self.inbox.get()
        try:
            task = Task(**raw)
            return task
        except ValidationError as e:
            print(f"REJECTED message: {e}")
            return None

    def __repr__(self):
        return f"Agent({self.name})"
