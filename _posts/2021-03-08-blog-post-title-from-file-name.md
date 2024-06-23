## Blog Post Title From First Header

Due to a plugin called `jekyll-titles-from-headings` which is supported by GitHub Pages by default. The above header (in the markdown file) will be automatically used as the pages title.

If the file does not start with a header, then the post title will be derived from the filename.

This is a sample blog post. You can talk about all sorts of fun things here.

---

### This is a header

#### Some T-SQL Code

```tsql
SELECT This, [Is], A, Code, Block -- Using SSMS style syntax highlighting
    , REVERSE('abc')
FROM dbo.SomeTable s
    CROSS JOIN dbo.OtherTable o;
```

#### Some PowerShell Code

```powershell
Write-Host "This is a powershell Code block";

# There are many other languages you can use, but the style has to be loaded first

ForEach ($thing in $things) {
    Write-Output "It highlights it using the GitHub style"
}
```
#### Some Mathjax I was trying out

Seperate Math Code Blocks Indented To Equal Sign 
$$
\begin{align*}
1 + 2x + x^2 &= 1 \cdot (1 + x) + x \cdot (1 + x) \\
&= (1 + x)^2 &&
\end{align*}
$$


De Morgan's Law:  
$\lnot({p}\land{q})\equiv\lnot{p}\lor\lnot{q}$  
$\lnot({p}\lor{q})\equiv\lnot{p}\land\lnot{q}$

Geometric Progression:  
$\sum\limits_{i=0}^{n}x^i=\frac{1-x^{n+1}}{1-x}$

Combination:  
$\sum\limits_{i=0}^{n}{n\choose{i}}=2^n$

Probability:  
$\sum\limits_{all\,x}{P(X = x)} = 1$