文章第46页（期刊页码）右栏所写长期效应为：
$$ \boxed{L=\frac{\beta_2-\beta_1}{1-\phi_1+\phi_2}.} $$
但据我们考证，按正文所列误差修正模型，在系统收敛、控制变量保持相同的条件下，民主程度永久提高一个单位所产生的稳态民主情绪差应为：
$$ \boxed{L=-\frac{\beta_2}{\phi_1+\phi_2}.} $$
虽然这并不影响后续结果，因为原文公开复现代码通过逐年递推计算图 5、图 6，没有调用正文印出的这条解析公式，但它毕竟是一个错误。以下分别用递推法和求导法推导正确公式。

本文讨论收敛情形，即特征方程
$$ r^2-(1+\phi_1)r-\phi_2=0 $$
的两个根均满足 $|r|<1$。

# 推导长期乘数

## 1. 递推式

省略国家下标，作者的模型是：
$$ \underbrace{m_t-m_{t-1}}_{\Delta m_t} =\alpha+\phi_1m_{t-1}+\phi_2m_{t-2} +\beta_1\underbrace{(d_t-d_{t-1})}_{\Delta d_t}+\beta_2d_{t-1} +\boldsymbol\gamma_1^\top(\mathbf x_t-\mathbf x_{t-1}) +\boldsymbol\gamma_2^\top\mathbf x_{t-1}+\varepsilon_t. $$
其中 $m_t$ 是民主支持水平，$d_t$ 是民主制度水平。比较同一个国家的两条预测路径。$A$ 路径从 $t=0$ 起把民主程度永久提高 $\delta$，$B$ 是基准路径。两条路径在冲击前有相同的民意历史，使用相同控制变量，并按条件均值预测。

### 1.1 将两条方程相减
定义
$$ Q_t=m_t^A-m_t^B,\qquad s_t=d_t^A-d_t^B. $$
左边是两条路径各自的年度变化再相减：
$$ \begin{aligned} q_t &=(m_t^A-m_{t-1}^A)-(m_t^B-m_{t-1}^B)\\ &=(m_t^A-m_t^B)-(m_{t-1}^A-m_{t-1}^B)\\ &=Q_t-Q_{t-1}. \end{aligned} $$
右边的截距和共同控制变量抵消。民意项和制度项分别变成
$$ \begin{aligned} m_{t-j}^A-m_{t-j}^B&=Q_{t-j},\\ (d_t^A-d_{t-1}^A)-(d_t^B-d_{t-1}^B)&=s_t-s_{t-1},\\ d_{t-1}^A-d_{t-1}^B&=s_{t-1}. \end{aligned} $$
因此，两条原方程相减后得到
$$ q_t=\phi_1Q_{t-1}+\phi_2Q_{t-2} +\beta_1(s_t-s_{t-1})+\beta_2s_{t-1}. \tag{1} $$

### 1.2 分别代入冲击当年和之后的年份
**冲击当年 $t=0$**，有冲击 $s_0=\delta$、$s_{-1}=0$，而且冲击前两条民意路径相同，所以 $Q_{-1}=Q_{-2}=0$。代入式（1）：
$$ \begin{aligned} q_0 &=\phi_1\cdot0+\phi_2\cdot0+\beta_1(\delta-0)+\beta_2\cdot0\\ &=\beta_1\delta,\\ Q_0&=Q_{-1}+q_0=\beta_1\delta. \end{aligned} $$
**从 $t=1$ 起**，当年和上一年都已经处于民主程度提高后的时期。所以 $s_t=s_{t-1}=\delta$，代入式（1）：
$$ q_t=\phi_1Q_{t-1}+\phi_2Q_{t-2}+\beta_2\delta. \tag{2} $$
再用 $q_{t-1}=Q_{t-1}-Q_{t-2}$，即 $Q_{t-2}=Q_{t-1}-q_{t-1}$，得到：
$$ \begin{aligned} q_t &=\phi_1Q_{t-1}+\phi_2(Q_{t-1}-q_{t-1})+\beta_2\delta\\ &=-\phi_2q_{t-1}+(\phi_1+\phi_2)Q_{t-1}+\beta_2\delta. \end{aligned} $$
于是，每年更新两条方程：
$$ \boxed{ \begin{aligned} q_t&=-\phi_2q_{t-1}+(\phi_1+\phi_2)Q_{t-1}+\beta_2\delta,\\ Q_t&=Q_{t-1}+q_t. \end{aligned}} \tag{3} $$

