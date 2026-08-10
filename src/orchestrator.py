import heapq
from pydantic import BaseModel, Field, ValidationError


class UrgencyCheck(BaseModel):
    urgency: int = Field(ge=1, le=5)


class Orchestrator:
    def __init__(self):
        self.tasks = []

    def add_task(self, urgency: int, task: str):
        try:
            UrgencyCheck(urgency=urgency)
        except ValidationError as e:
            print(f"REJECTED task: {e}")
            return
        heapq.heappush(self.tasks, (urgency, task))

    def next_task(self):
        if not self.tasks:
            return None
        return heapq.heappop(self.tasks)
