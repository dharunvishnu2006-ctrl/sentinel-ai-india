import csv
import heapq
import itertools
import logging
import uuid
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(f"sentinel.{__name__}")


class UrgencyCheck(BaseModel):
    urgency: int = Field(ge=1, le=5)


class Orchestrator:
    def __init__(self):
        self.tasks = []
        self._counter = itertools.count()

    def add_task(self, urgency: int, task: str):
        try:
            UrgencyCheck(urgency=urgency)
        except ValidationError as e:
            logger.warning(f"REJECTED task: {e}")
            return
        trace_id = str(uuid.uuid4())
        count = next(self._counter)
        logger.info(
            f"Task queued: urgency={urgency} task={task} " f"trace_id={trace_id}"
        )
        heapq.heappush(self.tasks, (urgency, count, task, trace_id))

    def next_task(self):
        if not self.tasks:
            return None
        return heapq.heappop(self.tasks)

    def export_history(self, path: str = "task_history.csv"):
        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for urgency, count, task, trace_id in self.tasks:
                writer.writerow([urgency, task, trace_id])
