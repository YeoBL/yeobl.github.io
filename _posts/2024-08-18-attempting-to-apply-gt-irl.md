---
tags: math
---

## Game Theory In Real Life Decision Making  

### Motivation

In Game Theory sense, a game can be defined as such

> A set of circiumstances where two or more players making choices, creating a result that affects all players  

Notice how a corollary is that those mobile 1-player games don't count. In the army, I often find myself playing "games" with varying number of players, with my buddy, my section or even my whole platoon, where each player's decisions affect every other player. I thought it'd be interesting to think about what Game Theory says when making optimal decisions.  

### Prisoner's Dilemma

The Prisoner's Dilemma can be summarised as follows:  

Players A and B were both taken into custody for commiting a robbery. The police don't really have evidence that they were the ones who commited the robbery, and are relying on both players ratting each other out to convict them, which both A and B are well aware of. Both players have two choices here, to deny ($D$) involvement completely or to snitch ($S$). Both will have to make their decisions simultaneously, without knowledge of the other players' choice or strategy.  

The (collectively) best case scenario is where both players choose $D$, and they each get a year in jail. If one player chooses $D$ while the other chooses $S$, the player who denied gets 5 years in jail, while the other gets none. In the (collectively) worst case, both players choose $S$, and each get 4 years worth in jail.  

Naturally, each player would like to spend as little time in jail as possible, making their happiness negatively correlated to the years they spend in jail. We define each player's utility as $s=5-x$, where $x$ is the numbers of years they spend in jail. The payoff table would look like this.  

##### Note: Payoff refers to the value of utility a player receieves from a particular result of the game

$$
\begin{array} {|c|c|c|}
\hline \enspace{A}\backslash{B}\enspace & S & D \\  
\hline S & \enspace1,1\enspace & \enspace5, 0\enspace \\  
\hline D & 0, 5 & 4,4 \\  
\hline  
\end{array}
$$

The most important property of the Prisoner's Dilemma game is that each player's individual optimal choice interestingly leads to the collectively worse outcome. Assume player B decides to play $S$. Player A's payoff would be $1$ and $0$ if he played $S$ and $D$ respectively. If player B plays $D$ instead, the payoffs for player A would be $5$ and $4$ if he played $S$ and $D$ respectively.  

It appears that regardless of what player B plays, player A's utility would be $1$ more by playing $S$ over $D$. Vice versa for player B. However, when both players play $S$, it leads to a payoff of $(1, 1)$, a much worse outcome than $(4, 4)$ achieved by both players playing $D$. Hence, if we were to play this game one-off, we would expect both rational players to choose $S$, leading to the collectively worse outcome.  

The Prisoner's Dilemma is aplenty in real life scenarios too. For instance, during area cleaning in army, one person could be allocated to clean the toilet while another might be tasked to clean the laundry area. Both players have a choice between dilligently cleaning ($D$) and slacking ($S$). Below are the possible outcomes:  

1. Both players choose $D$. The area is clean and everyone gets to go home happily. (Collective best outcome)  
2. Both players choose $S$. In which case, the entire area is dirty and nobody is happy. (Collective worst outcome)
3. One player chooses $D$, while the other chooses $S$. The slacker gets to enjoy partially clean living quarters despite doing nothing. Meanwhile, the other player has to settle for a partially clean place despite having held his end of the job. (Best payoff for one player, worst for another)

##### Note: This is a very simplified game with only two players, for easy analysing purposes

As with all Prisoner's Dilemma games, if this were a one-off game all rational players would simply choose $S$. Regardless of what the other player chooses, the payoff for $D$ is always lower than that of $S$.

#### Infinite Games

Infinite games don't really have a commonly agreed upon definition. In this post I'll just call any game that could theoretically go on infinitely an "infinite" game. For instance, a game where two players take turns rolling a dice, and the first player to roll a $1$ wins would be an infinite game, even though it's expected to end in $6$ turns.  

Back to the prisoner's dilemma, let's consider how the game would be played if it was repeated infinitely, with each player having full knowledge of the historical choices made.  

Now, both players have to consider how their current choice would affect the game in the future. A player may use the **grim trigger** following strategy to provide the greatest incentive for the other player to always cooperate and choose $D$.  

> Always choose $D$, and switch to $S$ permanently if at any point the previous game ended with something other than $(D,D)$.  

By never switching back to $D$ after a betrayal, this strategy maximises the penalty for choosing $S$ and encourages both players to stick to $D$ as much as possible.

To determine if both players will actually stick to $(D,D)$, we use the one-shot deviation principle. In straightforward terms it states that, if at every point, no player can increase their payoff by deviating from their strategy exactly once, then the set of strategies is feasible (i.e. both players' strategies are the best responses of each other).  

Before that, we need to introduce a new variable, $\beta$, which will be the discount factor. The idea is that the same amount of payoff is worth more in the present than in future turns. Hence, a payoff of $1$ in the $x$ turns later would be worth $\beta^x$ in the present turn, where $\beta<1$.  

Assuming both players stick to the grim trigger strategy,  

- $(D,D)$ will always be played.  
- Their payoffs would be $(4,4),(4,4),(4,4)\ldots$

The payoff for both players sticking to the strategy in discounted utility terms would be

$$
\begin{align*}
4 + 4\beta + 4\beta^2 + \ldots &= 4\cdot\sum\limits_{i=0}^{\infin}\beta^i \\
&= \frac{4}{1-\beta}\\
\end{align*}
$$  

If a player deviates from the strategy, by choosing $D$ at one point,  

- The outcome path would be: $(S,D), (S,S), (S,S), \ldots$  
- Their payoffs would be $(5,0),(1,1),(1,1),\ldots$

The payoff for the player who deviated in discounted utility terms would be  

$$
\begin{align*}
5 + \beta + \beta^2 + \beta^3 + \ldots &= 5 + \sum\limits_{i=1}^{\infin}\beta^i \\
&= 5 + \frac{\beta}{1-\beta}\\
\end{align*}
$$  

For deviating to not be profitable,  

$$
\frac{4}{1-\beta} \geq 5 + \frac{\beta}{1-\beta}  \\
4 \geq 5\cdot(1-\beta)+\beta \\
4 \geq 5 - 5\beta+\beta \\  
4\beta \geq 1 \\  
\beta \geq \frac{1}{4}
$$  

That's it, we've shown that both players playing the grim trigger strategy is feasible if and only if $\beta\geq\frac{1}{4}$ for both players. Of course, in real life scenarios the payoff tables will differ, hence the minimum value of $\beta$ for both players to cooperate would also be different.

#### Finite Games

Finite games on the other hand, are games where there is a fixed end, and always ends in a finite number of moves. Most real life repeated games tend to be finite. For instance, in the area cleaning game, at some (known) point, everyone moves out and the game ends.  

Intuitively, we would expect that for some sufficiently large $\beta$, the grim trigger strategy is feasible for both players. 