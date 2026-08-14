def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


print(two_sum([2, 7, 11, 15], 9))


def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


print(contains_duplicate([1, 2, 3, 1]))
print(contains_duplicate([1, 2, 3, 4]))


def valid_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    for char in t:
        if char not in counts:
            return False
        counts[char] -= 1
        if counts[char] == 0:
            del counts[char]
    return len(counts) == 0


print(valid_anagram("anagram", "nagaram"))
print(valid_anagram("rat", "car"))


def group_anagrams(strs):
    groups = {}
    for word in strs:
        key = "".join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())


print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
