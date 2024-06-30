---
tags: statistics
---

## Cool Statistical Distributions  

### Poisson Distribution

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

Obviously, this is extremely computationally expensive to calculate, considering the large magnitude of $5\;\cdot\;10^{22}\choose15$ and the high precision required to find $(1-4 \cdot 10^{-22})^{5\cdot10^{22}-15}$. Our regular scientific/graphing calculators would overflow for the first value, and output 1 (which is far off) for the second value.

#### Introducing Poisson's Distribution

For some binomial distribution $X\sim{B(n, p)}$, we let $np = \lambda$. If the following conditions hold

1. $n$ is large
2. $p$ is small

Then we can apply the formula $P(X = r) = e^{-\lambda}\cdot\frac{\lambda^{r}}{r!}$

<details>
<summary> **Derivation** </summary>

We start off with the binomial distribution  

$$
(p + q)^n = q^n + {n}p q^{n - 1} + \frac{n(n - 1)}{2!}p^2 q^{n - 2} + \dots + \frac{n(n - 1)\dots(n - r + 1)}{r!}p^r q^{n-r} + \dots + p^n
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
e^{-\lambda} + e^{-\lambda}\cdot{\lambda} + e^{-\lambda}\cdot\frac{\lambda^2}{2!} + e^{-\lambda}\cdot\frac{\lambda^3}{3!} + e^{-\lambda}\cdot\frac{\lambda^4}{4!} + e^{-\lambda}\cdot\frac{\lambda^5}{5!} + \dots
$$

We have shown that for some binomial distribution $X\sim{B(n, p)}$, under conditions $(1)$ and $(2)$,  

$$
\begin{align*}
P(X = r) &= \binom{n}{r}\cdot{p}^r(1-p)^{n-r} \\
&\approx e^{-\lambda}\cdot\frac{\lambda^r}{r!}
\end{align*}
$$
</details>


#### Testing It Out  

To evaluate the accuracy of the Poisson Distribution $P(n, p)$, we compare it against the Binomial Distribution $B(n, p)$. 

> Example: A hospital is testing out a few medical drugs, each with varying probabilities of side effects. The number of testers for each drug also varies, such that in each test, the expected number of testers suffering side effects is the same $(np=5)$. Find the probability that less than $3$ testers suffer side effects, when the sample sizes are $10, 20, 50, 100$ and $1000$ respectively. 

###### Note: I'm using MathJax arrays to make a table here and I have no idea how to center the X\dots$ in the first row  

$$
\begin{array} {|c|c|cc|cc|cc|cc|}\hline n & p & X=0 & & X=1 &  & X=2 &  & X\lt3 &  \\ \hline  &  & P & B & P & B & P & B & P & B \\ \hline 10 & 0.500 & 0.007 & 0.001 & 0.034 & 0.010 & 0.084 & 0.044 & 0.125 & 0.055 \\ \hline 20 & 0.250 & 0.007 & 0.003 & 0.034 & 0.021 & 0.084 & 0.067 & 0.125 & 0.091 \\ \hline 50 & 0.100 & 0.007 & 0.005 & 0.034 & 0.029 & 0.084 & 0.078 & 0.125 & 0.112 \\ \hline 100 & 0.050 & 0.007 & 0.006 & 0.034 & 0.031 & 0.084 & 0.081 & 0.125 & 0.118 \\ \hline 1000 & 0.005 & 0.007 & 0.007 & 0.034 & 0.033 & 0.084 & 0.084 & 0.125 & 0.124 \\ \hline  \end{array}
$$

From the above table, we notice that as $n$ increases and $p$ decreases, the Poisson Distribution gives an increasingly acurate estimate of the Binomial Distribution. At $n = 1000$ and $p = 0.005$, the probabilities of the Poisson Distribution are almost identical to that of the Binomial's.  

#### Properties of the Poisson Distribution  

##### Recurrence Relation:

$$
P(X = r) = \frac{\lambda}{r} \cdot P(X = r - 1) 
$$  

By comparing the ratios of $\frac{P(X=r)}{P(X=r-1)}$, we note that for $r \lt \lambda$, $P(X = r)$ is increasing (since $\frac{\lambda}{r} \gt 1$) and for $r \gt \lambda$, $P(X = r)$ is decreasing (since $\frac{\lambda}{r} \lt1$). We can use this to find the mode of the distribution, which occurs when $r$ is equal to the integer part of $\lambda$ (i.e. $\lfloor{\lambda}\rfloor$). Proof: do some casework for both $r \gt \lambda$ and $r \lt \lambda$.

Special case: if $\lambda \in \mathbb{R}$, then it is possible that $\lambda=r$. In this case, the distribution will have $2$ modes, $\lambda$ and $\lambda + 1$.  

##### Expected Value and Variance:  

In the binomial distribution, we have:

$$
E[X] = np \\
Var(X) = np(1 - p) \\
$$  

For the Poisson Distribution, as $p\rightarrow0$, we can take $1-p\approx1$. Hence, we have the following:

$$
E[X] = np \\
Var(X) = np \\
$$

##### Conditions:  

1. **Independence:** Similar to the binomial distribution, the events in the Poisson Distribution must be independent of each other
2. **Constant mean:** $\lambda$ cannot have any variation
3. **Discrete values:** The distribution is only defined at non-negative integer values of occurences (e.g. concentration of saltwater)
4. **Bernoulli representation:** In each subinterval, each event can only happen at most once (i.e. it can be represented as many Benoulli trials)