import time
import random
import sys

sys.path.insert(0, ".")  # noqa: E402
from src.trie import Trie, kmp_search  # noqa: E402

random.seed(3)

prefixes = ["sec", "net", "aut", "dat", "rou"]
suffixes = ["urity", "work", "hentication", "abase", "ting"]
capabilities = []
for i in range(5000):
    cap = random.choice(prefixes) + random.choice(suffixes) + str(i)  # nosec B311
    capabilities.append(cap)

capabilities.append("security_scan")
capabilities.append("security_audit")
capabilities.append("secure_channel")

trie = Trie()
for cap in capabilities:
    trie.insert(cap)

start = time.perf_counter()
trie_results = trie.starts_with("sec")
time_trie = time.perf_counter() - start

start = time.perf_counter()
naive_results = [c for c in capabilities if c.startswith("sec")]
time_naive = time.perf_counter() - start

print(f"Trie:  {len(trie_results)} matches, {time_trie:.8f}s")
print(f"Naive: {len(naive_results)} matches, {time_naive:.8f}s")
print(f"Results match: {sorted(trie_results) == sorted(naive_results)}")

trie.insert("zzzrare_capability")

start = time.perf_counter()
rare_trie = trie.starts_with("zzzrare")
time_rare_trie = time.perf_counter() - start

start = time.perf_counter()
rare_naive = [
    c for c in capabilities + ["zzzrare_capability"] if c.startswith("zzzrare")
]
time_rare_naive = time.perf_counter() - start

print(f"Rare prefix - Trie:  {time_rare_trie:.8f}s")
print(f"Rare prefix - Naive: {time_rare_naive:.8f}s")

text = "a" * 10000 + "b"
pattern = "a" * 100 + "b"

start = time.perf_counter()
kmp_matches = kmp_search(text, pattern)
time_kmp = time.perf_counter() - start


def naive_search(text, pattern):
    matches = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i : i + len(pattern)] == pattern:
            matches.append(i)
    return matches


start = time.perf_counter()
naive_matches = naive_search(text, pattern)
time_naive_kmp = time.perf_counter() - start

print(f"KMP:   {kmp_matches}, {time_kmp:.6f}s")
print(f"Naive: {naive_matches}, {time_naive_kmp:.6f}s")
