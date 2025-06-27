from sage.all import *
import random, hashlib
from hashlib import blake2b, sha1, md5, sha512
from Crypto.Util.number import long_to_bytes

MOD = 2 ** 80

def H(m, hash_func):
    preimage = long_to_bytes(m)
    h = hash_func(preimage).digest()
    return int.from_bytes(h, 'big') % MOD

ice_kachang = 380554279638146175205295
shaved_ice  = [H(m, blake2b) for m in [1]]
red_beans   = [H(m, sha1) for m in [1]]
syrup       = [H(m, sha512) for m in [1]]
target = (ice_kachang - sum(shaved_ice + red_beans + syrup)) % MOD
print(f"{target = }")

def h(m: int) -> int:
    return H(m, hashlib.md5)

def exist(hashes, targ_sum):
    n = len(hashes)
    flag = 0
    table = [[0 for _ in range(n + 2)] for __ in range(n + 2)]
    table[-1][0] = MOD
    table[-2][0] = -targ_sum
    table[-2][-1] = 1

    for idx in range(0, n):
        table[idx][0] = hashes[idx]
        table[idx][idx + 1] = 1
        table[-2][idx + 1] = -2

    A = Matrix(ZZ, table)
    B = A.LLL()  # Returns the LLL-reduced basis
    for row in B:
        if row[0] == 0 and row[-1] == 1 and min(row) >= -2:
            flag = 1
            return row
    return False

while True:
    l = []
    while len(l) < 40:
        l.append(random.randrange(2, 1000000))
    l_hashes = [h(x) for x in l]

    res = exist(l_hashes, target)

    if res:
        values = l
        hashes = l_hashes
        indices = res

        indices = [x + 2 for x in indices[1: -1]]
        print(f"{sum(indices) = }")
        tot = 0
        ans = []

        for hash, mult, value in zip(hashes, indices, values):
            tot += hash * mult
            tot %= 2 ** 80
            for idx in range(mult):
                ans.append(value)

        print(f"{ans = }")
        hashed_ans = [H(m, hashlib.md5) for m in ans]
        print(f"{sum(hashed_ans) % MOD = }")
        break
