---
tags: Crypto
---

## SSMCTF 2025 Crypto Writeup

### General remarks
This was my second time playing a CTF after studying the various Crypto techniques. The first was CDDC but regrettably, they didn't have much Crypto other than a relatively simple ECDSA chall entitled _Timeless MDS_. Overall, the crypto challs in this CTF were fairly interesting, and generally enjoyeable to work on. There were a total of 10 challenges, below are my ratings for each one:

1. [Tariff evaluation](#tariff-evaluation) (68 solves): 4/10
2. Cauldron (26 solves): 6/10
3. BB84 2 (22 solves): 2/10
4. Security Update (18 Solves): 7/10
5. Triple Baka (9 solves): 6/10
6. ECSSP (9 solves): 8/10
7. Ice Kachang (4 solves): 8/10
8. Milk (3 solves): 7/10
9. STONKS (2 solves): 8/10
10. Change (0 solves): Did Not Solve

### Tariff Evaluation

#### Factorizing n
We are provided with what looks like a simple RSA encryption [chall.py](/media/SSMTF25/chall1.py).

Interestingly, we are given $n$ and $p - leak$. My first thought was to just run the code and find $leak$, use it to find $p$ which would solve the factorization problem.

Unfortunately, running it seems to take forever, and the line that calculates $leak$ is simply too caonvoluted for us to figure out what's going on.  

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
>  where \(\phi\) satisfies \(\phi^2 - \phi - 1 = 0\).
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

We check if leak is indeed by verifying that $p|n$. 

```python
n = 1432796777893351...
p_min_leak = 1163296087009212...

leak = 1
p = p_min_leak + leak

print(n % p == 0)
# Outputs True
```

There we have it, since we know that $n = p\cdot{q}$ now we can easily compute 
$$\phi(n)=(p-1)\cdot(q-1)$$

We have $ct = pt^{65537}\space(mod{\space}n)$, so all we need to do is find $x$ such that 
$$ct^{x}{\space\equiv\space}pt\space(mod{\space}n)$$
$$pt^{65537\cdot{x}}{\space\equiv\space}pt{\space}(mod{\space}n)$$

By Euler's theorem, we know that since $pt$ and $n$ are coprime, 
$$pt^{\phi(n)}{\space\equiv\space}1\space(mod\space{n})$$

Hence, we observe that we want to choose $x$ s.t. 
$$65537{\cdot}x{\space\equiv\space}1\space(mod\space{n})$$

We easily find such $x$ with python's _pow_ function, and use _pycryptodome_'s long_to_bytes function to retrieve the flag from the integer value of pt

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
