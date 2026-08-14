from collections import deque


class SlidingWindowAverage:
    def __init__(self, window_size=50):
        self.window_size = window_size
        self.window = deque()
        self.total = 0

    def add(self, value):
        self.window.append(value)
        self.total += value
        if len(self.window) > self.window_size:
            removed = self.window.popleft()
            self.total -= removed

    def average(self):
        if not self.window:
            return 0
        return self.total / len(self.window)


class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [float("-inf")] * (2 * self.n)
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index, value):
        i = index + self.n
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

    def query_max(self, left, right):
        result = float("-inf")
        left += self.n
        right += self.n + 1
        while left < right:
            if left % 2 == 1:
                result = max(result, self.tree[left])
                left += 1
            if right % 2 == 1:
                right -= 1
                result = max(result, self.tree[right])
            left //= 2
            right //= 2
        return result


def next_greater_element(values):
    result = [-1] * len(values)
    stack = []
    for i, value in enumerate(values):
        while stack and values[stack[-1]] < value:
            prev_index = stack.pop()
            result[prev_index] = value
        stack.append(i)
    return result


def align_event_streams(stream_a, stream_b, max_gap=5):
    i = j = 0
    aligned = []
    while i < len(stream_a) and j < len(stream_b):
        diff = stream_a[i] - stream_b[j]
        if abs(diff) <= max_gap:
            aligned.append((stream_a[i], stream_b[j]))
            i += 1
            j += 1
        elif diff < 0:
            i += 1
        else:
            j += 1
    return aligned
