# Reference: Book Shopping Assistant

## Title Alias Database

Many Chinese books are known by multiple names. Always resolve before searching.

| Common Name | Official Published Title | Author | ISBN | Publisher | List Price |
|-------------|------------------------|--------|------|-----------|-----------|
| 不要让我思考 | 点石成金：访客至上的Web和移动可用性设计秘笈（原书第3版） | 史蒂夫·克鲁格 | 9787111640097 | 机械工业出版社 | ¥79 |
| 别让我思考 | 点石成金（同上） | 史蒂夫·克鲁格 | 9787111640097 | 机械工业出版社 | ¥79 |
| Don't Make Me Think | 点石成金（同上） | Steve Krug | 9787111640097 | 机械工业出版社 | ¥79 |
| 点石成金（第2版） | 点石成金：访客至上的网页设计秘笈（原书第2版） | 史蒂夫·克鲁格 | 9787111494553 | 机械工业出版社 | ¥49 |
| 访谈法 | 洞察人心：用户访谈成功之道 | Steve Portigal | 9787121269325 | 电子工业出版社 | ¥65 |
| Interviewing Users | 洞察人心（同上） | Steve Portigal | 9787121269325 | 电子工业出版社 | ¥65 |

### Psychology & Behavioral Economics Books (WeRead Coverage)

| Book | WeRead | ISBN | Publisher |
|------|--------|------|-----------|
| 思考，快与慢 | ✅ | 9787508633558 | 中信出版社 |
| 影响力（全新升级版） | ✅ | 9787550267527 | 北京联合出版公司 |
| 心理学与生活（第19/20版） | ✅ (第20版) | 9787115558923 | 人民邮电出版社 |
| 上瘾 | ✅ | 9787508668093 | 中信出版社 |
| 助推（终极版） | ✅ | 9787521713787 | 中信出版社 |
| 福格行为模型 | ✅ | 9787521729115 | 中信出版社 |
| 驱动力 | ✅ | 9787213047961 | 浙江人民出版社 |
| 掌控谈话 | ✅ | 9787550267510 | 北京联合出版公司 |
| 不要让我思考/点石成金 | ❌ | - | - |
| 用户体验要素 | ❌ | - | - |
| 访谈法/洞察人心 | ❌ | - | - |

## Platform Search URLs

### 京东 (JD.com)
- Search: `https://search.jd.com/Search?keyword={keyword}&enc=utf-8`
- Self-operated filter: Add `&evtype=3` for 自营
- Product page: `https://item.jd.com/{product_id}.html`

### 当当 (Dangdang)
- Search: `https://search.dangdang.com/?key={keyword}&medium=01`
- Product page: `http://product.dangdang.com/{product_id}.html`

### 淘宝 (Taobao)
- Search: `https://s.taobao.com/search?q={keyword}`
- Product page: `https://item.taobao.com/item.htm?id={item_id}`

### 微信读书 (WeRead)
- Search: `https://weread.qq.com/web/search/global?keyword={keyword}`
- Book detail: `https://weread.qq.com/web/bookDetail/{book_id}`

## Historical Sale Patterns for Books

### 618 (June 18)
- **Timeline**: May 13 - June 20
- **Key dates**:
  - May 13-31: Pre-sale / early access
  - June 1-3: First wave (开门红) — often best prices
  - June 15-18: Final wave
- **Book promo pattern**:
  - Base price: 5折 (50% of list)
  - Stack: 每满100减50 (¥50 off per ¥100)
  - PLUS members: extra coupons
- **Effective discount**: ~25-35% of list price
- **Best for**: 3+ books (to maximize 满减 stacking)

### 双11 (November 11)
- **Timeline**: October 20 - November 11
- **Key dates**:
  - Oct 20-31: Pre-sale
  - Nov 1-3: First wave
  - Nov 10-11: Final wave
- **Same discount pattern as 618**
- **Effective discount**: ~25-35% of list price

### 双12 (December 12)
- **Timeline**: December 1-12
- **Discount**: 每满100减30~40
- **Effective discount**: ~40-50% of list price
- **Not as good as 618/双11**

### 开学季 (Back to School)
- **Timeline**: Feb 15 - Mar 5, Aug 20 - Sep 10
- **Discount**: 每满100减30
- **Best for**: Textbooks and academic books

## Price Estimation Formula

For books with known list price:

```
Daily price ≈ List Price × 0.65-0.75

618/双11 price ≈ List Price × 0.25-0.35
  = (List Price × 0.5) - (满100减50 contribution)

Example for ¥79 book:
  Daily: ¥79 × 0.72 ≈ ¥57
  618: ¥79 × 0.5 = ¥39.50
       Buy 3 = ¥118.50 → -¥50 = ¥68.50
       Per book: ¥22.83
```

## Authenticity Tips

1. **京东自营** (JD self-operated): Most reliable for genuine books
2. **当当自营** (Dangdang self-operated): Very reliable
3. **天猫出版社旗舰店**: Publisher's official Tmall store, reliable
4. **淘宝第三方**: Check seller rating (≥4.8), reviews, and return policy
5. **Avoid**: Prices significantly below 40% of list outside of major sales

## Batch Input Format

```json
[
  {
    "title": "思考，快与慢",
    "author": "丹尼尔·卡尼曼",
    "publisher": "中信出版集团"
  },
  {
    "title": "点石成金",
    "author": "史蒂夫·克鲁格",
    "isbn": "9787111640097"
  }
]
```
