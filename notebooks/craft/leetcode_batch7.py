import heapq


def find_kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]


def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    result = [intervals[0]]

    for start, end in intervals[1:]:
        last = result[-1]

        if start <= last[1]:
            last[1] = max(last[1], end)
        else:
            result.append([start, end])

    return result


print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))
print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))
