---
tags: Crypto
---

# SCTF 2025 Training Challs Writeups

## General remarks

I set a few of the training challenges for SCTF 2025. The challenges were intended to be as beginner-friendly as possible, to ensure accessibility even for those new to Crypto or CTFs in general.

Here are the challs I set/ported over (from picoCTF) and their writeups:

1. [Baby RSA](#baby-rsa)
2. [Baby Diffie Hellman](#baby-diffie-hellman)
3. [Baby Ciphers](#baby-ciphers)
4. Baby Math
5. [picoCTF 2022 - bloat.py (modified)](#picoctf-2022---bloatpy-modified)
6. [picoCTF 2023 - timer](#picoctf-2023---timer)

## Baby RSA

### Description

RSA is a widely used public key cryptosystem. In this challenge, you will be given a public key and a ciphertext. Can you decrypt the ciphertext and find the flag?

Files Provided:

- [values.txt](/media/SCTF25/values.txt)

### Writeup

First, let's start by understanding how RSA works.

Let's say Alice wants to create a channel for Bob to send encrypted messages to her that no one else can read. She goes through this process:

#### Key Generation (code sameple below)

1. Alice selects two large prime numbers, $p$ and $q$
2. She computes $N = p \cdot q$, $N$ will serve as the _modulus_ for our encryption later on
3. Alice calculates the [Euler's Totient Function](https://brilliant.org/wiki/eulers-totient-function/) of $N$ with the formula $\phi (N) = (p - 1) \cdot (q- 1)$; this works since the prime factorization of $N$ is $p \cdot q$
4. Considering $\phi(n)$, Alice chooses some $e$ s.t. $gcd(N, e) = 1$; it becomes obvious why the aforementioned condition must hold later on in our **decryption** process
5. Alice gives the public key pair, $(N, e)$, to Bob

```python
from Crypto.Util.number import getPrime

# === Step 1 === 
p = getPrime(512)
q = getPrime(512)

# === Step 2 ===
N = p * q

# === Step 3 ===
phi_N = (p - 1) * (q - 1)

# === Step 4 ===
e = 0x10001

print(f"{p = }")
print(f"{q = }")
print(f"{N = }")
print(f"{phi_N = }")

# Output:
# p = 11996598273605636145069419593205005846975886031384924121525649872736600857931317463826741254540229918836213397425790401377065109199078890777034271748352803
# q = 11529332781459115465320542363273346403758998590779750801735045957912871132251628344661856090782819674759143792781986640386149201540006310809153803808787383
# N = 138312773741877291672357397663809010934140453857971665783406363279809934372759262739011787973458255321308759704546691267715470612972075635684713198071066863926094313139733670436026979253138676514853751406467734056724479988541636788408198686566031787831322699142635868515592233916796854802444681820907099084549
# phi_N = 138312773741877291672357397663809010934140453857971665783406363279809934372759262739011787973458255321308759704546691267715470612972075635684713198071066840400163258074982060046065022774786425779969129241792810796028649339069646605462390197968686464781729103785445660738550470702486115717243095632831541944364
```

Now, Bob has received the public key pair, $(N,e)$. He follows these steps to encrypt a secret message, $msg$

#### Encryption (code sample below)

1. Bob converts his message, $msg$ to an integer, $pt$; we can use python's `pycryptodome` library to do this
2. Next, he encrypts $pt$ into $ct$ with the formula $ct \equiv pt^{e} \space (mod \space N)$; `e=0x1001` is a common choice of $e$
3. Bob sends $ct$ to Alice, for her to decrypt

```python
from Crypto.Util.number import bytes_to_long
# run `pip install pycryptodome` if it is not currently installed

e = 0x10001
N = 138312773741877291672357397663809010934140453857971665783406363279809934372759262739011787973458255321308759704546691267715470612972075635684713198071066863926094313139733670436026979253138676514853751406467734056724479988541636788408198686566031787831322699142635868515592233916796854802444681820907099084549

msg = "hello, this is a secret message"
pt = bytes_to_long(msg.encode('UTF-8'))

ct = pow(pt, e, N)
print(f"{ct = }")

# ct = 66590078406431864155269238127192115295609648732772441452460501772391677180014077326200367705353791761442972311060357397439413829674643507788438343205587828559626302284973767398769362935501215148162207076851993424099823386066052328564997084130299315404076623317020097274086180469642150794534311465381986880107
```

Even if an eavesdropper, Eve, somehow intercepts the message $ct$, she will not be able to decrypt it into $pt$ if it is properly encrypted.

#### Decryption (code sample below)

1. Alice computes $d \equiv e^{-1} \space (mod \space \phi (N))$
2. Using the formula $ct^{d} \equiv pt \space (mod \space N)$, Alice retrieves $pt$
3. Alice converts $pt$, an integer, back into string form; we can use python's `pycryptodome` library to do this

```python
from Crypto.Util.number import long_to_bytes
p = 11996598273605636145069419593205005846975886031384924121525649872736600857931317463826741254540229918836213397425790401377065109199078890777034271748352803
q = 11529332781459115465320542363273346403758998590779750801735045957912871132251628344661856090782819674759143792781986640386149201540006310809153803808787383
N = 138312773741877291672357397663809010934140453857971665783406363279809934372759262739011787973458255321308759704546691267715470612972075635684713198071066863926094313139733670436026979253138676514853751406467734056724479988541636788408198686566031787831322699142635868515592233916796854802444681820907099084549
e = 0x10001
ct = 66590078406431864155269238127192115295609648732772441452460501772391677180014077326200367705353791761442972311060357397439413829674643507788438343205587828559626302284973767398769362935501215148162207076851993424099823386066052328564997084130299315404076623317020097274086180469642150794534311465381986880107

phi_N = (p - 1) * (q - 1)

# === Step 1 ===
d = pow(e, -1, phi_N)

# === Step 2 === 
pt = pow(ct, d, N)

# === Step 3 === 
msg = long_to_bytes(pt).decode()

print(f"{msg = }")
```

You might ask, why does $ct^{d} \equiv pt \space (mod \space N)$ hold? To answer this, we need to take a look at [Euler's Theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem) which tells us that for any 2 coprime integers $(a, n)$, $a ^{\phi (n)} \equiv 1 \space (mod \space n)$

Here, $gcd(pt, N) = 1$ holds (it holds for > 99.999% values of $pt$, in fact, $\frac{\phi (N)}{N}$ values $\in [1, N)$ have a gcd of $1$). The corollary is that $pt^{\phi (N)} \equiv 1 \space (mod \space N)$.

By choosing $d \equiv e^{-1} \space (mod \space \phi (N))$, we get $e \cdot d \equiv 1 \space (mod \space \phi (N)) \Rightarrow e \cdot d = k \cdot \phi (N) + 1, k \in \mathbb{Z}$

Applying the aforementioned formula, we get 

$$
\begin{align*}
    ct^d & \equiv (pt ^ e) ^ d && \space (mod \space N) \\
         & \equiv pt ^ {e \cdot d} && \space (mod \space N) \\
         & \equiv pt ^ {k \cdot \phi(N) + 1} && \space (mod \space N) \\
         & \equiv pt ^ {k \cdot \phi(N)} \cdot pt && \space (mod \space N) \\
         & \equiv (pt ^ {\phi(N)}) ^ k \cdot pt && \space (mod \space N) \\
         & \equiv 1 ^ k \cdot pt && \space (mod \space N) \\
         & \equiv pt && \space (mod \space N) \\
\end{align*}
$$

#### Retrieving The Flag

Now that we know how RSA works, let's retrieve the flag with the values in the challenge:

```python
N = 138312773741877291672357397663809010934140453857971665783406363279809934372759262739011787973458255321308759704546691267715470612972075635684713198071066863926094313139733670436026979253138676514853751406467734056724479988541636788408198686566031787831322699142635868515592233916796854802444681820907099084549
e = 65537
p = 11996598273605636145069419593205005846975886031384924121525649872736600857931317463826741254540229918836213397425790401377065109199078890777034271748352803
ct = 23303902472439364601400610165551656518493821119047909723492875263500112136980783683129651013037950319957072514387924720844366993096123785590772579351718636839441852796582801406943584212307393739154583251209665140171544643625178410939109184344556283724001694711941795642330913723038598484869456343973132964577
```

Notice that we are not given $p$, but since we know that $N = p \cdot q$, we can simply calculate it:

```python
q = N // p
```

Next, we calculate $\phi (N) = (p - 1) \cdot (q -1)$

```python
phi = (p - 1) * (q - 1)
```

Then we find $d \equiv e^{-1} \space (mod \space \phi (N))$

```python
d = pow(e, -1, phi)
```

We use $d$ to retrieve $pt$:

```python
pt = pow(ct, d, N)
```

Lastly we convert $pt$ into a string and print it:

```python
from Crypto.Util.number import long_to_bytes
# run `pip install pycryptodome` if it is not currently installed

flag = long_to_bytes(m).decode()
print(f"{flag = }")
```

[My solve script](/media/SCTF25/solve1.py)

## Baby Diffie Hellman

### Description

Diffie Hellman is a widely used private key cryptosystem. In this challenge, Alice has both her own private and public keys alongside Bob’s public key. Can you help her decrypt the ciphertext and find the flag?

Files Provided:

- [source.py](/media/SCTF25/source2.py)

### Writeup

First, let's start by understanding how Diffie-Hellman works.

Suppose Alice and Bob want to create a shared key (for AES encryption whatsoever), but do not have a secure channel to exchange this key, due to the presence of Eve, an eavesdropper who can listen in to their communications. They go through the following process

#### Shared Key Generation (Code Sample Below)

1. Alice chooses some large prime $p$, and a generator, $g$, and broadcasts $(p, g)$ to Bob
2. Alice also chooses her own private key, $a \in [0, p)$, and generates her public key $A = g^a \space (mod \space p)$, and broadcasts her public key, $A$ to Bob
3. Bob chooses his own private key, $b \in [0, p)$, and generates his public key $B = g^b \space (mod \space p)$, and broadcasts his public key, $B$ to Alice. Now, both Alice and Bob have sufficient information to compute the shared key $S = g^{a \cdot b} \space (mod \space p)$
4. Alice has $a, A$ and $B$, and simply computes $S = B^{a} = g ^ {a \cdot b} \space (mod \space p)$
5. Bob has $b, B$ and $A$, and simply computes $S = A^{b} = g ^ {b \cdot a} \space (mod \space p)$

##### Note: Eve, the eavesdropper, only has $A$ and $B$, which are by themselves unable to compute $S$, unless $a$ or $b$ is trivially recoverable

```python
# === Step 1 ===
# N is our modulus
N = getPrime(1024)

# g is our generator
g = 2

# === Step 2 ===
# a and A are Alice's private and public keys respectively
a = randrange(1024, N)
A = pow(g, a, N)

# === Step 3 ===
# b and B are Bob's private and public keys respectively
b = randrange(1024, N)
B = pow(g, b, N)

# === Step 4 ===
# Alice computes the shared key using Bob's public key and her own private key
shared_key_alice = pow(B, a, N)

# === Step 5 ===
# Bob computes the shared key using Alice's public key and his own private key
shared_key_bob = pow(A, b, N)

# This should always return true, i.e. both shared keys should match
assert shared_key_alice == shared_key_bob 

# Now, Alice and Bob can use the shared key for symmetric encryption algorithms such as AES
# Eve, however, is unable to compute the shared key unless a or b are trivially recoverable
```

#### Retrieving The Flag

In this challenge, we are playing the role of Alice, and are given $a, A$ and $B$. Using the above formula, we simply calculate $S = B^{a} \space (mod \space n)$ and use the provided `decrypt_flag` function to decrypt the encoded flag.

[My solve script](/media/SCTF25/solve2.py).

## Baby Ciphers

### Description

I have split my flag into multiple parts and encrypted them with various techniques!

You will never be able to find the original flag!

Files Provided:

- [source.py](/media/SCTF25/source3.py)

### Writeup

In this challenge, our flag is split into 4 parts, then passed through some ciphers/base64 encoding.

```python
# Defining a flag of length 36, all letters are lowercase
flag = 'sctf{k3yl355_c1ph3rs_4r3_n0t_s3cur3}'

# Split the flag into 4 parts, each of equal length
part_length = len(flag) // 4
parts = [flag[part_length * x : part_length * (x + 1)] for x in range(4)]

# Apply different techniques to hide flag
parts[0] = codecs.decode(parts[0], 'rot_13')
parts[1] = to_atbash(parts[1])
parts[2] = base64.b64encode(parts[2].encode()).decode()
parts[3] = to_morse(parts[3])
```

To retrieve the original flag, we simply undo the encodings/ciphers

#### ROT_13

Since the alphabet is cyclic with length $13$, we simply apply ROT_13 on `part[0]` again

#### Atbash Cipher

Atbash is a **monoalphabetic** cipher, meaning each character in the plaintext has a one-to-one mapping in the ciphertext. We simply find the mapping and reverse it, to get the plaintext.

#### Base64 encoding

Base64 is an encoding that simply "translates" information from one form into another. We can use python's _base64_ library to decode it back to UTF-8.

#### Morse Code

Similar to Atbash, Morse Code is also a **monoalphabetic** cipher, hence we simply have to match each phrase to the original characters and join them together.

[My solve script](/media/SCTF25/solve4.py)

## Baby Math

### Description

We managed to steal some information about a secret flag. Can you piece it together to get the whole thing?

Files Provided:

- [source.py](/media/SCTF25/source5.py)

### Writeup

We are given a bunch of $(divisor, remainder)$ pairs of $flag$ and are tasked to recover it's original value.

First, we use [Chinese Remainder Theorem (CRT)](https://brilliant.org/wiki/chinese-remainder-theorem/) to recover some $x$ that fulfils the congruences we were given:

$$
\begin{align*}
    x & \equiv remainder_1 && (mod \space divisor_1) \\
    & \equiv remainder_2 && (mod \space divisor_2) \\
    & \equiv remainder_3 && (mod \space divisor_3) \\
    & \cdots \\
    & \equiv remainder_{17} && (mod \space divisor_{17}) \\
\end{align*}
$$

```python
def crt_implementation(divisors, remainders):
    product = 1
    for divisor in divisors:
        product *= divisor

    ans = 0
    for divisor, remainder in zip(divisors, remainders):
        ans += (product // divisor) * pow(product // divisor, -1, divisor) * remainder
        ans %= product
    
    for divisor, remainder in zip(divisors, remainders):
        assert ans % divisor == remainder
    
    return ans, product

divisors = [439429297, 107, 60586153, 509311637, 56196341, 587, 1061, 3096757, 59, 193, 3637, 130003, 37243, 1148339, 254899, 15140887, 1904537]
remainders = [319989397, 11, 3768949, 192286989, 6160298, 584, 830, 550668, 32, 181, 2842, 90486, 2658, 608727, 237542, 13861648, 862306]

rem, prod = crt_implementation(divisors, remainders)
```

Using CRT, we get the following equation
$$
flag \equiv rem \space (mod \space prod)
$$

This means that $flag = rem + k \cdot prod, k \in \mathbb{Z}$

We further notice that in [source.py](/media/SCTF25/source5.py), we are told that the flag has 39 characters, hence $flag$ only has at most 312 bits.

We check the number of bits that $prod$:

```python
print(prod.bit_length())
```

Since $prod$ only has at most 14 bits less than $flag$, we know that $k \le 2^{15}$ (otherwise, $k \cdot prod \gt 2 ^ {312}$).

We simply try all $2^{15}$ possible values of $k$ then check if the candidate value of $flag = rem + k \cdot prod$ starts with `sctf`. If it does, we print it out accordingly.

[My solve script](/media/SCTF25/solve6.py)

## picoCTF 2022 - bloat.py (modified)

### Description

Run the Python program bloat.py in the same directory as the encrypted flag, flag.txt.enc.

Files Provided:

- [bloat_files.zip](/media/SCTF25/bloat_files.zip)

### Writeup

On first impression, the code appears to be mildly obfuscated by creating a charset `a` and converting all strings into their individual characters, then representing each character as a particular index of `a`

```python
import sys
a = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"+ \
            "[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
def arg133(arg432):
  if arg432 == a[71]+a[64]+a[79]+a[79]+a[88]+a[66]+a[71]+a[64]+a[77]+a[66]+a[68]:
    return True
  else:
    print(a[51]+a[71]+a[64]+a[83]+a[94]+a[79]+a[64]+a[82]+a[82]+a[86]+a[78]+\
a[81]+a[67]+a[94]+a[72]+a[82]+a[94]+a[72]+a[77]+a[66]+a[78]+a[81]+\
a[81]+a[68]+a[66]+a[83])
    sys.exit(0)
    return False
def arg111(arg444):
  return arg122(arg444.decode(), a[81]+a[64]+a[79]+a[82]+a[66]+a[64]+a[75]+\
a[75]+a[72]+a[78]+a[77])
```

To make this more readable, we replace all of `a[idx]` with the literal string values, and join adjacent strings together. For instance, _'a'+'b'+'c'_ = _'abc'_. We can do this by deleting all _'+'_ strings to combine them together _'a'+'b'+'c'_ $\rightarrow$ _'a **'+'** b **'+'** c'_ $\rightarrow$ _'abc'_. A similar approach can be taken for adjacent strings separated by newlines.

My processing script can be found [here](/media/SCTF25/deobfuscate.py). After running it, we get [more readable code](/media/SCTF25/clean.py), albeit with meaningless names.

Next, we rename some of the variables and function names to better understand what the code is doing. After some renaming, I got [this](/media/SCTF25/renamed.py).

Reading the renamed code seems to suggest that the script takes in user input, checks if it matches the password and decrypts the flag for us if it matches:

```python
def check_password(password):
  if password == 'happychance':
    return True
  else:
    print('That password is incorrect')
    sys.exit(0)
    return False

# ... code in between

flag_bytes_enc = read_flag_bytes()
user_input = get_user_input()
check_password(user_input)
display()
arg423 = arg111(flag_bytes_enc)
```

It appears that the password is `happychance`. To find the flag, we simply run the script in the same directory as _flag.txt.enc_ and enter `happychance` as the password.

## picoCTF 2023 - timer

### Description

You will find the flag after analysing this apk. Note that specifically for this challenge, the flag is wrapped in picoCTF{...}

Files Provided:

- [timer.apk](/media/SCTF25/timer.apk)

### Writeup

A `.apk` file is pretty much just a zip file, hence we start by unzipping the file with Linux CLI:

```bash
unzip timer.apk -d unzipped
```

Next, we check if our `picoCTF` wrapper exists in any of the unzipped files:

```bash
cd unzipped
grep -rw picoCTF .
```

From the output, it appears that a match for the `picoCTF` string was found in `classes3.dex`. We simply use `strings` and `grep` to retrieve it:

```bash
strings -t x classes3.dex | grep picoCTF
```
