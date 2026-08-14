def search_rotated(nums, target):
    low, high = 0, len(nums) - 1

    while low <= high:
        mid = (low + high) // 2

        if nums[mid] == target:
            return mid

        if nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1

        else:
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1


print(search_rotated([4, 5, 6, 7, 0, 1, 2], 0))
print(search_rotated([4, 5, 6, 7, 0, 1, 2], 3))


def can_jump(nums):
    furthest = 0

    for i, jump in enumerate(nums):
        if i > furthest:
            return False

        furthest = max(furthest, i + jump)

    return True


print(can_jump([2, 3, 1, 1, 4]))
print(can_jump([3, 2, 1, 0, 4]))
