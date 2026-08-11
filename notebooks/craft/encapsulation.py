class NaiveAgent:
    def __init__(self):
        self.status = "idle"


a = NaiveAgent()
print("Before:", a.status)

a.status = "failed"
print("After:", a.status)


class SafeAgent:
    VALID_TRANSITIONS = {
        "idle": {"working"},
        "working": {"failed", "idle"},
        "failed": {"idle"},
    }

    def __init__(self):
        self._status = "idle"

    @property
    def status(self):  # type: ignore[misc]
        return self._status

    def set_status(self, new_status):
        allowed = self.VALID_TRANSITIONS[self._status]
        if new_status not in allowed:
            raise ValueError(f"Cannot go from {self._status!r} to {new_status!r}")
        self._status = new_status


b = SafeAgent()
print("Status:", b.status)

b.set_status("working")
print("Status:", b.status)

try:
    b.status = "hacked"  # type: ignore[misc]
except AttributeError as e:
    print("Direct write blocked:", e)

try:
    b.set_status("idle")
    b.set_status("failed")
except ValueError as e:
    print("Invalid transition blocked:", e)
