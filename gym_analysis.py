import pandas as pd
import numpy as np

# 读取数据
df = pd.read_excel('f:\github\shujufenxi_1\k\健身房会员消费数据.xlsx')

print("="*80)
print("一、数据处理")
print("="*80)

# 1. 验证并修正消费总额
df['计算总额'] = df['消费次数'] * df['单价（元）']
df['差额'] = df['消费总额（元）'] - df['计算总额']

# 找出不一致的记录
不一致记录 = df[df['差额'] != 0]
print(f"\n1. 消费总额验证结果：")
print(f"   - 总记录数: {len(df)}")
print(f"   - 不一致记录数: {len(不一致记录)}")

if len(不一致记录) > 0:
    print(f"\n   不一致记录详情：")
    print(不一致记录[['会员ID', '消费项目', '消费次数', '单价（元）', '消费总额（元）', '计算总额', '差额']].head(10).to_string())
    # 修正数据
    df['消费总额（元）_修正'] = df['计算总额']
    print(f"\n   已修正所有不一致记录")
else:
    print(f"   - 所有记录消费总额计算正确，无需修正")
    df['消费总额（元）_修正'] = df['消费总额（元）']

# 2. 按月份聚合 - 月度消费总额汇总表
df['消费日期'] = pd.to_datetime(df['消费日期'])
df['月份'] = df['消费日期'].dt.to_period('M').astype(str)

print(f"\n2. 月度消费总额汇总表：")

# 2.1 按消费项目维度汇总
月度项目汇总 = df.groupby(['月份', '消费项目'])['消费总额（元）_修正'].sum().reset_index()
月度项目透视 = 月度项目汇总.pivot(index='月份', columns='消费项目', values='消费总额（元）_修正').fillna(0)
print(f"\n   (1) 按消费项目维度汇总（单位：元）：")
print(月度项目透视.to_string())

# 2.2 按消费区域维度汇总
月度区域汇总 = df.groupby(['月份', '消费区域'])['消费总额（元）_修正'].sum().reset_index()
月度区域透视 = 月度区域汇总.pivot(index='月份', columns='消费区域', values='消费总额（元）_修正').fillna(0)
print(f"\n   (2) 按消费区域维度汇总（单位：元）：")
print(月度区域透视.to_string())

# 保存处理后的数据
df.to_excel('f:\github\shujufenxi_1\k\健身房数据_处理后.xlsx', index=False)
print(f"\n   处理后的数据已保存至：健身房数据_处理后.xlsx")

print("\n" + "="*80)
print("二、统计分析")
print("="*80)

# 1. 各消费区域、各消费项目的消费额占比
total_amount = df['消费总额（元）_修正'].sum()

print(f"\n1. 消费额占比分析（总消费额: {total_amount:,.0f} 元）：")

# 按消费区域占比
区域消费 = df.groupby('消费区域')['消费总额（元）_修正'].sum().sort_values(ascending=False)
区域占比 = (区域消费 / total_amount * 100).round(2)
print(f"\n   (1) 各消费区域消费额占比：")
for area, pct in 区域占比.items():
    amount = 区域消费[area]
    print(f"       {area}: {amount:,.0f}元 ({pct}%)")

# 按消费项目占比
项目消费 = df.groupby('消费项目')['消费总额（元）_修正'].sum().sort_values(ascending=False)
项目占比 = (项目消费 / total_amount * 100).round(2)
print(f"\n   (2) 各消费项目消费额占比：")
for item, pct in 项目占比.items():
    amount = 项目消费[item]
    print(f"       {item}: {amount:,.0f}元 ({pct}%)")

# 2. Top3 私教教练评选
私教数据 = df[df['消费项目'] == '私教课']
私教总消费 = 私教数据['消费总额（元）_修正'].sum()

教练消费 = 私教数据.groupby('教练ID')['消费总额（元）_修正'].sum().sort_values(ascending=False)
教练消费 = 教练消费[教练消费.index != '无']  # 排除无教练ID的记录

print(f"\n2. 私教课 Top3 教练评选（私教课总消费额: {私教总消费:,.0f} 元）：")
print(f"\n   排名 | 教练ID | 消费总额(元) | 贡献度(%)")
print(f"   " + "-"*45)
for i, (coach, amount) in enumerate(教练消费.head(3).items(), 1):
    contribution = (amount / 私教总消费 * 100)
    print(f"   {i}    | {coach}   | {amount:>12,.0f} | {contribution:>6.2f}%")

# 3. 不同年龄区间会员消费偏好及人均消费
print(f"\n3. 不同年龄区间会员消费分析：")

年龄区间分析 = []
for age_group in df['年龄区间'].unique():
    age_data = df[df['年龄区间'] == age_group]
    
    # 该区间会员数（按会员ID去重）
    member_count = age_data['会员ID'].nunique()
    
    # 总消费额
    total = age_data['消费总额（元）_修正'].sum()
    
    # 人均消费
    avg_per_person = total / member_count if member_count > 0 else 0
    
    # 消费项目分布
    item_dist = age_data.groupby('消费项目')['消费总额（元）_修正'].sum()
    item_pct = (item_dist / item_dist.sum() * 100).round(2)
    
    年龄区间分析.append({
        '年龄区间': age_group,
        '会员数': member_count,
        '总消费额': total,
        '人均消费额': avg_per_person,
        '消费项目占比': item_pct.to_dict()
    })

# 按年龄区间排序
年龄排序 = {'18-25岁': 1, '26-35岁': 2, '36-45岁': 3, '46岁以上': 4}
年龄区间分析.sort(key=lambda x: 年龄排序.get(x['年龄区间'], 99))

for info in 年龄区间分析:
    print(f"\n   【{info['年龄区间']}】")
    print(f"   - 会员数: {info['会员数']}人")
    print(f"   - 总消费额: {info['总消费额']:,.0f}元")
    print(f"   - 人均消费额: {info['人均消费额']:,.0f}元")
    print(f"   - 消费项目分布:")
    for item, pct in sorted(info['消费项目占比'].items(), key=lambda x: -x[1]):
        print(f"       {item}: {pct}%")

print("\n" + "="*80)
print("三、可视化说明")
print("="*80)

可视化说明 = """
1. 折线图展示「月度消费总额趋势」

   适用场景：
   - 展示近6个月健身房整体营收变化趋势
   - 对比不同消费项目或区域的月度表现
   - 识别消费高峰期和低谷期（如节假日、促销活动期间）
   - 预测未来营收走势，辅助制定经营策略

   业务价值：
   - 帮助管理者快速把握经营状况的时间变化规律
   - 及时发现异常波动，便于深入分析原因
   - 为制定月度/季度营销计划提供数据支撑
   - 评估促销活动效果，优化资源配置

2. 桑基图展示「年龄区间→消费项目→消费区域」消费额分布

   适用场景：
   - 展示多维度数据间的流量关系和转化路径
   - 分析不同年龄段会员的消费流向（喜欢什么项目、去什么区域）
   - 识别主要消费路径和潜在优化空间
   - 呈现复杂的关联关系，比传统交叉表更直观

   业务价值：
   - 直观展示会员从年龄特征到消费行为的全链路分布
   - 帮助识别高价值客户群体的消费偏好
   - 为区域布局优化、项目设置调整提供依据
   - 发现潜在交叉销售机会（如某年龄段在特定区域的消费集中）
   - 支持精准营销策略制定（针对不同年龄+项目+区域组合）
"""
print(可视化说明)

print("\n" + "="*80)
print("分析完成！")
print("="*80)
