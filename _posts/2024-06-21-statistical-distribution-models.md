## Cool Statistical Distribution Models  
---
tags: stats
--- 

### Poisson's Distribution

#### Motivation
Say we have a radioactive decaying sample with some large number ($n = 5 \cdot10^{22}$) of particles. Each individual particle has an extremely small probability ($p = 4 \cdot 10^{-22}$) of decaying in the next $30$ minutes. Assuming the decay of particles are independent from each other, find the probability exactly $15$ particles have decayed after $30$ minutes.

##### Using The Binomial Distribution
Recalling the formula for the binomial distribution, we know that the probability of $X = r$ for a set of $n$ Bernoulli trials is given by 

$$
P(X = r) = \binom{n}{r}\cdot{p}^r{q}^{n-r}
$$

Now to calculate the probability that exactly $15$ particles have decayed after $30$ minutes, we substitute in the values, and replace $q$ with $1-p$.

$$
P(X = 15) = \binom{5\cdot10^{22}}{15}\cdot(4 \cdot 10^{-22})^{15}\cdot(1-4 \cdot 10^{-22})^{5\cdot10^{22}-15}
$$

Obviously, this is extremely expensive to calculate, considering the large magnitude of $5\;\cdot\;10^{22}\choose15$ and the high precision required to find $(1-4 \cdot 10^{-22})^{5\cdot10^{22}-15}$. Our regular scientific/graphing calculators would overflow for the first value, and output 1 (which is far off) for the second value.

#### Introducing Poisson's Distribution

For some binomial distribution $X\sim{B(n, p)}$, we let $np = \lambda$. If the following conditions hold

1. $n$ is large
2. $p$ is small

Then we can apply the formula $P(X = r) = e^{-\lambda}\cdot\frac{\lambda^{r}}{r!}$

#### Derivation 

We start off with the binomial distribution  

$$
(p + q)^n = q^n + {n}p q^{n - 1} + \frac{n(n - 1)}{2!} + \dots + \frac{n(n - 1)\dots(n - r + 1)}{r!}p^r q^{n-r} + \dots + p^n
$$

Using condition $(1)$ that $n$ is large, we can approximate the terms $n, (n-1), (n-2),\dots,(n-r)$ to be $n$ as $n\rightarrow\infty$. Doing so, we obtain  

$$
q^n + {n}pq^{n - 1} + \frac{n^2}{2!}{p^2}q^{n - 2} + \frac{n^3}{3!}{p^3}q^{n - 3} + \dots 
$$  

Using condition $(2)$ that $p$ is small (i.e. $p \rightarrow 0^+$), and the fact that $q = 1 - p$, we can also approximate $q \approx 1$. Doing so, we obtain  

$$
1 + {n}p + \frac{n^2}{2!}{p^2} + \frac{n^3}{3!}{p^3} + \frac{n^4}{4!}{p^4} + \dots
$$  

Note that under conditions $(1)$ and $(2)$, $p^n \rightarrow 0$, hence we can leave out the terms at the back. Rewriting the above formula, we get  

$$
1 + {np} + \frac{(np)^2}{2!} + \frac{(np)^3}{3!} + \frac{(np)^4}{4!} + \frac{(np)^5}{5!} + \dots
$$

Since $\lambda = np$, the above formula can be rewritten as 

$$
1 + {\lambda} + \frac{\lambda^2}{2!} + \frac{\lambda^3}{3!} + \frac{\lambda^4}{4!} + \frac{\lambda^5}{5!} +  \dots
$$

This summation happens to be the McLaurin expansion of $e^\lambda$. By the **Law Of Total Probability**, all probabilities must add up to 1. Hence, we divide all the terms by $e^\lambda$ for this to remain a valid probability distribution.  

$$
e^{-\lambda} + e^{-\lambda}{\lambda} + e^{-\lambda}\frac{\lambda^2}{2!} + e^{-\lambda}\frac{\lambda^3}{3!} + e^{-\lambda}\frac{\lambda^4}{4!} + e^{-\lambda}\frac{\lambda^5}{5!} + \dots
$$

We have shown that for some binomial distribution $X\sim{B(n, p)}$, under conditions $(1)$ and $(2)$,  

$$
\begin{align*}
P(X = r) &= \binom{n}{r}p^r(1-p)^{n-r} \\
&\approx e^{-\lambda}\frac{\lambda^r}{r!}
\end{align*}
$$