### 1.3 求稳态
假设有一个有限稳态 $(Q^\ast,q^\ast)$。到了稳态，今年和去年的这两个量分别相同。先代入式（3）的第二条：
$$ Q^\ast=Q^\ast+q^\ast \quad\Longrightarrow\quad q^\ast=0. $$
再代入式（3）第一条：
$$ 0=-\phi_2\cdot0+(\phi_1+\phi_2)Q^\ast+\beta_2\delta. $$
如果 $\phi_1+\phi_2\ne0$，解得
$$ \boxed{ Q^\ast=-\frac{\beta_2\delta}{\phi_1+\phi_2},\qquad q^\ast=0. } $$
因此，每单位永久制度变化对应的**长期效应**是
$$ \boxed{L=\frac{Q^\ast}{\delta}=-\frac{\beta_2}{\phi_1+\phi_2}.} $$

## 2. 求导法

依旧先保留全部项，省略国家下标：
$$ \Delta m_t =\alpha+\phi_1m_{t-1}+\phi_2m_{t-2} +\beta_1\Delta d_t+\beta_2d_{t-1} +\sum_k\gamma_{1k}\Delta x_{kt} +\sum_k\gamma_{2k}x_{k,t-1} +\varepsilon_t. $$

### 2.1 求均衡
设从某个时点起，制度水平固定为 $d^\ast$，控制变量固定为 $x_k^\ast$，对模型预测的均值路径求稳态，并令该预测下扰动的长期均值为零。以下仍用 $m_t$ 表示模型预测的均值路径，所以：
$$ m_t-m_{t-1} =\alpha+\phi_1m_{t-1}+\phi_2m_{t-2} +\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast. $$
假设均值路径最终收敛到一个有限水平 $m^\ast$，那么
$$ m_t\to m^\ast,\qquad m_{t-1}\to m^\ast,\qquad m_{t-2}\to m^\ast. $$
所以：
$$ 0=\alpha+(\phi_1+\phi_2)m^\ast +\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast. $$
当 $\phi_1+\phi_2\ne0$，解出
$$ \boxed{ m^\ast(d^\ast,\mathbf x^\ast) =-\frac{\alpha+\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast} {\phi_1+\phi_2}. } $$
**这个 $m^\ast$ 就是均衡民主情绪。**

### 2.2 求偏导
接着看长期效应，保持控制变量的稳态水平相同，比较制度水平为 $d^\ast$ 和 $d^\ast+\delta$ 的两个均衡，逐项相减：
$$ \begin{aligned} &m^\ast(d^\ast+\delta,\mathbf x^\ast)-m^\ast(d^\ast,\mathbf x^\ast)\\ &=-\frac{\alpha+\beta_2(d^\ast+\delta)+\sum_k\gamma_{2k}x_k^\ast} {\phi_1+\phi_2} +\frac{\alpha+\beta_2d^\ast+\sum_k\gamma_{2k}x_k^\ast} {\phi_1+\phi_2}\\ &=-\frac{\beta_2\delta}{\phi_1+\phi_2}. \end{aligned} $$
因此，每单位永久制度变化对应的稳态民意差为
$$ \boxed{ L= \frac{\partial m^\ast}{\partial d^\ast} =\lim_{\delta\to0} \frac{m^\ast(d^\ast+\delta,\mathbf x^\ast)-m^\ast(d^\ast,\mathbf x^\ast)}{\delta} =-\frac{\beta_2}{\phi_1+\phi_2}} $$
截距和控制变量在这一步抵消，是因为两个均衡共用这些量。**它们决定均衡水平的位置，$\beta_2/[-(\phi_1+\phi_2)]$ 决定在控制变量固定时，均衡水平随制度改变的斜率。** $\beta_1$ 则控制制度变化发生当年的反应，并影响随后走向稳态的路径。到达稳态时，制度年度变化已为零，所以它不出现在这个斜率里。