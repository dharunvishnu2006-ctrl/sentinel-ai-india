def is_palindrome(s):
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True


print(is_palindrome("A man, a plan, a canal: Panama"))
print(is_palindrome("race a car"))


def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1

    while left < right:
        total = numbers[left] + numbers[right]

        if total == target:
            return [left + 1, right + 1]
        elif total < target:
            left += 1
        else:
            right -= 1

    return []


print(two_sum_sorted([2, 7, 11, 15], 9))


def move_zeroes(nums):
    insert_pos = 0

    for num in nums:
        if num != 0:
            nums[insert_pos] = num
            insert_pos += 1

    for i in range(insert_pos, len(nums)):
        nums[i] = 0

    return nums


print(move_zeroes([0, 1, 0, 3, 12]))
