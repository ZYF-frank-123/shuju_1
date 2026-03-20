import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_excel(r'f:\github\shujufenxi_1\g\健身房会员消费数据.xlsx')
df['消费月份'] = pd.to_datetime(df['消费日期']).dt.strftime('%Y-%m')

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

ax1 = axes[0, 0]
monthly_total = df.groupby('消费月份')['消费总额（元）'].sum().sort_index()
ax1.plot(monthly_total.index, monthly_total.values, marker='o', linewidth=2.5, markersize=10, color='#2E86AB')
ax1.fill_between(monthly_total.index, monthly_total.values, alpha=0.3, color='#2E86AB')
ax1.set_title('月度消费总额趋势', fontsize=16, fontweight='bold', pad=15)
ax1.set_xlabel('月份', fontsize=12)
ax1.set_ylabel('消费总额（元）', fontsize=12)
ax1.tick_params(axis='x', rotation=0)
ax1.grid(True, alpha=0.3, linestyle='--')
for i, (x, y) in enumerate(zip(monthly_total.index, monthly_total.values)):
    ax1.annotate(f'{y:,.0f}', (x, y), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=10, fontweight='bold')

ax2 = axes[0, 1]
monthly_project = df.pivot_table(values='消费总额（元）', index='消费月份', columns='消费项目', aggfunc='sum', fill_value=0).sort_index()
colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C', '#E67E22']
for i, col in enumerate(monthly_project.columns):
    ax2.plot(monthly_project.index, monthly_project[col], marker='o', linewidth=2, markersize=6, label=col, color=colors[i % len(colors)])
ax2.set_title('各消费项目月度消费趋势', fontsize=16, fontweight='bold', pad=15)
ax2.set_xlabel('月份', fontsize=12)
ax2.set_ylabel('消费总额（元）', fontsize=12)
ax2.tick_params(axis='x', rotation=0)
ax2.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax2.grid(True, alpha=0.3, linestyle='--')

ax3 = axes[1, 0]
monthly_area = df.pivot_table(values='消费总额（元）', index='消费月份', columns='消费区域', aggfunc='sum', fill_value=0).sort_index()
area_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
for i, col in enumerate(monthly_area.columns):
    ax3.plot(monthly_area.index, monthly_area[col], marker='s', linewidth=2, markersize=6, label=col, color=area_colors[i % len(area_colors)])
ax3.set_title('各消费区域月度消费趋势', fontsize=16, fontweight='bold', pad=15)
ax3.set_xlabel('月份', fontsize=12)
ax3.set_ylabel('消费总额（元）', fontsize=12)
ax3.tick_params(axis='x', rotation=0)
ax3.legend(loc='upper right', fontsize=9, framealpha=0.9)
ax3.grid(True, alpha=0.3, linestyle='--')

ax4 = axes[1, 1]
area_ratio = df.groupby('消费区域')['消费总额（元）'].sum().sort_values(ascending=False)
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
wedges, texts, autotexts = ax4.pie(area_ratio.values, labels=area_ratio.index, autopct='%1.1f%%', 
                                    colors=colors_pie, explode=[0.05, 0.02, 0.02, 0.02, 0.02],
                                    shadow=True, startangle=90)
ax4.set_title('各消费区域消费额占比', fontsize=16, fontweight='bold', pad=15)
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')

plt.tight_layout(pad=3.0)
plt.savefig(r'f:\github\shujufenxi_1\g\消费趋势折线图.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("折线图已保存：消费趋势折线图.png")
