---
tags: Crypto
---

## SSMCTF 2025 Crypto Writeup

### General remarks

This was my second time playing a CTF after studying the various Crypto techniques. The first was CDDC but regrettably, they didn't have much Crypto other than a relatively simple ECDSA chall entitled _Timeless MDS_. Overall, the crypto challs in this CTF were fairly interesting, and generally enjoyeable to work on. There were a total of 10 challenges, below are my ratings for each one:

1. [Tariff evaluation (68 solves)](#tariff-evaluation): 4/10
2. [Cauldron (26 solves)](#cauldron): 5/10
3. [BB84 2 (22 solves)](#bb84-2): 2/10
4. [Security Update (18 Solves)](#security-update): 7/10
5. [Triple Baka (9 solves)](#triple-baka): 8/10
6. [ECSSP (9 solves)](#ecssp): 7/10
7. Ice Kachang (4 solves): 7/10
8. Milk (3 solves): 7/10
9. STONKS (2 solves): 8/10
10. Change (0 solves): Did Not Solve

### Tariff Evaluation

#### Understanding The Challenge

We are provided with what looks like a simple RSA encryption [chall.py](/media/SSMCTF25/chall1.py).

Interestingly, we are given $n$ and $p - leak$. My first thought was to just run the code and find $leak$, use it to find $p$ which would solve the factorization problem.

Unfortunately, running it seems to take forever, and the line that calculates $leak$ is simply too convoluted for us to figure out what's going on.  

#### Factorizing $n$

ChatGPT conveniently gives us this explanation:
> Let:
> - **A**: the prime‑theorem factor  
>   $$A = \ln(n) - \frac{n}{\pi(n)} \quad\text{with } n = \text{factorial}(10000),$$  
>  refined so that \(A = 1\).
>
> - **B**: the moonshine factor  
>  $$B = 196884 - 196883 = 1.$$
>
> - **C**: the trigonometric identity  
>  $$C = \sin^2(1) + \cos^2(1) = 1.$$
>
> - **R**: the Riemann sum factor over \([-0.5, 0.5]\) of an odd function, giving  
>  $$R = 0.$$
>
> - **H**: the hash-based constant ratio, designed such that  
>  $$H = 1.$$
>
> - **G**: the golden ratio factor  
>  $$G = \phi^2 - \phi = 1,$$  
>  where \($\phi$) satisfies \($phi^2 - \phi - 1 = 0$).
>
> Then the value of `leak` is given by:
> $$
> \text{leak} = (A \cdot B \cdot C) + (R \cdot H \cdot G).
> $$
> 
> Substituting the values:
> $$
> \text{leak} = (1 \cdot 1 \cdot 1) + (0 \cdot 1 \cdot 1) = 1.
> $$

We check if leak is indeed $1$ by verifying that $p {\mid} n $:

```python
n = 1432796777893351...
p_min_leak = 1163296087009212...

leak = 1
p = p_min_leak + leak

print(n % p == 0)
# Outputs True
```

There we have it, we can easily find $q = \frac{n}{p}$ and we know that $n = p\cdot{q}$ so we can easily compute
$$\phi(n)=(p-1)\cdot(q-1)$$

#### Calculating $pt$

We have $ct = pt^{65537}\space(mod{\space}n)$, so all we need to do is find $x$ such that
$$ct^{x}{\space\equiv\space}pt\space(mod{\space}n)$$
$$pt^{65537\cdot{x}}{\space\equiv\space}pt{\space}(mod{\space}n)$$

By Euler's theorem, we know that since $pt$ and $n$ are coprime, 
$$pt^{\phi(n)}{\space\equiv\space}1\space(mod\space{n})$$

Hence, we observe that we want to choose $x$ s.t. 
$$65537{\cdot}x{\space\equiv\space}1\space(mod\space{\phi(n)})$$
$$x{\space\equiv\space}65537^{-1}\space(mod\space{\phi(n)})$$

We easily find such $x$ with python's built-in _pow_ function, and use _pycryptodome_'s _long_to_bytes_ function to retrieve the flag from the integer value of pt

```python
from Crypto.Util.number import long_to_bytes

leak = 1
n = 14327967778933513684866741755591664860009753335289842801500138776246927388908565045549036953515821363782360195603223134969430251873746384902650245859216942478227679940968216392374020987088032189979649651207466678612481243028925015679241748401963491207527485705180215317627141927757414725735045204253853660905080780363956413549452746600539875673613497721615180116534516152310881448965832037145076142117113964080856096271518220684895761507535874424951586089881169141701209499788164074440619615229101530812012074536366473358651533916950773961659249817974974369435476243005102815457927657745687933477253799476265131761443
p_min_leak = 116329608700921268219766270234310817804604851928199730711558466567902777993123659585400002712294671354175439631889219638125564836115230152964446576187727220004877191154015250469077590936104201390817315774241347283869619414516623651771211649835826869325694760344337757904706438096211760033894962243458863212410
ct = 4781314062204780803707083785029526695515373328754437058360148481983776761238818824513873915894272458596935350980408035233897241944785362251336400778024643919001797904298257118956520404524323559715746000068412954302542636386259106528078043580652880881897576074268512303671155030218729500291454403743708608548480977506269831895151273739405520980230118053504663654907891856282911532618045404860638219785802714538998317878998629883714243141387091669847359587414088871667047728752324989888015074594967676359710063823610770145417994477795587582507026793311537537265129227699483332016257848146975506362526106699486237406763

p = p_min_leak + leak
q = n // p
phi_n = (p - 1) * (q - 1)

e = 0x10001
d = pow(e, -1, phi_n)

pt = pow(ct, d, n)
pt_bytes = long_to_bytes(pt)

print(pt_bytes)
# Output: b'SSMCTF{This is a great time to get rich, richer than ever before!!! The markets are going to boom, the stock is going to boom!}'
```

### Cauldron

#### Understanding The Challenge

We are provided with 6 unknown functions, $C, B, R, S, X, O$ in [cauldron.py](/media/SSMCTF25/chall2.py).

Additionally, we are provided an [output.txt](/media/SSMCTF/output_chall2.txt) which was generated by

```python
text = "Double, double, toil and trouble. Fire burn and cauldron bubble!"
functions = [C, B, R, S, X, O]

output = open('output.txt', 'w')

for func1 in functions:
    for func2 in functions:
        for func3 in functions:
            output.write(func1(func2(func3(text))))
            output.write('\n')

for func in functions:
    flag = func(flag)

output.write(flag)
```

#### Initial Guesses

To start, we first take a look at the lines which had the same function applied to `text` 3 times.

```python 

# C(C(C(text)))
line1 = 'YwzA5ywzA5~5vy5wzC5[~z5w5vy5xvy5wwwz6'

# B(B(B(text)))
line44 = 'VWtjNU1WbHRlR3hNUTBKcllqTldhV0pIVlhOSlNGSjJZVmQzWjFsWE5XdEpTRko1WWpOV2FXSkhWWFZKUlZwd1kyMVZaMWx1Vm5saWFVSm9ZbTFSWjFreVJqRmlSMUo1WWpJMFoxbHVWbWxaYlhoc1NWRTlQUT09'

# R(R(R(text)))
line87 = '!elbbub nordluac dna nrub eriF .elbuort dna liot ,elbuod ,elbuoD'

# S(S(S(text)))
line130 = 'oDbuel ,odbuel ,otlia dnt orbuel .iFerb ru nna daclurdnob bulb!e'

# X(X(X(text))) - shortened
line173 = '205,207,201,211,206,...,207,202'

# O(O(O(text))) - truncated
line216 = 'ABCBCDCDEBCDCDEDEF...'
```

I initially guessed the following

- $B$: conversion to base64
- $R$: reversing the string
- $S$: swap adjacent characters e.g. `"123456"` $\rightarrow$ `"214365"`
- $X$: convert all characters to their ordering with `ord`, then concatenate with `','`

My guesses for $B$, $R$ and $S$ turned out to be correct, but $X$ was unfortunately wrong.

#### Figuring Out The Rest

Since $R^2(text) = text$, we can use $RRC(text)=C(text)$, $RRX(text)=X(text)$ and $RRO(text)=O(text)$ to more easily deduce what the remaining functions are.

Let's take a look at the relevant lines

```python
# R(R(C(text))) = C(text)
line85 = "Kv|isl3'kv|isl3'{vps'huk'{yv|isl5'Mpyl'i|yu'huk'jh|skyvu'i|iisl("

# R(R(X(text))) = X(text)
line89 = "187,144,138,157,147,154,211,223,155,144,138,157,147,154,211,223,139,144,150,147,223,158,145,155,223,139,141,144,138,157,147,154,209,223,185,150,141,154,223,157,138,141,145,223,158,145,155,223,156,158,138,147,155,141,144,145,223,157,138,157,157,147,154,222"

# R(R(O(text))) = O(text)
line90 = 'CDEnoptuvabcklmdef+,- !cdenoptuvabcklmdef+,- !stunophijklm !`abmnocde !stuqrsnoptuvabcklmdef-./ !EFGhijqrsdef !abctuvqrsmno !`abmnocde !bcd`abtuvklmcdeqrsnopmno !abctuvabcabcklmdef !"'
```

##### Note: $C(R(R(text))) = C(text)$ too, same for $X$ and $O$

For $C(text)$, we notice that it has the same length as $text$. Further, it appears that there is a consistent mapping between the characters (e.g. "o" $\rightarrow$ "v", "b" $\rightarrow$ "i", "l" $\rightarrow$ "s"). On further in spection, we notice that the distance between their ordering has a constant value of 7. 

```python
text = "Double, double, toil and trouble. Fire burn and cauldron bubble!"
line85 = "Kv|isl3'kv|isl3'{vps'huk'{yv|isl5'Mpyl'i|yu'huk'jh|skyvu'i|iisl("
for ch1, ch2 in zip(text, line85):
    print(ord(ch2) - ord(ch1), end = ' ')

# output: 7 7 7 7 ... 7 7
```

From this, we deduce that the function $C$ merely replaces each character, `ch`, with `chr(ord(ch) + 7)`

For $X(text)$, I compared my above guess with the actual output

```python
text = "Double, double, toil and trouble. Fire burn and cauldron bubble!"
print(','.join(map(str, map(ord, text))))
# output : 68,111,117,98,108,101,44,32,100,111,117,98,108,101,44,32,116,111,105,108,32,97,110,100,32,116,114,111,117,98,108,101,46,32,70,105,114,101,32,98,117,114,110,32,97,110,100,32,99,97,117,108,100,114,111,110,32,98,117,98,98,108,101,33
# line89 : 187,144,138,157,147,154,211,223,155,144,138,157,147,154,211,223,139,144,150,147,223,158,145,155,223,139,141,144,138,157,147,154,209,223,185,150,141,154,223,157,138,141,145,223,158,145,155,223,156,158,138,147,155,141,144,145,223,157,138,157,157,147,154,222
```

Comparing the both side by side, we notice that the $n$-th number in output and the $n$-th number in line89 add up to 255. My guess was somewhat close, I was just missing out the mapping of $x \rightarrow 255 - x$ prior to concatatenating the order numbers.

For $O(text)$, I noticed that its length was exactly 3 times that of $text$'s. Further, we note that if we split line90 into blocks of length 3 and take the middle element, we get $text$. 

```python
line90 = 'CDEnoptuvabcklmdef+,- !cdenoptuvabcklmdef+,- !stunophijklm !`abmnocde !stuqrsnoptuvabcklmdef-./ !EFGhijqrsdef !abctuvqrsmno !`abmnocde !bcd`abtuvklmcdeqrsnopmno !abctuvabcabcklmdef !"'
print(''.join(line90[i] for i in range(1, len(line90), 3)))
# Output is exactly the same as initial text
# If you are not getting the expected output, check that you are copying over the invisible characters too
```

We can find out what exactly $X$ does by noticing a pattern of the mappings ("D" $\rightarrow$ "CDE", "o" $\rightarrow$ "nop" and "u" $\rightarrow$ "tuv") but it is not necessary as we are only interested in finding its inverse to retrieve the flag.

#### Solving The Challenge

The rest is trivial, we simply implement the functions' inverse and apply them in the reverse order on the text in [output.txt](/media/SSMCTF/output_chall2.txt)'s line 217 to retrieve our flag.

My [solve script](/media/SSMCTF25/solve2.py)

### BB84 2

#### Understanding The Challenge

We are given this really large 3D-nested list in [convos.py](/media/SSMCTF25/convos.py), and a ciphertext in [ct.txt](/media/SSMCTF25/ct.txt). We are also told that the ciphertext was encrypted with AES, with the key/iv being exchanged via BB84.

#### Solving The Challenge

This challenge wasn't interesting, hence, as you might've noticed, I was not particularly zealous in describing my solution in a detailed manner. We first note that each 2D-nested list is of exactly size 4, with all 4 1D lists inside having the exact same length (but varying across different 2D-nested lists).

I applied the BB84 protocool to each of these 2D-nested lists, where you drop bits if different bases were used to measure them, and found that for each 2D-nested list, we would have 2 bitarrays of length exactly 128 remaining.

I just brute forced the ciphertext by considering each 128 bit as a candidate key/iv value for the AES decryption, and filtered out those that had the flag wrapper, 'SSMCTF' in them.

My [solve script](/media/SSMCTF25/solve3.py).

### Security Update

#### Understanding The Challenge

We are given some RSA encryption server code in [chall.py](/media/SSMCTF25/chall4.py). $N$ is a 512-bit pseudoprime (i.e. it is obtained by multiplying 2 256-bit primes together). This makes a factorization attack on $N$ not feasible.

```python
p, q = getPrime(256), getPrime(256)
N = p * q
```

At the start, our flag is encrypted with the parameter `e=3`, and we are provided with the values of $N$ and $ct=flag^e\space(mod\space{N})$.

We can try to solve a challenge where we attempt to derive the original value of $m$, a 22-byte number, from $c=m^e\space(mod\space{N})$. If we succeed, the server will "update" its security by setting `e=65537`.

```python
def update_security():
    global e
    e = 65537

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
```

#### Initial Attempt

I originally tried to solve this problem with RSA's [small e attack](https://ir0nstone.gitbook.io/crypto/rsa/public-exponent-attacks/small-e), to directly recover $flag$ from $ct$. However, I suppose the value of $flag$ was too large so I couldn't get a result after waiting for a couple of minutes. [Here](/media/SSMCTF25/solve4_1.py)'s the code from that attempt.

To use it, replace `N_challenge` and `c_challenge` with the values of $N$ and $ct$ respectively.

#### Cracking the challenge

Even though the above attack was not successful at retrieving $flag$, we could still use it to break the challenge as $m$ is a 22-byte/176-bit number. $m^3$ would have no more than 528 bits, which is not a lot more than $N$'s 512 bits.

Since $c=m^3\space(mod{\space}n)$, we can determine that $\sqrt[3]{c + kn}=m$, for some value of k. As $m^3$ has no more than 528 bits and $N$ has 512 bits, $k$ has at most 17 bits. If $k$ did have more than 17 bits, then $kn$ would have more than 528 bits. The limited range of $k$ makes for a computationally feasible search space of size $2^{17}=1.3e6$.

#### Retrieving $flag$

After cracking the challenge, we have 2 values of $ct$, encrypted with the same $N$. Let $ct_1=flag^{3}\space(mod{\space}n)$ and $ct_2=flag^{65537}\space(mod{\space}n)$. It is easily-verifiable that $gcd(3, 65537) = 1$, which we can abuse (I couldn't find a name for this attack).

Since $gcd(3, 65537) = 1$, we can find some $(a, b)$ pair such that $3a + 65537b = 1$ using the **extended** euclidean algorithm. One such solution is `a=21846` and `b=-1`. We solve for $flag$ with the following:

$$
\begin{align*}
ct_1^{21856} \cdot ct_2^{-1} &= {flag}^{3 \cdot 21856} \cdot {flag}^{65537 \cdot -1}&&\space(mod\space{N}) \\
        &= {flag}^{65538} \cdot {flag}^{-65537}&&\space(mod\space{N}) \\
        &= flag&&\space(mod\space{N})
\end{align*}
$$

[Here](/media/SSMCTF25/sol4_2.py) is my solve script, amend the values of $N$, $ct_1$ and $ct_2$ accordingly.

##### Note: sometimes $ct_2$ might not have an inverse under modulo $N$, since $N$ is not prime, causing this solution to fail. In that case, not having an inverse implies that $ct_2$ is not coprime to $N$, and we can use $gcd(ct_2, N)$ to find $p$ and factorize $N$. This would be an even bigger break that allows us to decrypt all messages encrypted with $N$

### Triple Baka

#### Understanding The Challenge

We are given [chall.py](/media/SSMCTF25//chall5.py), which defines a few mathy-looking functions `baka`, `hyperbaka` and `triple_baka`.

We are also provided with a Linear Congruence Generator (LCG) defined by:
$$
x_1=10275910798653121436396833379154598008161 \\
x_n = ax_{n-1}+b \space (mod \space m)
$$

$a, b, m$ are some constants unknown to us. Let $k=triplebaka(64)$ We are given $x_1, x_2, ... x_{9}$, and $ct=secret{\space\oplus\space}x_k$. Our goal is to retrieve $x_k$ so that we can calculate $secret=ct{\space\oplus\space}x_k$

#### Reverse-Engineering The LCG

We are given the values from $x_1$ to $x_9$ in [chall.py](/media/SSMCTF25//chall5.py). We first try to solve for $m$, as without it, it is not possible to find the values of $a$ and $b$.

To do so, we try to rewrite the equation into something of the form $x_n-x_{n-1}+x_{n+1}...\equiv0\space(mod{\space}m)$ so that the LHS is a multiple of $m$. We need to make sure the LHS is independent of $a$ and $b$, so that we know the actualy value of the LHS. If we can find enough LHS values that are multiples of $m$, we can take their gcd to find $m$.

First, let's get rid of the $b$ value.
$$
\begin{align*}
    & \space\space\space\space\space\space x_n \equiv ax_{n-1}+b \space && (mod \space m) \\
    & \Rightarrow x_{n+1} - x_n \equiv (ax_n+b) - (ax_{n-1}+b) && (mod \space m) \\
    & \Rightarrow x_{n+1} - x_n \equiv a(x_n-x_{n-1}) && (mod \space m) \\
\end{align*}
$$

Let $y_n=x_{n+1}-x_n$. From the above, we have $y_n\equiv{a}(x_n-x_{n-1})\space(mod \space m)$. In particular, we observe the following recurrence relation:

$$
\begin{align*}
    y_{n+1}&\equiv {a}(x_{n+1}-x_n) && (mod \space m) \\
    &\equiv a*y_n && (mod \space m) \\
\end{align*}
$$

Hence, we can see that
$$
\begin{align*}
    y_{n+2}*y_n&\equiv a*y_{n+1}*y_n && (mod \space m) \\
    &\equiv y_{n+1}*a*y_n && (mod \space m) \\
    &\equiv y_{n+1}*y_{n+1} && (mod \space m) \\
    &\equiv y_{n+1}^2 && (mod \space m) \\
\end{align*}
$$

Which gives us the following nice result:
$$
y_{n+2}*y_n-y_{n+1}^2\equiv0{\space}(mod \space m)
$$

Hence, for all values of $n$, $y_{n+2}*y_n-y_{n+1}^2$ is a multiple of $m$. We write a short python script to calculate the gcd across all values of $y_{n+2}*y_n-y_{n+1}^2$.

```python
from sage.all import * 
def gcd(a, b):
    return b if a == 0 else gcd(b % a , a)
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
print(f"{m = }")
print(f"{ZZ(m).is_prime() = }")

# Output: 
# m = 27071808322005969892390787400752803991921
# ZZ(m).is_prime() = True
```

Now, we solve for $a$ and $b$, which is relatively trivial now that we know $m$.

Solving for $a$:
$$
    y_{n+1} \equiv a * y_n\space(mod{\space}m) \\
    \Rightarrow a \equiv y_{n+1}*y_{n}^{-1}\space(mod{\space}m)
$$
Solving for $b$:
$$
    x_n \equiv ax_{n-1}+b \space (mod \space m) \\
    \Rightarrow b = x_n - ax_{n-1}  \space (mod \space m) 
$$

#### Finding The Value Of $triplebaka$

Let's analyse what each recursive function does:

```python
def baka(ba, ka):
    bakabaka = ba
    for bakabakabaka in range(ka-1):
        bakabaka = ba**bakabaka
    return bakabaka
```

This one's pretty straightforward, it's just tetration

$$
\mathrm{baka}(ba,\,ka)
=
  \underbrace{
    ba^{\,ba^{\,\cdots^{\,ba}}}
  }_{ka\text{ times}}
$$

In Knuth arrow notation, this is simply:

$$
baka(ba,ka)=ba \,\uparrow\uparrow\, ka
$$

Now we get to the recursive functions:

```python
def hyperbaka(ba, ka, bakabaka):
    if bakabaka == 1:
        return ba**ka
    elif ka == 0:
        return 1
    elif bakabaka == 2 and ba == ka:
        return baka(ba, bakabaka)
    else:
        bakabakabaka = hyperbaka(ba, ka-1, bakabaka)
        return hyperbaka(ba, bakabakabaka, bakabaka-1)
```

This starts to get a bit messy, I just asked ChatGPT and it told me that `hyperbaka` was just the h-th order hyper operation on b and k
$$
\mathrm{hyperbaka}(b,k,h)\;=\;b\,\uparrow^{\,h}\,k
$$

The last, and final function is `triplebaka`

```python
def triple_baka(n):
    if n == 1:
        return hyperbaka(3, 3, 4)
    else:
        return hyperbaka(3, 3, triple_baka(n-1))
```

I asked ChatGPT again and it gave me this

$$
T_1 \;=\;\mathrm{hyperbaka}(3,3,4)  = 3 \;\uparrow^4\;3 \\
T_n =\mathrm{hyperbaka}\bigl(3,3,T_{n-1}\bigr) =3\;\uparrow^{\,T_{n-1}}\;3
$$

Well now $triplebaka=T_{64}$ looks like a really huge number, making it computationally unfeasible for us to calculate x_{triplebaka}. Fortunately since this LCG has a cyclic order of $m - 1$, we just need to find $triplebaka \space mod \space (m-1)$

$triplebaka$, when expanded, looks something like this:

$$
\mathrm{triplebaka}
=
  \underbrace{
    3^{\,3^{\,\cdots^{\,3}}}
  }_{\text{a lot of times}}
$$

Since we only want to find $triplebaka (mod{\space}(m - 1))$, we can apply Fermat's last theorem here:

$$
\begin{align*}
triplebaka &= 3 ^ {3 ^ {3 ^ {... 3}}} (mod{\space}(m - 1)) \\
        &= 3 ^ {3 ^ {3 ^ {... 3}} (mod{\space}{\phi}(m - 1))} \\
        &= 3 ^ {3 ^ {3 ^ {... 3} (mod{\space}{\phi}(\phi(m - 1)))}} \\
\end{align*}
$$

Since $phi(m) \leq m$, where equality holds i.f.f $m=1$, eventually $phi(phi(...phi(m - 1)))$ reduces to $1$, which simplifies our calculations. Now we just have to find the point where $phi(phi(...phi(m - 1)))=1$, and from there we can backtrack and calculate $triplebaka (mod{\space}(m - 1))$.

#### Solving For Flag

Finally, we use the closed form for LCGs:
$$
x_{N} = (a^N * x_0 + b*(a^N - 1)*(a-1)^{-1}))\space(mod{\space}m)
$$

My complete solve script can be found [here](/media/SSMCTF25/sol5.py).

### ECSSP

#### Understanding The Challenge

We are given [chall.py](/media/SSMCTF25/chall6.py) that encrypts our flag with some special Elliptic Curve algorithm.

```python
A = [E.random_point() for _ in range(42)]
enc = []

m = bin(bytes_to_long(flag))[2:]
m = m.zfill(len(m)//42*42+42)

for i in range(0,len(m),42):
    buffer = None
    for j, bit in enumerate(m[i:i+42]):
        if bit == '1':
            if not buffer:
                buffer = A[j]
            else:
                buffer += A[j]
    enc.append(buffer)
```

$42$ random points on the curve $E$ are chosen and stored in the list $A$. Our flag is converted to a bitarrray and padded to a length that is a multiple of 42. Each 42-bit chunk is then encoded into a point by using the 42 points in A as a basis.

We are given the 42 points in A alongside the encoded points in [output.txt](/media/SSMCTF25/output_chall6.txt). Our goal is to recover the original bitarray and convert it back into our flag.

#### 0-1 Knapsack

This problem is equivalent to having a 0-1 knapsack, where we are tasked with finding the specific combination of items that give us a particular sum. The idea behind our solution is rather similarly to [this problem](https://codebreaker.xyz/problem/harddisk).

#### Naive Solution

Let $k$ be the number of items we have in our knapsack. We can attempt to create a hash table mapping all possible points to the items that sum up to them. Our hash table would have a size of up to $O(2^k)$. For $k=42$ though, this is unfortunately not computationally feasible.

#### Meet In The Middle

Instead of generating all $2^k$ possible points, we can instead split our $k$ items into two halves, `left` and `right`, each of size $\frac{k}{2}$. For both `left` and `right`, we create a hash table mapping all possible points to the subset of the items in each half that sums up to them.

Now, each hash table will have size of up to $O(2^{\frac{k}{2}})$. For $k=42$, this is approximately $2e6$. To find the subset of the 42 items that sum up to a particular ppoint $P$, we simply iterate through all points, $Q$, in `left`, then check if $P - Q$ exists in `right`.

If it does, then we find the subset of items in `left` that sum up to $Q$, and the subset of items in `right` that sum up to $P - Q$, and join them together to find our answer. Assuming an upper-bound hash-map lookup time of $O(log{\space}n)$ (to account for collisions), our lookup time becomes $O(2^{\frac{k}{2}}{\cdot}log(2^\frac{k}{2}))=O(2^{\frac{k}{2}}{\cdot}k)$, which is much faster than our naive solution of $O(2^k)$. For $k=42$, $O(2^{\frac{k}{2}}{\cdot}k)$ is very much computationally feasible.

My solve script can be found [here](/media/SSMCTF25/sol6.py).

