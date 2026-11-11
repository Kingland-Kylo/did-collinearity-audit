The expression for the long-run effect printed in the right-hand column on page 46 (journal pagination) is

$$ \boxed{L=\frac{\beta_2-\beta_1}{1-\phi_1+\phi_2}.} $$

However, our examination of the error-correction model specified in the article shows that, provided the system converges and the control variables are held constant across the two paths, a permanent one-unit increase in democracy produces the following steady-state difference in democratic mood

$$ \boxed{L=-\frac{\beta_2}{\phi_1+\phi_2}.} $$

This formula error does not affect the subsequent results, since the published replication code generates Figures 5 and 6 through year-by-year recursion without calling the printed analytical expression. The expression itself nevertheless requires correction. The correct formula is derived below using recursion and differentiation.

The analysis considers the convergent case, in which both roots of the characteristic equation

$$ r^2-(1+\phi_1)r-\phi_2=0 $$

satisfy $|r|<1$.

# Deriving the Long-Run Multiplier

## 1. Recursive Derivation

Suppressing the country subscript, the author's model is

$$ \underbrace{m_t-m_{t-1}}_{\Delta m_t} =\alpha+\phi_1m_{t-1}+\phi_2m_{t-2} +\beta_1\underbrace{(d_t-d_{t-1})}_{\Delta d_t}+\beta_2d_{t-1} +\boldsymbol\gamma_1^\top(\mathbf x_t-\mathbf x_{t-1}) +\boldsymbol\gamma_2^\top\mathbf x_{t-1}+\varepsilon_t. $$

Here, $m_t$ is the level of support for democracy, and $d_t$ is the level of democracy. Consider two predicted paths for the same country. Along path $A$, democracy increases permanently by $\delta$ starting at $t=0$. Path $B$ is the baseline. The two paths share the same pre-shock history of democratic mood and the same control variables, and predictions are made for conditional means.

### 1.1 Subtracting the Two Equations

Define

$$ Q_t=m_t^A-m_t^B,\qquad s_t=d_t^A-d_t^B. $$

On the left-hand side, subtracting the annual change along path B from that along path A gives

$$ \begin{aligned} q_t &=(m_t^A-m_{t-1}^A)-(m_t^B-m_{t-1}^B)\\ &=(m_t^A-m_t^B)-(m_{t-1}^A-m_{t-1}^B)\\ &=Q_t-Q_{t-1}. \end{aligned} $$

On the right-hand side, the intercept and common control-variable terms cancel. The mood and democracy terms become

$$ \begin{aligned} m_{t-j}^A-m_{t-j}^B&=Q_{t-j},\\ (d_t^A-d_{t-1}^A)-(d_t^B-d_{t-1}^B)&=s_t-s_{t-1},\\ d_{t-1}^A-d_{t-1}^B&=s_{t-1}. \end{aligned} $$

Subtracting the two original equations therefore yields

$$ q_t=\phi_1Q_{t-1}+\phi_2Q_{t-2} +\beta_1(s_t-s_{t-1})+\beta_2s_{t-1}. \tag{1} $$

### 1.2 Substitution for the Shock Year and Subsequent Years

**In the shock year, $t=0$**, the democracy gap is $s_0=\delta$, while $s_{-1}=0$. The two mood paths coincide before the shock, so $Q_{-1}=Q_{-2}=0$. Substituting into equation (1) gives

$$ \begin{aligned} q_0 &=\phi_1\cdot0+\phi_2\cdot0+\beta_1(\delta-0)+\beta_2\cdot0\\ &=\beta_1\delta,\\ Q_0&=Q_{-1}+q_0=\beta_1\delta. \end{aligned} $$

**From $t=1$ onward**, both the current and previous years fall within the period after the permanent increase in democracy. Thus, $s_t=s_{t-1}=\delta$. Substituting into equation (1) gives

$$ q_t=\phi_1Q_{t-1}+\phi_2Q_{t-2}+\beta_2\delta. \tag{2} $$

Using $q_{t-1}=Q_{t-1}-Q_{t-2}$, or equivalently $Q_{t-2}=Q_{t-1}-q_{t-1}$, we obtain

$$ \begin{aligned} q_t &=\phi_1Q_{t-1}+\phi_2(Q_{t-1}-q_{t-1})+\beta_2\delta\\ &=-\phi_2q_{t-1}+(\phi_1+\phi_2)Q_{t-1}+\beta_2\delta. \end{aligned} $$

