# 购书助手 / Book Shopping Assistant

> 先查电子版，再比实体价，帮你省钱买书
> Check e-book first, compare prices next, save money on books

## 一句话介绍

给你一份书单，自动找到最优购买方案。

## 功能亮点

- **电子版优先** — 自动查微信读书/得到覆盖情况，能看电子版就不花冤枉钱
- **全网比价** — 一键对比京东、当当、淘宝、拼多多四个平台的价格
- **促销时机分析** — 智能分析距离 618/双 11 还有几天，告诉你"现在买"还是"等大促"
- **书名自动解析** — "不要让我思考"自动识别为"点石成金"，不再搜不到书
- **中英双语触发** — "买书"或"buy books"都能唤起
- **零依赖开箱即用** — 纯 Python，无第三方库依赖

## 适用场景

- "帮我看看这几本书怎么买最划算"
- "这些书微信读书上有吗？"
- "618 快到了，现在是买书的好时机吗？"
- "I want to buy these books, find the best deal"

## 使用方法

### 快速开始

1. 检查单本书是否有电子版：

```bash
python scripts/check_digital.py --title "点石成金" --author "史蒂夫克鲁格"
```

2. 对比单本书的实体书价格：

```bash
python scripts/compare_prices.py --title "点石成金" --isbn "9787111640097"
```

3. 查看促销时机建议：

```bash
python scripts/compare_prices.py --sale-timing
```

### 批量使用

准备一个 JSON 文件 `books.json`：

```json
[
  {"title": "思考，快与慢", "author": "丹尼尔卡尼曼"},
  {"title": "点石成金", "author": "史蒂夫克鲁格", "isbn": "9787111640097"},
  {"title": "用户体验要素", "author": "加勒特", "isbn": "9787111616627"}
]
```

然后运行：

```bash
# 批量检查数字平台
python scripts/check_digital.py --batch books.json

# 批量比价
python scripts/compare_prices.py --batch books.json
```

## 文件结构

```
book-shopping-assistant/
├── SKILL.md              # 主流程指引（QoderWork Skill 格式）
├── reference.md          # 书名别名库、平台URL、促销规律
├── SKILL_MARKETING.md    # 营销文案（各平台提交用）
└── scripts/
    ├── check_digital.py       # 数字平台可用性检查
    └── compare_prices.py      # 电商比价 + 促销时机分析
```

## 技术说明

- Python 3，仅使用标准库（urllib、json、datetime），无第三方依赖
- SKILL.md 符合 [Agent Skills](https://skills.sh/) 开放标准

## License

MIT
