import pandas as pd
import numpy as np

df = pd.read_excel(r'f:\github\shujufenxi_1\g\健身房会员消费数据.xlsx')

print("=" * 60)
print("一、数据处理")
print("=" * 60)

print("\n【1. 验证消费总额计算】")
df['计算总额'] = df['消费次数'] * df['单价（元）']
df['总额差异'] = df['消费总额（元）'] - df['计算总额']
inconsistent = df[df['总额差异'] != 0]

if len(inconsistent) > 0:
    print(f"发现 {len(inconsistent)} 条记录消费总额计算不一致：")
    print(inconsistent[['会员ID', '会员姓名', '消费次数', '单价（元）', '消费总额（元）', '计算总额', '总额差异']])
    df['消费总额（元）'] = df['计算总额']
    print("\n已修正消费总额数据")
else:
    print("所有记录的消费总额计算正确，无需修正")

print("\n【2. 月度消费总额汇总表】")
df['消费月份'] = pd.to_datetime(df['消费日期']).dt.strftime('%Y-%m')

print("\n(1) 按月份-消费项目汇总：")
monthly_project = df.pivot_table(
    values='消费总额（元）',
    index='消费月份',
    columns='消费项目',
    aggfunc='sum',
    fill_value=0
)
monthly_project['月度合计'] = monthly_project.sum(axis=1)
print(monthly_project.round(2))

print("\n(2) 按月份-消费区域汇总：")
monthly_area = df.pivot_table(
    values='消费总额（元）',
    index='消费月份',
    columns='消费区域',
    aggfunc='sum',
    fill_value=0
)
monthly_area['月度合计'] = monthly_area.sum(axis=1)
print(monthly_area.round(2))

print("\n" + "=" * 60)
print("二、统计分析")
print("=" * 60)

print("\n【1. 消费额占比分析】")
total_consumption = df['消费总额（元）'].sum()

print("\n(1) 各消费区域消费额占比：")
area_ratio = df.groupby('消费区域')['消费总额（元）'].sum()
area_ratio_df = pd.DataFrame({
    '消费总额（元）': area_ratio,
    '占比（%）': (area_ratio / total_consumption * 100).round(2)
}).sort_values('消费总额（元）', ascending=False)
print(area_ratio_df)

print("\n(2) 各消费项目消费额占比：")
project_ratio = df.groupby('消费项目')['消费总额（元）'].sum()
project_ratio_df = pd.DataFrame({
    '消费总额（元）': project_ratio,
    '占比（%）': (project_ratio / total_consumption * 100).round(2)
}).sort_values('消费总额（元）', ascending=False)
print(project_ratio_df)

print("\n【2. 私教课Top3教练评选】")
private_coach = df[df['消费项目'] == '私教课']
private_total = private_coach['消费总额（元）'].sum()

coach_ranking = private_coach.groupby('教练ID').agg({
    '消费总额（元）': 'sum',
    '会员ID': 'count'
}).rename(columns={'会员ID': '消费笔数'})

coach_ranking['贡献度（%）'] = (coach_ranking['消费总额（元）'] / private_total * 100).round(2)
coach_ranking = coach_ranking.sort_values('消费总额（元）', ascending=False)

print(f"\n私教课总消费额：{private_total:.2f} 元")
print(f"\nTop3 教练消费额贡献排名：")
top3_coaches = coach_ranking.head(3)
print(top3_coaches)
print(f"\nTop3 教练合计贡献度：{top3_coaches['贡献度（%）'].sum():.2f}%")

print("\n【3. 年龄区间消费偏好及人均消费额】")
print("\n(1) 各年龄区间消费项目分布占比：")
age_project = df.pivot_table(
    values='消费总额（元）',
    index='年龄区间',
    columns='消费项目',
    aggfunc='sum',
    fill_value=0
)
age_project_pct = age_project.div(age_project.sum(axis=1), axis=0) * 100
print(age_project_pct.round(2))

print("\n(2) 各年龄区间人均消费额：")
age_stats = df.groupby('年龄区间').agg({
    '消费总额（元）': 'sum',
    '会员ID': 'nunique'
}).rename(columns={'会员ID': '会员人数'})
age_stats['人均消费额（元）'] = (age_stats['消费总额（元）'] / age_stats['会员人数']).round(2)
print(age_stats)

print("\n" + "=" * 60)
print("三、可视化说明")
print("=" * 60)

print("""
【1. 折线图 - 月度消费总额趋势】

适用场景：
• 展示连续6个月（2025-09至2026-02）的消费总额变化趋势
• 可同时绘制多条折线对比不同消费项目或消费区域的月度走势
• 适合观察消费的季节性波动、增长或下降趋势

业务价值：
• 帮助管理层识别消费高峰期和低谷期，优化资源配置
• 评估营销活动效果，如某月促销是否带动消费增长
• 预测未来消费趋势，制定合理的营收目标和预算计划
• 发现异常波动，及时调整经营策略

【2. 桑基图 - 年龄区间→消费项目→消费区域消费额分布】

适用场景：
• 展示三个维度之间的消费流向关系
• 直观呈现不同年龄区间会员的消费路径选择
• 流量宽度反映消费额大小，便于识别主要消费通道

业务价值：
• 精准定位目标客群：识别各年龄段的核心消费项目和偏好区域
• 优化服务布局：根据消费流向合理配置各区域的资源和教练
• 制定差异化营销策略：针对不同年龄段推送个性化消费项目
• 发现潜在机会：识别消费流量较小的路径，挖掘增长空间
• 提升会员体验：根据年龄偏好优化设施和课程安排
""")

print("\n" + "=" * 60)
print("分析完成！")
print("=" * 60)
