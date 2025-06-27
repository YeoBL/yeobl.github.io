from sage.all import *

p =  2**128 - 159

# A = Matrix(ZZ, [[3, 1, 0, 0],
#                 [2, 0, 1, 0],
#                [5, 0, 0, 1]])
# A = Matrix(ZZ, table)
# B = A.LLL()  # Returns the LLL-reduced basis

table = [[0 for _ in range(10)] for __ in range(10)]
transaction = [(198193157717789055527366780661596339848, 166202502717000344279950965663835465592), (297361877263173917664691047674087635752, 336083410361517958484499423796333212464), (308061865278087832960991325596486333105, 337905919901916593851631511113221945932), (299713217553427714493871342376026433055, 41770912335284067759997315164874203869)]

x = [tmp[0] for tmp in transaction]
y = [tmp[1] for tmp in transaction]

# Define vectors for coeff[i] * (pow(x_0, i, p), ... pow(x_3, i, p))
for idx in range(1, 5):
    for pos in range(0, 4):
        table[idx][pos] = pow(x[pos], idx, p)
    table[idx][idx + 4] = 1

# Define vector for 1 * (-y_0, -y_1, -y_2, -y_3)
for idx in range(0, 4):
    table[5][idx] = (-y[idx]) % p
table[5][9] = 2 ** 300

# Define vectors to allow modulo p
for idx in range(0, 4):
    table[6 + idx][idx] = p

table = table[1:]

A = Matrix(ZZ, table)
B = A.LLL()

for row in B:
    if row[0] == row[1] == row[2] == row[3] and row[0].bit_length() < 50:
        print("FOUND IT")
        print("Enter secret menu by entering 7828322")
        ans = -row[0]
        print(f"{ans = }")