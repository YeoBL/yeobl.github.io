from Crypto.Util.number import long_to_bytes
import gmpy2

def recover_m(N, c):
    N = gmpy2.mpz(N)
    c = gmpy2.mpz(c)
    # keep adding N until we land on a perfect cube
    while True:
        root, exact = gmpy2.iroot(c, 3)
        if exact:
            return int(root)
        c += N

# paste in your challenge values here:
N_challenge = 6056534745148887370509137622595153503269326745083953268288575065013553747188788385737503467130883166106982885481133239272481071440487456652945753901450207
c_challenge = 979191251156688116964410474229106853168255224101556179373565776551828110762071351322332729415117139652660157267751125882144323661577120019663074129676123

m = recover_m(N_challenge, c_challenge)
print("m =", m)