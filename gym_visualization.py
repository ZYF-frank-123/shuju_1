import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
df = pd.read_excel('f:\github\shujufenxi_1\k\健身房数据_处理后.xlsx')

# 数据预处理
df['消费日期'] = pd.to_datetime(df['消费日期'])
df['月份'] = df['消费日期'].dt.to_period('M').astype(str)

# 创建输出目录
import os
output_dir = 'f:\github\shujufenxi_1\k\charts'
os.makedirs(output_dir, exist_ok=True)

print("正在生成可视化图表...")

# ============ 图1: 月度消费总额趋势折线图 ============
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('健身房会员消费数据分析可视化', fontsize=16, fontweight='bold')

# 1.1 月度总消费趋势
月度总消费 = df.groupby('月份')['消费总额（元）_修正'].sum()
ax1 = axes[0, 0]
ax1.plot(月度总消费.index, 月度总消费.values, marker='o', linewidth=2, markersize=8, color='#2E86AB')
ax1.fill_between(月度总消费.index, 月度总消费.values, alpha=0.3, color='#2E86AB')
ax1.set_title('月度消费总额趋势', fontsize=12, fontweight='bold')
ax1.set_xlabel('月份')
ax1.set_ylabel('消费总额（元）')
ax1.grid(True, alpha=0.3)
for i, v in enumerate(月度总消费.values):
    ax1.annotate(f'{v:,.0f}', (月度总消费.index[i], v), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

# 1.2 按消费项目的月度趋势
ax2 = axes[0, 1]
月度项目 = df.groupby(['月份', '消费项目'])['消费总额（元）_修正'].sum().unstack(fill_value=0)
for col in 月度项目.columns:
    ax2.plot(月度项目.index, 月度项目[col], marker='o', label=col, linewidth=2)
ax2.set_title('各消费项目月度趋势', fontsize=12, fontweight='bold')
ax2.set_xlabel('月份')
ax2.set_ylabel('消费总额（元）')
ax2.legend(loc='upper left', fontsize=8)
ax2.grid(True, alpha=0.3)

# 1.3 按消费区域的月度趋势
ax3 = axes[1, 0]
月度区域 = df.groupby(['月份', '消费区域'])['消费总额（元）_修正'].sum().unstack(fill_value=0)
for col in 月度区域.columns:
    ax3.plot(月度区域.index, 月度区域[col], marker='s', label=col, linewidth=2)
ax3.set_title('各消费区域月度趋势', fontsize=12, fontweight='bold')
ax3.set_xlabel('月份')
ax3.set_ylabel('消费总额（元）')
ax3.legend(loc='upper left', fontsize=8)
ax3.grid(True, alpha=0.3)

# 1.4 消费项目占比饼图
ax4 = axes[1, 1]
项目消费 = df.groupby('消费项目')['消费总额（元）_修正'].sum().sort_values(ascending=False)
colors = plt.cm.Set3(np.linspace(0, 1, len(项目消费)))
wedges, texts, autotexts = ax4.pie(项目消费.values, labels=项目消费.index, autopct='%1.1f%%', 
                                   colors=colors, startangle=90)
ax4.set_title('消费项目占比分布', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/01_月度消费趋势分析.png', dpi=150, bbox_inches='tight')
print("✓ 图1: 月度消费趋势分析已保存")
plt.close()

# ============ 图2: 消费区域与项目分析 ============
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('消费区域与项目分析', fontsize=16, fontweight='bold')

# 2.1 消费区域占比饼图
ax1 = axes[0, 0]
区域消费 = df.groupby('消费区域')['消费总额（元）_修正'].sum().sort_values(ascending=False)
colors = plt.cm.Pastel1(np.linspace(0, 1, len(区域消费)))
wedges, texts, autotexts = ax1.pie(区域消费.values, labels=区域消费.index, autopct='%1.1f%%', 
                                   colors=colors, startangle=90)
ax1.set_title('消费区域占比分布', fontsize=12, fontweight='bold')

# 2.2 消费区域柱状图
ax2 = axes[0, 1]
bars = ax2.bar(区域消费.index, 区域消费.values, color=plt.cm.Pastel1(np.linspace(0, 1, len(区域消费))))
ax2.set_title('各消费区域消费额', fontsize=12, fontweight='bold')
ax2.set_xlabel('消费区域')
ax2.set_ylabel('消费总额（元）')
ax2.tick_params(axis='x', rotation=45)
for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{height:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

# 2.3 消费项目柱状图
ax3 = axes[1, 0]
bars = ax3.bar(项目消费.index, 项目消费.values, color=plt.cm.Set3(np.linspace(0, 1, len(项目消费))))
ax3.set_title('各消费项目消费额', fontsize=12, fontweight='bold')
ax3.set_xlabel('消费项目')
ax3.set_ylabel('消费总额（元）')
ax3.tick_params(axis='x', rotation=45)
for bar in bars:
    height = bar.get_height()
    ax3.annotate(f'{height:,.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

# 2.4 区域-项目热力图
ax4 = axes[1, 1]
区域项目交叉 = df.groupby(['消费区域', '消费项目'])['消费总额（元）_修正'].sum().unstack(fill_value=0)
im = ax4.imshow(区域项目交叉.values, cmap='YlOrRd', aspect='auto')
ax4.set_xticks(np.arange(len(区域项目交叉.columns)))
ax4.set_yticks(np.arange(len(区域项目交叉.index)))
ax4.set_xticklabels(区域项目交叉.columns, rotation=45, ha='right')
ax4.set_yticklabels(区域项目交叉.index)
ax4.set_title('消费区域-项目热力图', fontsize=12, fontweight='bold')
# 添加数值标注
for i in range(len(区域项目交叉.index)):
    for j in range(len(区域项目交叉.columns)):
        text = ax4.text(j, i, f'{区域项目交叉.iloc[i, j]:.0f}', ha="center", va="center", color="black", fontsize=7)
plt.colorbar(im, ax=ax4, label='消费额（元）')

plt.tight_layout()
plt.savefig(f'{output_dir}/02_消费区域与项目分析.png', dpi=150, bbox_inches='tight')
print("✓ 图2: 消费区域与项目分析已保存")
plt.close()

# ============ 图3: 私教教练分析 ============
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('私教教练业绩分析', fontsize=16, fontweight='bold')

# 3.1 Top10 教练消费额
私教数据 = df[df['消费项目'] == '私教课']
教练消费 = 私教数据.groupby('教练ID')['消费总额（元）_修正'].sum().sort_values(ascending=False)
教练消费 = 教练消费[教练消费.index != '无']

ax1 = axes[0]
top10 = 教练消费.head(10)
bars = ax1.barh(range(len(top10)), top10.values, color=plt.cm.viridis(np.linspace(0, 1, len(top10))))
ax1.set_yticks(range(len(top10)))
ax1.set_yticklabels(top10.index)
ax1.invert_yaxis()
ax1.set_title('Top10 私教教练消费额', fontsize=12, fontweight='bold')
ax1.set_xlabel('消费总额（元）')
for i, v in enumerate(top10.values):
    ax1.text(v + 100, i, f'{v:,.0f}', va='center', fontsize=9)

# 3.2 Top3 教练贡献度饼图
ax2 = axes[1]
top3 = 教练消费.head(3)
others = 教练消费.iloc[3:].sum()
if others > 0:
    plot_data = list(top3.values) + [others]
    plot_labels = list(top3.index) + ['其他教练']
else:
    plot_data = top3.values
    plot_labels = top3.index

colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
wedges, texts, autotexts = ax2.pie(plot_data, labels=plot_labels, autopct='%1.1f%%', 
                                   colors=colors, startangle=90)
ax2.set_title('Top3 教练消费额贡献度', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{output_dir}/03_私教教练分析.png', dpi=150, bbox_inches='tight')
print("✓ 图3: 私教教练分析已保存")
plt.close()

# ============ 图4: 年龄区间分析 ============
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('不同年龄区间会员消费分析', fontsize=16, fontweight='bold')

# 准备年龄区间数据
年龄分析 = []
for age_group in ['18-25岁', '26-35岁', '36-45岁', '46岁以上']:
    age_data = df[df['年龄区间'] == age_group]
    member_count = age_data['会员ID'].nunique()
    total = age_data['消费总额（元）_修正'].sum()
    avg = total / member_count if member_count > 0 else 0
    年龄分析.append({'年龄区间': age_group, '会员数': member_count, '总消费': total, '人均消费': avg})

年龄_df = pd.DataFrame(年龄分析)

# 4.1 各年龄区间会员数
ax1 = axes[0, 0]
bars = ax1.bar(年龄_df['年龄区间'], 年龄_df['会员数'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax1.set_title('各年龄区间会员数', fontsize=12, fontweight='bold')
ax1.set_xlabel('年龄区间')
ax1.set_ylabel('会员数（人）')
for bar in bars:
    height = bar.get_height()
    ax1.annotate(f'{int(height)}人', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

# 4.2 各年龄区间人均消费
ax2 = axes[0, 1]
bars = ax2.bar(年龄_df['年龄区间'], 年龄_df['人均消费'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax2.set_title('各年龄区间人均消费额', fontsize=12, fontweight='bold')
ax2.set_xlabel('年龄区间')
ax2.set_ylabel('人均消费（元）')
for bar in bars:
    height = bar.get_height()
    ax2.annotate(f'{height:.0f}元', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

# 4.3 各年龄区间总消费
ax3 = axes[1, 0]
bars = ax3.bar(年龄_df['年龄区间'], 年龄_df['总消费'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax3.set_title('各年龄区间总消费额', fontsize=12, fontweight='bold')
ax3.set_xlabel('年龄区间')
ax3.set_ylabel('总消费（元）')
for bar in bars:
    height = bar.get_height()
    ax3.annotate(f'{height:,.0f}元', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

# 4.4 年龄区间-消费项目堆叠柱状图
ax4 = axes[1, 1]
年龄项目 = df.groupby(['年龄区间', '消费项目'])['消费总额（元）_修正'].sum().unstack(fill_value=0)
年龄项目 = 年龄项目.reindex(['18-25岁', '26-35岁', '36-45岁', '46岁以上'])
年龄项目.plot(kind='bar', stacked=True, ax=ax4, colormap='Set3')
ax4.set_title('各年龄区间消费项目分布', fontsize=12, fontweight='bold')
ax4.set_xlabel('年龄区间')
ax4.set_ylabel('消费总额（元）')
ax4.legend(loc='upper right', fontsize=8)
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(f'{output_dir}/04_年龄区间分析.png', dpi=150, bbox_inches='tight')
print("✓ 图4: 年龄区间分析已保存")
plt.close()

# ============ 图5: 桑基图 ============
try:
    import plotly.graph_objects as go
    
    # 准备桑基图数据：年龄区间 -> 消费项目 -> 消费区域
    桑基数据 = df.groupby(['年龄区间', '消费项目', '消费区域'])['消费总额（元）_修正'].sum().reset_index()
    
    # 创建节点列表
    年龄节点 = list(桑基数据['年龄区间'].unique())
    项目节点 = list(桑基数据['消费项目'].unique())
    区域节点 = list(桑基数据['消费区域'].unique())
    
    all_nodes = 年龄节点 + 项目节点 + 区域节点
    node_indices = {node: i for i, node in enumerate(all_nodes)}
    
    # 创建连接
    sources = []
    targets = []
    values = []
    
    # 年龄 -> 项目
    age_project = df.groupby(['年龄区间', '消费项目'])['消费总额（元）_修正'].sum().reset_index()
    for _, row in age_project.iterrows():
        sources.append(node_indices[row['年龄区间']])
        targets.append(node_indices[row['消费项目']])
        values.append(row['消费总额（元）_修正'])
    
    # 项目 -> 区域
    project_area = df.groupby(['消费项目', '消费区域'])['消费总额（元）_修正'].sum().reset_index()
    for _, row in project_area.iterrows():
        sources.append(node_indices[row['消费项目']])
        targets.append(node_indices[row['消费区域']])
        values.append(row['消费总额（元）_修正'])
    
    # 创建桑基图
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
            color=["rgba(255, 107, 107, 0.8)" if n in 年龄节点 else 
                   "rgba(78, 205, 196, 0.8)" if n in 项目节点 else 
                   "rgba(69, 183, 209, 0.8)" for n in all_nodes]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )])
    
    fig.update_layout(
        title_text="年龄区间 → 消费项目 → 消费区域 消费额流向图",
        font_size=12,
        height=700
    )
    
    fig.write_html(f'{output_dir}/05_桑基图_年龄项目区域流向.html')
    print("✓ 图5: 桑基图（交互式HTML）已保存")
    
except ImportError:
    print("⚠ plotly 未安装，跳过桑基图生成")
    print("  如需生成交互式桑基图，请运行: pip install plotly")

# ============ 图6: 综合仪表盘 ============
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

fig.suptitle('健身房会员消费数据仪表盘', fontsize=18, fontweight='bold', y=0.98)

# 关键指标
总消费 = df['消费总额（元）_修正'].sum()
总会员 = df['会员ID'].nunique()
总记录 = len(df)
私教占比 = df[df['消费项目'] == '私教课']['消费总额（元）_修正'].sum() / 总消费 * 100

# 指标卡片
ax1 = fig.add_subplot(gs[0, 0])
ax1.text(0.5, 0.7, f'¥{总消费:,.0f}', fontsize=24, ha='center', fontweight='bold', color='#2E86AB')
ax1.text(0.5, 0.3, '总消费额', fontsize=12, ha='center', color='gray')
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')

ax2 = fig.add_subplot(gs[0, 1])
ax2.text(0.5, 0.7, f'{总会员}', fontsize=24, ha='center', fontweight='bold', color='#A23B72')
ax2.text(0.5, 0.3, '会员总数', fontsize=12, ha='center', color='gray')
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

ax3 = fig.add_subplot(gs[0, 2])
ax3.text(0.5, 0.7, f'{私教占比:.1f}%', fontsize=24, ha='center', fontweight='bold', color='#F18F01')
ax3.text(0.5, 0.3, '私教课占比', fontsize=12, ha='center', color='gray')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

# 月度趋势
ax4 = fig.add_subplot(gs[1, :2])
ax4.plot(月度总消费.index, 月度总消费.values, marker='o', linewidth=3, markersize=8, color='#2E86AB')
ax4.fill_between(月度总消费.index, 月度总消费.values, alpha=0.3, color='#2E86AB')
ax4.set_title('月度消费总额趋势', fontsize=12, fontweight='bold')
ax4.set_xlabel('月份')
ax4.set_ylabel('消费总额（元）')
ax4.grid(True, alpha=0.3)

# 消费项目占比
ax5 = fig.add_subplot(gs[1, 2])
项目消费 = df.groupby('消费项目')['消费总额（元）_修正'].sum().sort_values(ascending=False)
colors = plt.cm.Set3(np.linspace(0, 1, len(项目消费)))
ax5.pie(项目消费.values, labels=项目消费.index, autopct='%1.1f%%', colors=colors, startangle=90)
ax5.set_title('消费项目占比', fontsize=12, fontweight='bold')

# 年龄区间人均消费
ax6 = fig.add_subplot(gs[2, 0])
bars = ax6.bar(年龄_df['年龄区间'], 年龄_df['人均消费'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
ax6.set_title('各年龄区间人均消费', fontsize=12, fontweight='bold')
ax6.set_ylabel('人均消费（元）')
ax6.tick_params(axis='x', rotation=45)

# Top5 教练
ax7 = fig.add_subplot(gs[2, 1])
top5 = 教练消费.head(5)
bars = ax7.barh(range(len(top5)), top5.values, color=plt.cm.viridis(np.linspace(0, 1, len(top5))))
ax7.set_yticks(range(len(top5)))
ax7.set_yticklabels(top5.index)
ax7.invert_yaxis()
ax7.set_title('Top5 私教教练', fontsize=12, fontweight='bold')
ax7.set_xlabel('消费额（元）')

# 消费区域分布
ax8 = fig.add_subplot(gs[2, 2])
区域消费 = df.groupby('消费区域')['消费总额（元）_修正'].sum().sort_values(ascending=False)
ax8.pie(区域消费.values, labels=区域消费.index, autopct='%1.1f%%', colors=plt.cm.Pastel1(np.linspace(0, 1, len(区域消费))))
ax8.set_title('消费区域分布', fontsize=12, fontweight='bold')

plt.savefig(f'{output_dir}/06_综合仪表盘.png', dpi=150, bbox_inches='tight')
print("✓ 图6: 综合仪表盘已保存")
plt.close()

print("\n" + "="*60)
print("所有可视化图表生成完成！")
print(f"图表保存位置: {output_dir}")
print("="*60)
print("\n生成的图表列表：")
print("1. 01_月度消费趋势分析.png - 月度趋势折线图及项目占比")
print("2. 02_消费区域与项目分析.png - 区域分析、热力图")
print("3. 03_私教教练分析.png - Top教练排名及贡献度")
print("4. 04_年龄区间分析.png - 年龄维度消费分析")
print("5. 05_桑基图_年龄项目区域流向.html - 交互式桑基图")
print("6. 06_综合仪表盘.png - 关键指标汇总仪表盘")
