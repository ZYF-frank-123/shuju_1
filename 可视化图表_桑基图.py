import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

df = pd.read_excel(r'f:\github\shujufenxi_1\g\健身房会员消费数据.xlsx')

age_groups = df['年龄区间'].unique()
projects = df['消费项目'].unique()
areas = df['消费区域'].unique()

labels = list(age_groups) + list(projects) + list(areas)

age_to_project = df.groupby(['年龄区间', '消费项目'])['消费总额（元）'].sum().reset_index()
project_to_area = df.groupby(['消费项目', '消费区域'])['消费总额（元）'].sum().reset_index()

source_indices = []
target_indices = []
values = []

age_to_idx = {age: i for i, age in enumerate(age_groups)}
project_to_idx = {proj: i + len(age_groups) for i, proj in enumerate(projects)}
area_to_idx = {area: i + len(age_groups) + len(projects) for i, area in enumerate(areas)}

for _, row in age_to_project.iterrows():
    source_indices.append(age_to_idx[row['年龄区间']])
    target_indices.append(project_to_idx[row['消费项目']])
    values.append(row['消费总额（元）'])

for _, row in project_to_area.iterrows():
    source_indices.append(project_to_idx[row['消费项目']])
    target_indices.append(area_to_idx[row['消费区域']])
    values.append(row['消费总额（元）'])

colors_source = [
    '#FF6B6B', '#FFB347', '#87CEEB', '#98D8C8'
][:len(age_groups)]

colors_mid = [
    '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#1ABC9C', '#E67E22'
][:len(projects)]

colors_target = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'
][:len(areas)]

link_colors = []
for src in source_indices:
    if src < len(age_groups):
        link_colors.append('rgba(255, 107, 107, 0.4)')
    else:
        link_colors.append('rgba(100, 149, 237, 0.4)')

fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=20,
        thickness=25,
        line=dict(color="black", width=0.8),
        label=labels,
        color=['#FF6B6B', '#FFB347', '#87CEEB', '#98D8C8'] * (len(labels) // 4 + 1)
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors
    )
)])

fig.update_layout(
    title=dict(
        text="<b>年龄区间 → 消费项目 → 消费区域</b><br><sup>消费额流向桑基图</sup>",
        font=dict(size=20),
        x=0.5,
        xanchor='center'
    ),
    font=dict(size=13, family="Microsoft YaHei"),
    width=1200,
    height=700,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

pio.write_html(fig, file=r'f:\github\shujufenxi_1\g\消费流向桑基图.html', include_plotlyjs=True, full_html=True)
print("桑基图已保存：消费流向桑基图.html（交互式图表，可用浏览器打开）")
