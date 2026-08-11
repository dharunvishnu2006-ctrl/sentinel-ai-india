result_true = 47 / 5
result_floor = 47 // 5

print("47 / 5 =", result_true)
print("47 // 5 =", result_floor)

remainder = 47 % 5
print("47 % 5 =", remainder)
print(f"{5} agents get {result_floor} tasks each, {remainder} left over")

response_times = [123.456, 89.234, 456.789]

for i, t in enumerate(response_times, start=1):
    print(f"Agent {i}: {t:>8.1f} ms")
