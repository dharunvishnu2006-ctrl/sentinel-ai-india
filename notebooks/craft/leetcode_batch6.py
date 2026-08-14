def climb_stairs(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


for n in [1, 2, 3, 5, 10]:
    print(f"n={n}: {climb_stairs(n)}")


def coin_change(coins, amount):
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for current in range(1, amount + 1):
        for coin in coins:
            if current >= coin:
                dp[current] = min(dp[current], dp[current - coin] + 1)
    return -1 if dp[amount] == float("inf") else dp[amount]


print(coin_change([1, 2, 5], 11))
print(coin_change([2], 3))
