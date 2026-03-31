---
name: "finance-tracker"
description: "守护灵记账助手，中英双语记录财务，自动写入每日记录文件，保留基本财务信息，提供守护灵建议。当用户提供账单或询问财务状况时调用。"
---

# 守护灵记账助手

## 核心功能

- 中英双语财务记录
- 自动写入每日记录文件（`c:\Users\32199\shElter\I\A-04每日记录\YYYY-MM-DD.md`）
- 保留余额、定存目标、可支配额度等基本信息
- 累计结余管理（初始为0）
- 守护灵式财务建议

## 使用方式

用户只需说："今日花销：[项目] [金额]"

## 自动文件写入

技能会自动：
- 创建每日记录文件：`c:\Users\32199\shElter\I\A-04每日记录\YYYY-MM-DD.md`
- 按照五界框架格式写入内容
- 自动添加 `#I #记账 #守护灵建议` 标签
- 保持中英双语交替格式

## 文件格式示例

```markdown
# 📊 2026年3月31日财务记录 | Financial Record for March 31, 2026

## 💰 基本财务信息 | Basic Financial Information

*Total balance: 54,787.97 yuan*

*总余额：54,787.97元*

*Savings goal: 35,000 yuan*

*定存目标：35,000元*

*Available funds: 19,787.97 yuan*

*可支配额度：19,787.97元*

## 💸 今日花销 | Today's Expenses

*Lunch: 25 yuan*

*午餐：25元*

## 📈 当日情况 | Daily Situation

*Daily budget: 71.96 yuan*

*当日预算：71.96元*

*Daily balance: 46.96 yuan*

*当日结余：46.96元*

*Cumulative balance: 46.96 yuan*

*累计结余：46.96元*

## 💡 守护灵建议 | Guardian Spirit Advice

*Good spending control today! Save the remaining balance to cumulative.*

*今日消费控制良好！将剩余预算存入累计结余。*

---

#I #记账 #守护灵建议
```

## 累计结余规则

- 初始累计结余为0
- 每日结余自动存入累计
- 花超时从累计中扣除