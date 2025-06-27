from sage.all import *
import hashlib, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tqdm import tqdm

def decrypt_flag(secret: int, iv_hex: str, ct_hex: str) -> bytes:
    h = hashlib.sha1()
    h.update(str(secret).encode('ascii'))
    key = h.digest()[:16]

    iv = bytes.fromhex(iv_hex)
    ct = bytes.fromhex(ct_hex)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)

    if b'SSMCTF' in pt_padded:
        print(pt_padded)

    try:
        pt = unpad(pt_padded, AES.block_size)
    except ValueError as e:
        raise ValueError("Decryption succeeded but padding was invalid") from e

    return pt

def dnc_log_factors(base, P, verbose=True):
    ord = base.order()
    remainders, factors = [], []
    for prime, exponent in factor(ord):
        mult = (ord // (prime ** exponent))
        if prime ** exponent > 20521106721679:
            continue
        P_new, base_new = P * mult, base * mult
        dlog = P_new.log(base_new)
        if verbose:
            print(prime ** exponent, dlog)
        assert P_new == dlog * base_new
        factors.append(prime ** exponent)
        remainders.append(dlog)
    return remainders, factors

p1 = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFED
a1 = 0x76d06
b1 = 0x01
F1 = GF(p1)
E1 = EllipticCurve(F1, [a1, b1])
G1 = E1(
    47063170801806052288146673528871417153526850064394483981146410830175982208544,
    53518176899357161526249489715124114639791104549020667616657543916324221249348
)
pt1 = E1(
    56710714175061483991870664898200691885016604747806913517177632746453560406455,
    22183016490403262414869646241566186015038886824498859131560775826194154678831
)
print(f"{factor(G1.order()) = }")

p2 = 0x1FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD
a2 = 0x01C93A
b2 = 0x01
F2 = GF(p2)
E2 = EllipticCurve(F2, [a2, b2])
G2 = E2(
    44463004732374493397893178641833179486751816974247573994673798864,
    1106794713284151358838640453450775713656116663772692522843863128471
)
pt2 = E2(
    861801353887926730429905301581104022799000762265859378776929570795,
    2414525705848701236524399200022909146362752492100235869363750117869
)
assert pt2 in E2
print(f"{factor(G2.order()) = }")

# dnc_log_factors(G2, pt2)
# dnc_log_factors(G1, pt1)
# Output:
# 2 1
# 3 2
# 3562267 1452015
# 844201807 129853961
# 1475029691 573227031
# 4 1
# 107 12
# 227 153
# 2988429752821 2125536701115
# 20521106721679 17921044611639


div = [4, 107, 227, 2988429752821, 20521106721679, 3, 3562267, 844201807, 1475029691]
rem = [1, 12, 153, 2125536701115, 17921044611639, 2, 1452015, 129853961, 573227031]
mult = 1

iv = 'c001a9fe49c5eaee271777f7deac8eb8'
ct = '12068639a25f527caf97b8f8572723571ebf212cf673e71b5e705f99404cc50e97a5dbbde566ea52fde3bf8caaede3629ede5731bb4340c27a6b352636546f02'

for num in div:
    mult *= num
res = crt(rem, div)
for idx in tqdm(range(2 ** 200 // mult)):
    try:
        ans = decrypt_flag(res, iv, ct)
    except:
        pass
    res = res + mult

# Or attempt discrete_log (only feasible if the subgroup is small):
#    sage: discrete_log(pt1, G1)
#    sage: discrete_log(pt2, G2)