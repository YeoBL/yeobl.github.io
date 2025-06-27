from hashlib import blake2b, sha1, md5, sha512
from Crypto.Util.number import long_to_bytes
from flag import flag
import ast

n = 2**80

def H(m, hash_func):
    preimage = long_to_bytes(m)
    h = hash_func(preimage).digest()
    return int.from_bytes(h, 'big') % n

def main():
    ice_kachang = H(flag, blake2b)
    print("Let's make Ice Kachang!")
    print(f"follow the recipe and you should get: {ice_kachang}")

    try:
        shaved_ice  = [H(m, blake2b) for m in ast.literal_eval(input("Add shaved_ice: "))]
        red_beans   = [H(m, sha1) for m in ast.literal_eval(input("Add red_beans: "))]
        jelly       = [H(m, md5) for m in ast.literal_eval(input("Add jelly: "))]
        syrup       = [H(m, sha512) for m in ast.literal_eval(input("Add syrup: "))]

        assert any(shaved_ice) and any(red_beans) and any(jelly) and any(syrup)
        assert len(shaved_ice + red_beans + jelly + syrup) <= 128
    except:
        print("You didn't follow the recipe!")
        quit()

    if sum(shaved_ice + red_beans + jelly + syrup) % n == ice_kachang:
        print(flag)
    else:
        print("You did not cook \U0001F614")

if __name__ == '__main__':
    main()