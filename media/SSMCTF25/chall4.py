from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.Random import get_random_bytes

FLAG = b"ssmctf{this_is_not_the_real_flag}"

e = 3
p, q = getPrime(256), getPrime(256)
N = p * q
padding = get_random_bytes(32)


def update_security():
    global e
    e = 65537

def encrypt_flag():
    flag = bytes_to_long(FLAG + padding)
    print(f"{N = }")
    print(f"Here's your encrypted flag: {pow(flag, e, N)}")

def get_challenge():
    m = bytes_to_long(b"ssmctf" + get_random_bytes(16))
    c = pow(m, e, N)
    print(f"{N = }")
    print(f"{c = }")
    answer = input("Can you recover the message?\n")

    if int(answer) == m:
        print("Oops, looks like e = 3 is insecure, better use a bigger exponent!")
        update_security()
    else:
        print("WRONG!")


def menu():
    print("""
=== sEcUrItY UpDaTe ===
1. Get Challenge
2. Get Encrypted Flag
3. Exit
""")
    option = int(input("Select option: "))

    if option == 1:
        get_challenge()
    elif option == 2:
        encrypt_flag()
    else:
        exit()


if __name__ == "__main__":
    while True:
        menu()