The two equations are therefore updated each year as follows

$$ \boxed{ \begin{aligned} q_t&=-\phi_2q_{t-1}+(\phi_1+\phi_2)Q_{t-1}+\beta_2\delta,\\ Q_t&=Q_{t-1}+q_t. \end{aligned}} \tag{3} $$

### 1.3 Solving for the Steady State

Suppose a finite steady state $(Q^\ast,q^\ast)$ exists. At that steady state, each quantity is the same in the current and previous years. Substituting into the second equation in (3) gives

$$ Q^\ast=Q^\ast+q^\ast \quad\Longrightarrow\quad q^\ast=0. $$

Substituting into the first equation in (3) then gives

$$ 0=-\phi_2\cdot0+(\phi_1+\phi_2)Q^\ast+\beta_2\delta. $$

If $\phi_1+\phi_2\ne0$, the solution is

$$ \boxed{ Q^\ast=-\frac{\beta_2\delta}{\phi_1+\phi_2},\qquad q^\ast=0. } $$

The **long-run effect** per unit of permanent change in democracy is therefore

$$ \boxed{L=\frac{Q^\ast}{\delta}=-\frac{\beta_2}{\phi_1+\phi_2}.} $$

## 2. Derivation by Differentiation

Once again, retain all terms and suppress the country subscript

$$ \Delta m_t =\alpha+\phi_1m_{t-1}+\phi_2m_{t-2} +\beta_1\Delta d_t+\beta_2d_{t-1} +\sum_k\gamma_{1k}\Delta x_{kt} +\sum_k\gamma_{2k}x_{k,t-1} +\varepsilon_t. $$

### 2.1 Solving for the Equilibrium

Suppose that, from some point onward, democracy is held at $d^\ast$ and the control variables at $x_k^\ast$. We seek the steady state of the predicted mean path and set the long-run mean of the disturbance under that prediction to zero. In what follows, $m_t$ continues to denote the model's predicted mean path. Hence

$$ m_t-m_{t-1} =\alpha+\phi_1m_{t-1}+\phi_2m_{t-2} +\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast. $$

Suppose the mean path eventually converges to a finite level $m^\ast$. Then

$$ m_t\to m^\ast,\qquad m_{t-1}\to m^\ast,\qquad m_{t-2}\to m^\ast. $$

It follows that

$$ 0=\alpha+(\phi_1+\phi_2)m^\ast +\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast. $$

For $\phi_1+\phi_2\ne0$, solving yields

$$ \boxed{ m^\ast(d^\ast,\mathbf x^\ast) =-\frac{\alpha+\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast} {\phi_1+\phi_2}. } $$

**The quantity $m^\ast$ is the equilibrium level of democratic mood.**

### 2.2 Taking the Partial Derivative

To obtain the long-run effect, hold the steady-state values of the control variables fixed and compare the equilibria at democracy levels $d^\ast$ and $d^\ast+\delta$. Subtracting term by term gives

$$ \begin{aligned} &m^\ast(d^\ast+\delta,\mathbf x^\ast)-m^\ast(d^\ast,\mathbf x^\ast)\\ &=-\frac{\alpha+\beta_2(d^\ast+\delta)+\sum_k\gamma_{2k}x_k^\ast} {\phi_1+\phi_2} +\frac{\alpha+\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast} {\phi_1+\phi_2}\\ &=-\frac{\beta_2\delta}{\phi_1+\phi_2}. \end{aligned} $$

The steady-state difference in democratic mood per unit of permanent change in democracy is therefore

$$ \boxed{ L= \frac{\partial m^\ast}{\partial d^\ast} =\lim_{\delta\to0} \frac{m^\ast(d^\ast+\delta,\mathbf x^\ast)-m^\ast(d^\ast,\mathbf x^\ast)}{\delta} =-\frac{\beta_2}{\phi_1+\phi_2}} $$

The intercept and control-variable terms cancel because they are identical across the two equilibria. **They determine the equilibrium level, while $\beta_2/[-(\phi_1+\phi_2)]$ determines the slope of the equilibrium relationship with democracy when the controls are held fixed.** The coefficient $\beta_1$ governs the response in the year democracy changes and influences the subsequent adjustment path. At the steady state, the annual change in democracy is zero, so this coefficient drops out of the slope.
