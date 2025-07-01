---
tags: Crypto
---

# SCTF 2025 Training Challs Writeups

## General remarks

I set a few of the training challenges for SCTF 2025. The challenges were intended to be as beginner-friendly as possible, to ensure accessibility even for those new to Crypto or CTFs in general.

Here are the challs I set and their writeups

1. [Baby RSA](#baby-rsa)

### Baby RSA

#### Description

RSA is a widely used public key cryptosystem. In this challenge, you will be given a public key and a ciphertext. Can you decrypt the ciphertext and find the flag?

Files provided:

- [values.txt](/media/SCTF25/values.txt)

#### Writeup

First, let's start by understanding how RSA works.

Let's say Alice wants to create a channel for Bob to send encrypted messages to her that no one else can read. She goes through this process:

##### Key Generaton (code sameple below)

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

##### Encryption (code sample below)

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

##### Decryption (code sample below)

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

You might ask, why does $ct^{d} \equiv pt \space (mod \space N)$ hold? To answer this, we need to take a look at [Euler's Theorem](https://en.wikipedia.org/wiki/Euler%27s_theorem) which tells us that for any 2 coprime integers $(a, n), $a ^{\phi (n)} \equiv 1 \space (mod \space n)$

Here, $gcd(pt, N) = 1$ holds (it holds for > 99.999% values of $pt$) too. The corollary is that $pt^{\phi (N)} \equiv 1 \space (mod N)$.

By choosing $d \equiv e^{-1} \space (mod \space \phi (N))$, we get $e \cdot d \equiv 1 \space (mod \space \phi (N)) \Rarr e \cdot d = k \cdot \phi (N) + 1, k \in \mathbb{Z}$

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

Now that we know how RSA works, let's retrieve the flag with the given values:

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
