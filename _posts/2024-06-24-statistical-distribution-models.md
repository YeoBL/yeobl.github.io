---
tags: stats
--- 

## Cool Statistical Distribution Models  

### Poisson's Distribution

#### Motivation
Say we have a radioactive decaying sample with some large number ($n = 5 \cdot10^{22}$) of particles. Each individual particle has an extremely small probability ($p = 4 \cdot 10^{-22}$) of decaying in the next $30$ minutes. Assuming the decay of particles are independent from each other, find the probability exactly $15$ particles have decayed after $30$ minutes.

##### Using The Binomial Distribution
Recalling the formula for the binomial distribution, we know that the probability of $X = r$ for a set of $n$ Bernoulli trials is given by 

$$
P(X = r) = {{n}\choose{r}}\cdot{p}^r{q}^{n-r}
$$

Now to calculate the probability that exactly $15$ particles have decayed after $30$ minutes, we substitute in the values, and replace $q$ with $1-p$.

$$
P(X = 15) = {{5\cdot10^{22}}\choose{15}}\cdot({4 \cdot 10^{-22})^{15}}\cdot(1-4 \cdot 10^{-22})^{5\cdot10^{22}-15}
$$

Obviously, this is extremely expensive to calculate, considering the large magnitude of $5\;\cdot\;10^{22}\choose15$ and the high precision required to find $(1-4 \cdot 10^{-22})^{5\cdot10^{22}-15}$. Our regular scientific/graphing calculators would overflow for the first value, and output 1 (which is far off) for the second value.

#### Introducing Poisson's Distribution

For some binomial distribution $X\sim{B(n, p)}$, we let $E(X) = \lambda$ (i.e. $np = \lambda$) if the following conditions hold

1. $n$ is large
2. $p$ is small

Then we can apply the formula  
$$
P(X = r) = e^{-\lambda}\frac{\lambda^{r}}{r!}
$$