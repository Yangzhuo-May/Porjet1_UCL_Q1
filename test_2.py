import matplotlib.pyplot as plt
import numpy as np

# 1. 读取数据
# skip_header=2: 跳过前两行（第1行是“质量 A”，第2行是列名“t x vx”）
# usecols=(0, 1): 只读取第0列(t)和第1列(x)，避免某些行缺少vx导致列数不匹配报错
data = np.genfromtxt(
    "data/massA_test.csv",
    delimiter=None,
    skip_header=2,
    usecols=(0, 1),
    invalid_raise=False,
)

# 提取时间和水平位移列
t = data[:, 0]
x = data[:, 1]

# 2. 过滤掉可能存在的空值 (NaN)
valid_mask = ~np.isnan(t) & ~np.isnan(x)
t = t[valid_mask]
x = x[valid_mask]

# 3. 进行二次多项式拟合（模拟质点运动轨迹）
fit_coeffs = np.polyfit(t, x, 2)
x_fit = np.polyval(fit_coeffs, t)

# 4. 使用 Matplotlib 绘制图表
plt.figure(figsize=(9, 5), dpi=100)

# 绘制实验测量散点图
plt.scatter(
    t, x, color="blue", label="Experimental Data (Mass A)", s=25, zorder=3
)

# 绘制拟合曲线
plt.plot(
    t, x_fit, color="red", linestyle="--", label="Polynomial Fit", linewidth=2
)

# 5. 图表美化与标签设置
plt.title("Mass A - Position $x$ vs Time $t$", fontsize=14, fontweight="bold")
plt.xlabel("Time $t$ (s)", fontsize=12)
plt.ylabel("Position $x$ (m)", fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle=":", alpha=0.6)

# 显示图表
plt.tight_layout()
plt.show()

# 文件读取路径错误，图表列（名字）和数据文件的表头对不上，数据文件断层（因为缺失帧或是被去除的无效数据）- 让程序跳过这些空缺，程序的分割符号和数据文件的不一致