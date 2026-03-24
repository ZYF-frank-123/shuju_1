import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
import seaborn as sns

# 读取数据
df = pd.read_excel('f:/github/shujufenxi_1/d/健身房会员消费数据.xlsx')

# 数据处理：验证消费总额计算
df['计算消费总额'] = df['消费次数'] * df['单价（元）']
inconsistent_count = len(df[df['消费总额（元）'] != df['计算消费总额']])
print(f'计算不一致的记录数：{inconsistent_count}')
if inconsistent_count > 0:
    df['消费总额（元）'] = df['计算消费总额']
    print('已修正消费总额数据')
df = df.drop('计算消费总额', axis=1)

# 处理消费日期，提取月份
df['消费日期'] = pd.to_datetime(df['消费日期'])
df['月份'] = df['消费日期'].dt.strftime('%Y-%m')

# 创建可视化图表
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# 1. 月度消费总额趋势折线图
plt.figure(figsize=(12, 6))
monthly_total = df.groupby('月份')['消费总额（元）'].sum().reset_index()
plt.plot(monthly_total['月份'], monthly_total['消费总额（元）'], marker='o', linewidth=2, markersize=8, color='#2E86AB')
plt.title('月度消费总额趋势', fontsize=16, pad=20)
plt.xlabel('月份', fontsize=12)
plt.ylabel('消费总额（元）', fontsize=12)
plt.grid(True, alpha=0.3)
for x, y in zip(monthly_total['月份'], monthly_total['消费总额（元）']):
    plt.text(x, y + 500, f'{y:,}', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/月度消费总额趋势.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. 各消费区域消费额占比饼图
plt.figure(figsize=(10, 8))
area_ratio = df.groupby('消费区域')['消费总额（元）'].sum()
colors = sns.color_palette('Set2', len(area_ratio))
wedges, texts, autotexts = plt.pie(area_ratio, labels=area_ratio.index, colors=colors,
                                   autopct='%1.1f%%', startangle=90)
plt.title('各消费区域消费额占比', fontsize=16, pad=20)
plt.setp(autotexts, size=10, weight='bold')
plt.axis('equal')
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/消费区域占比.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. 各消费项目消费额占比饼图
plt.figure(figsize=(10, 8))
item_ratio = df.groupby('消费项目')['消费总额（元）'].sum()
colors = sns.color_palette('Set3', len(item_ratio))
wedges, texts, autotexts = plt.pie(item_ratio, labels=item_ratio.index, colors=colors,
                                   autopct='%1.1f%%', startangle=90)
plt.title('各消费项目消费额占比', fontsize=16, pad=20)
plt.setp(autotexts, size=10, weight='bold')
plt.axis('equal')
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/消费项目占比.png', dpi=300, bbox_inches='tight')
plt.show()

# 4. 私教课消费额 Top3 教练柱状图
private_class = df[df['消费项目'] == '私教课']
private_class_with_coach = private_class[private_class['教练ID'] != '无']
coach_consumption = private_class_with_coach.groupby('教练ID')['消费总额（元）'].sum().sort_values(ascending=False).head(3)

plt.figure(figsize=(10, 6))
bars = plt.bar(coach_consumption.index, coach_consumption.values, color=['#E63946', '#F4A261', '#2A9D8F'])
plt.title('私教课消费额 Top3 教练', fontsize=16, pad=20)
plt.xlabel('教练ID', fontsize=12)
plt.ylabel('消费总额（元）', fontsize=12)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 100,
             f'{height:,}', ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/Top3教练.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. 各年龄区间人均消费额柱状图
age_total = df.groupby('年龄区间')['消费总额（元）'].sum().reset_index()
age_member_count = df.groupby('年龄区间')['会员ID'].nunique().reset_index(name='会员数')
age_avg = pd.merge(age_total, age_member_count, on='年龄区间')
age_avg['人均消费额(元)'] = (age_avg['消费总额（元）'] / age_avg['会员数']).round(2)
age_avg = age_avg.sort_values('人均消费额(元)', ascending=False)

plt.figure(figsize=(10, 6))
bars = plt.bar(age_avg['年龄区间'], age_avg['人均消费额(元)'], color=sns.color_palette('viridis', len(age_avg)))
plt.title('各年龄区间人均消费额', fontsize=16, pad=20)
plt.xlabel('年龄区间', fontsize=12)
plt.ylabel('人均消费额（元）', fontsize=12)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{height:.0f}', ha='center', va='bottom', fontsize=11)
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/年龄区间人均消费.png', dpi=300, bbox_inches='tight')
plt.show()

# 6. 各年龄区间消费项目分布热力图
age_item_dist = df.groupby(['年龄区间', '消费项目'])['消费总额（元）'].sum().unstack().fillna(0)
age_item_dist_pct = age_item_dist.div(age_item_dist.sum(axis=1), axis=0) * 100

plt.figure(figsize=(12, 8))
sns.heatmap(age_item_dist_pct, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': '占比(%)'})
plt.title('各年龄区间消费项目分布占比(%)', fontsize=16, pad=20)
plt.xlabel('消费项目', fontsize=12)
plt.ylabel('年龄区间', fontsize=12)
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/年龄区间消费偏好.png', dpi=300, bbox_inches='tight')
plt.show()

# 7. 月度消费趋势（按消费项目）
plt.figure(figsize=(14, 8))
monthly_by_item = df.groupby(['月份', '消费项目'])['消费总额（元）'].sum().unstack().fillna(0)
monthly_by_item.plot(kind='line', marker='o', linewidth=2, ax=plt.gca())
plt.title('月度消费趋势（按消费项目）', fontsize=16, pad=20)
plt.xlabel('月份', fontsize=12)
plt.ylabel('消费总额（元）', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('f:/github/shujufenxi_1/d/月度消费趋势_按项目.png', dpi=300, bbox_inches='tight')
plt.show()

print('='*60)
print('可视化图表已生成完成！')
print('生成的图表文件：')
print('1. 月度消费总额趋势.png')
print('2. 消费区域占比.png')
print('3. 消费项目占比.png')
print('4. Top3教练.png')
print('5. 年龄区间人均消费.png')
print('6. 年龄区间消费偏好.png')
print('7. 月度消费趋势_按项目.png')
print('='*60)

# 保存分析结果到Excel
with pd.ExcelWriter('f:/github/shujufenxi_1/d/健身房分析结果.xlsx') as writer:
    monthly_total.to_excel(writer, sheet_name='月度消费总额', index=False)
    area_ratio.reset_index().to_excel(writer, sheet_name='消费区域占比', index=False)
    item_ratio.reset_index().to_excel(writer, sheet_name='消费项目占比', index=False)
    coach_consumption.reset_index().to_excel(writer, sheet_name='Top3教练', index=False)
    age_avg.to_excel(writer, sheet_name='年龄区间人均消费', index=False)
    age_item_dist_pct.to_excel(writer, sheet_name='年龄区间消费偏好')

print('分析结果已保存到：健身房分析结果.xlsx')
