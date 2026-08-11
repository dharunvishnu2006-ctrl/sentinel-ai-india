def add_task(task, task_list=[]):
    task_list.append(task)
    return task_list


result1 = add_task("Report A")
print("First call:", result1)

result2 = add_task("Report B")
print("Second call:", result2)

result3 = add_task("Report C")
print("Third call:", result3)

print("Same object?", result1 is result2 is result3)


def add_task_fixed(task, task_list=None):
    if task_list is None:
        task_list = []
    task_list.append(task)
    return task_list


fixed1 = add_task_fixed("Report X")
print("fixed call 1:", fixed1)

fixed2 = add_task_fixed("Report Y")
print("Fixed call 2:", fixed2)

print("Same object now?", fixed1 is fixed2)
