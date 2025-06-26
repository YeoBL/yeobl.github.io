from sage.all import * 
from Crypto.Util.number import long_to_bytes
from sympy import totient
from tqdm import tqdm

def gcd(a, b):
    return b if a == 0 else gcd(b % a , a)

def tetration_mod(base, modulo):
    if modulo <= 1:
        return 0
    
    phi = int(totient(modulo))
    e = tetration_mod(base, phi)

    return pow(base, e, modulo)

def get_next():
    global x_cur
    x_cur = (a * x_cur + b) % m

x = [
    10275910798653121436396833379154598008161,
    2068591239728841545706452127889450693176,
    26350147429806384823786121899280661716493,
    25358475244916002220884659082517978530071,
    12563752780567442975545946639227178025296,
    19642601882956204519785723889340847589962,
    6259116168994041128833294897342371591968,
    16406333604491605091556863399044907242384,
    25867766060185127305007083226436225587634
]
y = [x[i + 1] - x[i] for i in range(len(x) - 1)]
u = [abs(y[i + 2] * y[i] - y[i+1] ** 2) for i in range(len(y) - 2)]

m = 0
for val in u:
    m = gcd(m, val)

a = (y[1] * pow(y[0], -1, m)) % m
b = (x[1] - a * x[0]) % m
print(f"{a = }")
print(f"{b = }")

TRIPLE_BAKA = tetration_mod(3, m - 1)
print(f"{TRIPLE_BAKA = }")
x0 = ((x[0] - b) * pow(a, -1, m)) % m
a_n = pow(a, TRIPLE_BAKA, m)
x_final = (a_n * x0 + b * (a_n - 1) * pow(a - 1, -1, m)) % m
print("x_final =", x_final)

ct = 8194779757417092844428719009359907728048
secret = ct ^ x_final
flag = long_to_bytes(secret).decode()
print(f"{flag = }")
