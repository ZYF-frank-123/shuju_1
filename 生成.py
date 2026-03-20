# gym_consume_data.py
import pandas as pd
import random
from datetime import datetime, timedelta

# 固定随机种子，保证每次生成数据一致
random.seed(42)

# 1. 基础配置（修复：2026年2月只有28天，修正end_date）
# 时间范围：2025-09-01 至 2026-02-28（近6个月）
start_date = datetime(2025, 9, 1)
end_date = datetime(2026, 2, 28)  # 关键修改：29→28
date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
# 数据条数
num_rows = 200

# 2. 基础数据字典（贴合真实健身房场景）
last_names = ["王", "李", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
first_names = ["伟", "芳", "娜", "敏", "静", "强", "磊", "洋", "杰", "婷"]
genders = ["男", "女"]
age_ranges = ["18-25岁", "26-35岁", "36-45岁", "46岁以上"]
card_types = ["年卡", "季卡", "月卡", "次卡", "体验卡"]
consume_items = ["私教课", "瑜伽团课", "动感单车团课", "搏击团课", "健身卡续费", "体能检测", "运动装备购买"]
time_periods = ["早间（6:00-10:00）", "午间（10:00-14:00）", "晚间（14:00-22:00）", "深夜（22:00-24:00）"]
consume_areas = ["有氧区", "力量区", "私教区", "团课室", "前台服务区"]
pay_methods = ["微信支付", "支付宝", "银行卡", "现金"]
consume_status = ["已完成", "已取消", "待核销"]

# 3. 生成数据
data = []
for i in range(num_rows):
    # 核心字段赋值（逻辑关联，无异常值）
    member_id = f"HY{i + 1:03d}"  # 会员ID：HY001-HY200
    name = random.choice(last_names) + random.choice(first_names)
    gender = random.choice(genders)
    age_range = random.choice(age_ranges)
    card_type = random.choice(card_types)
    item = random.choice(consume_items)

    # 消费项目关联单价/次数/教练ID
    if item == "私教课":
        price = random.randint(200, 500)
        times = random.randint(1, 10)
        coach_id = f"JL{random.randint(1, 20):03d}"
    elif "团课" in item:
        price = random.randint(30, 80)
        times = random.randint(1, 5)
        coach_id = "无"
    elif item == "健身卡续费":
        price_map = {"年卡": 1800, "季卡": 500, "月卡": 200, "次卡": 30, "体验卡": 99}
        price = price_map[card_type]
        times = 1
        coach_id = "无"
    elif item == "体能检测":
        price = 100
        times = 1
        coach_id = "无"
    else:  # 运动装备
        price = random.randint(50, 500)
        times = random.randint(1, 3)
        coach_id = "无"

    total = price * times  # 自动计算总额
    consume_date = random.choice(date_range).strftime("%Y-%m-%d")
    time_period = random.choice(time_periods)
    area = random.choice(consume_areas)
    pay_method = random.choice(pay_methods)
    status = random.choice(consume_status)

    data.append([
        member_id, name, gender, age_range, card_type, item, times, price, total,
        consume_date, time_period, coach_id, area, pay_method, status
    ])

# 4. 写入Excel
columns = [
    "会员ID", "会员姓名", "性别", "年龄区间", "会员卡类型", "消费项目",
    "消费次数", "单价（元）", "消费总额（元）", "消费日期", "消费时段",
    "教练ID", "消费区域", "支付方式", "消费状态"
]
df = pd.DataFrame(data, columns=columns)
df.to_excel("健身房会员消费数据.xlsx", index=False, engine="openpyxl")

print(f"健身房数据生成完成！共{len(df)}条，文件保存为：健身房会员消费数据.xlsx")