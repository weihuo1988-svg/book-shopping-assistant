---
name: book-shopping-assistant
description: Help users find and purchase books with optimal pricing. Checks digital platforms (WeRead, Dedao) for e-book availability first, then compares physical book prices across e-commerce platforms (Taobao, JD, Dangdang). Analyzes upcoming sale events (618, Double 11) for best timing. Use when the user asks to buy books, find book prices, check if a book is available electronically, compare book prices, mentions 买书, 购书, 比价, 微信读书, 618, 双十一, buy books, book shopping, price compare books, e-book availability.
---

# Book Shopping Assistant

Help users acquire books at the best price by checking digital availability first, then comparing physical book prices across platforms.

## Workflow

Always follow this order:

```
Task Progress:
- [ ] Step 1: Parse book list and resolve Chinese titles/editions
- [ ] Step 2: Check digital platform availability
- [ ] Step 3: Search e-commerce prices for books needing physical copies
- [ ] Step 4: Analyze upcoming sale events
- [ ] Step 5: Generate purchase recommendation
```

### Step 1: Parse and Resolve Book Info

For each book, extract:
- Title (Chinese and English if applicable)
- Author
- Publisher
- Translator
- Edition

**Important**: Many books have different Chinese titles than their literal translation. Use `scripts/check_digital.py` to resolve title aliases.

```bash
python scripts/check_digital.py --title "不要让我思考" --author "史蒂夫克鲁格"
# May resolve to: "点石成金：访客至上的Web和移动可用性设计秘笈"
```

### Step 2: Check Digital Platforms

Run the digital check script:

```bash
python scripts/check_digital.py --title "书名" --author "作者" [--isbn "ISBN"]
```

This checks:
- **微信读书 (WeRead)**: https://weread.qq.com
- **得到 (Dedao)**: https://www.dedao.cn
- **京东读书 (JD Read)**: https://read.jd.com
- **Kindle/Amazon CN**: Note - Amazon CN Kindle store closed in 2023

The script returns the book's availability status and direct links for each platform.

For batch checking:

```bash
python scripts/check_digital.py --batch books.json
```

Where `books.json` is:
```json
[
  {"title": "思考，快与慢", "author": "丹尼尔卡尼曼"},
  {"title": "影响力", "author": "罗伯特西奥迪尼"}
]
```

**Output format to user**:
- Books available on digital platforms: list with links
- Books NOT available digitally: list with resolved correct title and ISBN

### Step 3: Search E-commerce Prices

For books NOT available digitally (or when user wants physical copies), compare prices across platforms.

Run the price comparison script:

```bash
python scripts/compare_prices.py --title "书名" --isbn "ISBN" [--publisher "出版社"]
```

This searches:
- **京东自营**: JD.com self-operated (best for authenticity guarantee)
- **当当**: Dangdang.com (book specialist, frequent promotions)
- **淘宝/天猫**: Taobao/Tmall (lowest prices, verify seller credibility)
- **拼多多**: Pinduoduo (budget option, caution on authenticity)

For batch comparison:

```bash
python scripts/compare_prices.py --batch need_to_buy.json
```

**Price collection strategy**:
1. Search using both Chinese title and ISBN for accuracy
2. Record: platform, price, seller type (self-operated vs third-party), discount rate
3. Identify the lowest credible price (prefer self-operated flagship stores)

**Present results as a comparison table**:

| 书名 | 定价 | 京东自营 | 当当自营 | 淘宝最低 | 推荐渠道 |
|------|------|---------|---------|---------|---------|
| 书名A | ¥79 | ¥56.90 | ¥55.00 | ¥50.00 | 当当自营 |

### Step 4: Analyze Sale Events

Check current date and determine proximity to major sale events.

Run:

```bash
python scripts/compare_prices.py --sale-timing
```

This returns:
- Current date
- Days until next major sale event
- Historical discount patterns for books

**Major sale events and typical book discounts**:

| Event | Period | Typical Book Discount | Strategy |
|-------|--------|----------------------|----------|
| **618** | May 13 - Jun 20 | 5折 + 每满100减50 | Best for books |
| **双11** | Oct 20 - Nov 11 | 5折 + 每满100减50 | Best for books |
| **双12** | Dec 1-12 | 每满100减30~40 | Moderate |
| **开学季** | Feb/Sep | 每满100减30 | Textbooks |
| **年货节** | Jan | 满减力度一般 | Not ideal |

**618/Dual-11 book pricing pattern**:
1. Books discounted to ~50% of list price
2. Stack with 每满100减50 coupon
3. Final price: ~25%-35% of list price

**Calculation example** (list price ¥79):
- 5折: ¥39.50
- 满100减50 (on ¥39.50 × 3 = ¥118.50): -¥50
- Final for 3 books: ¥68.50 → ~¥22.8/book
- vs daily price ~¥55/book → saves ~60%

### Step 5: Generate Recommendation

Produce a clear recommendation covering:

1. **Digital reading**: Which books can be read online (with links)
2. **Physical purchase**: Which books need buying, with price comparison
3. **Timing advice**: Buy now vs wait for next sale event
4. **Platform recommendation**: Where to buy (prioritize self-operated for authenticity)
5. **Search keywords**: Correct titles to use (resolve any naming differences)

**Output template**:

```markdown
## 可以电子阅读的书（X本）
1. 《书名》- 作者 / 平台：[微信读书](链接)

## 需要购买实体书的书（X本）

### 当前价格对比
| 书名 | 定价 | 京东 | 当当 | 淘宝 | 推荐 |
|------|------|------|------|------|------|
| ... | ... | ... | ... | ... | ... |

### 购买建议
- 现在买：总价约 ¥XXX
- 等618买：预估约 ¥XXX（省约 ¥XX）
- 建议：[等待/立即购买]

### 搜索关键词
- 《正确书名》ISBN: XXXXX
```

## Important Notes

- **Title resolution**: Many Chinese books have multiple names. Always resolve to the official published title before searching prices. Example: "不要让我思考" → "点石成金"
- **Edition matters**: Different editions have different ISBNs and prices. Confirm the exact edition.
- **Authenticity**: Recommend self-operated (自营/官方旗舰) stores for books to avoid pirated copies
- **Batch purchases**: When buying 3+ books, sale events offer much better value due to 满减 stacking
- **Digital first**: Always check WeRead first — it has the largest Chinese book catalog

## Additional Resources

- For detailed platform coverage and API details, see [reference.md](reference.md)
