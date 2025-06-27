from Crypto.Util.number import getPrime
from random import getrandbits, randint, choice
from secret import FLAG

tf = getrandbits(48)

p =  2**128 - 159
q = getPrime(256)
g = 2

def make_random_shares(minimum, num_shares):
    coefficients = [tf]
    vv = [pow(g, tf, q)]

    for i in range(1, minimum):
        r = randint(2**58, 2**59)
        coefficients.append(r)
        vv.append(pow(g, r, q))

    shares = []
    for _ in range(num_shares):
        x = randint(2**127, 2**128)
        y = 0
        for power, coeff in enumerate(coefficients):
            y = (y + coeff * pow(x, power, p)) % p
        shares.append((x, y))

    return shares, vv

# STONKS
def GOOGL():
    return make_random_shares(5, 12)

def AMZN():
    return make_random_shares(6, 16)

def META():
    return make_random_shares(5, 15)

def MSFT():
    return make_random_shares(7, 17)

def AAPL():
    return make_random_shares(6, 12)

def NVDA():
    return make_random_shares(7, 16)

def TSLA():
    return make_random_shares(8, 13)

def broker():
    print("""===== broker =====
1. buy stonks
2. sell stonks
3. exit
===== ====== =====""")
    inp = int(input(""))
    if inp == 1:
        stonk = choice([GOOGL, AMZN, META, MSFT, AAPL, NVDA, TSLA])
        shares, vv = stonk()
        print(f"Trade executed: {randint(1,100)} of ${stonk.__name__} bought at ${randint(1,1000)} per share")
        print(f"Transaction Details: {shares[:4]}\n{vv}")
    elif inp == 2:
        print("Error: selling is disabled, STONKS ONLY GO UP!")
    elif inp == 7828322:
        what = int(input("Sir, this is a casino. "))
        if what == tf:
            print(FLAG)
            quit()
    else:
        print("Error: leaving is not allowed")


def main():
    print("Welcome to the stonk market!")
    while True:
        broker()




if __name__ == '__main__':
    main()