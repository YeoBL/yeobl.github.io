---
tags: statistics
---

## Cool Statistical Distributions  

### Poisson Distribution

#### Motivation
Suppose we have a radioactive decaying sample with some large number ($n = 5 \cdot10^{22}$) of particles. Each individual particle has an extremely small probability ($p = 4 \cdot 10^{-22}$) of decaying in the next $30$ minutes. Assuming the decay of particles are independent from each other, find the probability exactly $15$ particles have decayed after $30$ minutes.

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
<summary> Derivation </summary>

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

<br/>

#### Testing It Out  

To evaluate the accuracy of the Poisson Distribution $P(n, p)$, we compare it against the Binomial Distribution $B(n, p)$. 

> Example: A hospital is testing out a few medical drugs, each with varying probabilities of side effects. The number of testers for each drug also varies, such that in each test, the expected number of testers suffering side effects is the same $(np=5)$. Find the probability that less than $3$ testers suffer side effects, when the sample sizes are $10, 20, 50, 100$ and $1000$ respectively. 

###### Note: I'm using MathJax arrays to make a table here and I have no idea how to center the $X\dots$ in the first row  

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
\begin{gather*}
E[X] = np \\
Var(X) = np(1 - p) \\
\end{gather*}
$$  

For the Poisson Distribution, as $p\rightarrow0$, we can take $1-p\approx1$. Hence, we have the following:

$$
\begin{gather*}
E[X] = np \\
Var(X) = np \\
\end{gather*}
$$

##### Conditions:  

1. **Independence:** Similar to the binomial distribution, the events in the Poisson Distribution must be independent of each other
2. **Constant mean:** $\lambda$ cannot have any variation
3. **Discrete values:** The distribution is only defined at non-negative integer values of occurences (e.g. concentration of saltwater)
4. **Bernoulli representation:** In each subinterval, each event can only happen at most once (i.e. it can be represented as many Benoulli trials)

### Chi-Squared $(\chi^2)$ Distribution  

#### Motivation  
Suppose we are in a casino and we want to determine if a roulette wheel is truly fair (i.e. equiprobability of all numbers). Obviously, the casino wouldn't let us inspect the roulette wheel. The best we could do would be to observe the wheel alot of times, then tabulate our results. If we observe the wheel 700 times, our table would look something like this

##### For simplicity, let's just assume the wheel only has the numbers 0 - 6 so the table isn't ridiculously big. 

$$
\begin{array} {|c|c|c|c|c|c|c|c|}
\hline Value & 0 & 1 & 2 & 3 & 4 & 5 & 6 \\ 
\hline Observed & 95 & 103 & 99 & 110 & 90 & 95 & 108 \\ 
\hline Expected & 100 & 100 & 100 & 100 & 100 & 100 & 100\\
\hline 
 \end{array}
$$

Due to the randomness of the wheel, we will almost always see some variation between the Observed and Expected values of each number appearing. This leaves us with the difficulty of figuring out whether the wheel is biased or not. How do we quantitatively test the hypothesis that the wheel is fair?

#### Introducing the Chi-Squared $(\chi^2)$ distribution

*Definition:* A Chi-Squared distribution with k-degrees of freedom is the distribution of a variable that is the sum of squares of k independent standard normal distributions $Z\sim{N}(0,1)$. Formally, the Chi-Squared distribution is defined as 

$$  
\sum\limits_{i=1}^{k}Z_i^2 \sim \chi^2(k)
$$  

##### Note: we denote the Chi-Squared distribution with $\chi^2(k)$.  

Here, "degrees of freedom" corresponds with the number of independent standard normal distributions. When we are conducting hypothesis testing later it will be used to refer to the number of variables that we can choose without any constraints.

We can try to imagine how $\chi^2(1)$ looks like based on the normal distribution. For $k\geq2$, I found it difficult to visualise, perhaps there are geniuses able to, but [here](https://en.wikipedia.org/wiki/File:Chi-square_pdf.svg)'s the probability density function and [here](https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Chi-square_cdf.svg/482px-Chi-square_cdf.svg.png)'s the cumulative density function.

#### Hypothesis testing

To quantitatively determine the randomness, we follow this procedure  
1. Form the null and alternative hypotheses
2. Tabulate the expected and observed frequencies
3. Check if any of the cells have expected values $<5$ or observed values $<1$. Combine these cellstogether to reduce the error of margin for the testing.
4. Calculate $X^2=\sum_{i=1}^{N} \frac{(E_i-O_i)^2}{E_i}$
5. Calculate the number of degrees of freedom with $k =$ number of values $-$ number of constraints $- 1$. We always $-1$ beacuse the total sum is fixed, which is in itself a constraint.
6. Choose either step 7 or 8
7. Use either G.C. or MF26 to find the critical value of our Chi-Squared distribution. If it exceeds our value of $X^2$, we reject the null hypothesis in favour of the alternative hypothesis. Otherwise, we do not reject the null hypothesis.
8. Use G.C. to calculate the p-value of our calculated $X^2$. If it is greater than our Level of Significance (LoS), we reject we reject the null hypothesis in favour of the alternative hypothesis. Otherwise, we do not reject the null hypothesis.

#### Worked Example (Roulette Wheel)

1. To test the hypothesis that the roulette wheel is fair, we need an alternative hypothesis, which will be that the roulette wheel is not fair
2. We observe the wheel 700 times, and tabulate our observations 
$$
\begin{array} {|c|c|c|c|c|c|c|c|}
\hline Value & 0 & 1 & 2 & 3 & 4 & 5 & 6 \\ 
\hline Observed & 95 & 103 & 99 & 110 & 90 & 95 & 108 \\ 
\hline Expected & 100 & 100 & 100 & 100 & 100 & 100 & 100\\
\hline 
 \end{array}
$$

3. All cells have expected values $\geq5$ and observed values $\geq1$, so there is no need to perform merging here

4. We calculate $X^2$ to use for testing later on

    $$
    \begin{align*}
    X^2 &= \sum\limits_{i=0}^{6}\frac{(O_i-E_i)^2}{E_i} \\
    &= \frac{(95-100)^2+(103-100)^2+\dots+(108-100)^2}{100} \\
    &= 3.24
    \end{align*}
    $$

5. Apart from the total sum adding up to 700, we have 0 other constraints on the observed value. Hence, we take the number of degrees of freedom , $v=7-0-1=6$

6. For demonstration purposes, we will use both steps 7 and 8. In actual testing, only one is needed. Our level of significance will be $LoS=0.05$

7. Referring to page 9 of MF26, when $v=5$ and $p=1-0.05=0.95$, our critical value $\chi^2_5(0.05)=11.07$. Since our $X^2$ value is under the critical value, it is not statistically signficiant and we do not reject the null hypothesis in favour of the alternative hypothesis

    ##### Note: $\chi^2_v(k)$ refers to the critical value for the Chi-Squared distribution with $v$ degrees of freedom at Level of Significance $k$

8. Using G.C. to calculate our p-value, we get $P(X^2\gt3.24)=0.337$. Since $0.337>0.05$, this result is not statistically significant and we do not reject the null hypothesis in favour of the alternative hyothesis.

We can also use the p-value for other distributions, such as the Poisson, Binomial and Negative Binomial Distribution. Below are more examples (To be added).

<details>
<summary>Poisson Distribution</summary>
</details>

<br/>

<details>
<summary>Binomial Distribution</summary>
</details>

<br/>

<details>
<summary>Negative Binomial Distribution</summary>
</details>
