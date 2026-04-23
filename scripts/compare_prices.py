#!/usr/bin/env python3
"""
Compare book prices across Chinese e-commerce platforms.

Platforms:
- 京东自营 (JD.com self-operated)
- 当当 (Dangdang)
- 淘宝/天猫 (Taobao/Tmall)

Usage:
    python compare_prices.py --title "点石成金" --isbn "9787111640097"
    python compare_prices.py --title "用户体验要素" --publisher "机械工业出版社"
    python compare_prices.py --batch need_to_buy.json
    python compare_prices.py --sale-timing
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

# Known book database with list prices
LIST_PRICES = {
    "9787111640097": {"title": "点石成金（第3版）", "price": 79},
    "9787111616627": {"title": "用户体验要素（第2版）", "price": 79},
    "9787121269325": {"title": "洞察人心", "price": 65},
}

# Sale event calendar (month-day ranges)
SALE_EVENTS = [
    {
        "name": "618年中大促",
        "start": (5, 13),
        "end": (6, 20),
        "discount": "5折 + 每满100减50",
        "book_discount_rate": 0.25,  # ~25% of list price
    },
    {
        "name": "双11",
        "start": (10, 20),
        "end": (11, 11),
        "discount": "5折 + 每满100减50",
        "book_discount_rate": 0.25,
    },
    {
        "name": "双12",
        "start": (12, 1),
        "end": (12, 12),
        "discount": "每满100减30~40",
        "book_discount_rate": 0.40,
    },
    {
        "name": "年货节",
        "start": (1, 10),
        "end": (1, 25),
        "discount": "满减力度一般",
        "book_discount_rate": 0.55,
    },
    {
        "name": "开学季(春)",
        "start": (2, 15),
        "end": (3, 5),
        "discount": "每满100减30",
        "book_discount_rate": 0.50,
    },
    {
        "name": "开学季(秋)",
        "start": (8, 20),
        "end": (9, 10),
        "discount": "每满100减30",
        "book_discount_rate": 0.50,
    },
]

# Typical daily discount rates by platform
DAILY_DISCOUNT = {
    "京东自营": 0.72,  # ~72% of list price (28% off)
    "当当自营": 0.70,  # ~70% of list price (30% off)
    "淘宝/天猫": 0.65,  # ~65% of list price (35% off)
    "拼多多": 0.60,  # ~60% of list price (40% off)
}


def days_until_sale(sale):
    """Calculate days until the next occurrence of a sale event."""
    now = datetime.now()
    year = now.year
    start_month, start_day = sale["start"]
    end_month, end_day = sale["end"]

    start_date = datetime(year, start_month, start_day)
    end_date = datetime(year, end_month, end_day)

    if now > end_date:
        # Sale has passed this year, calculate for next year
        start_date = datetime(year + 1, start_month, start_day)

    days = (start_date - now).days
    return max(0, days), start_date


def get_next_sale():
    """Find the next upcoming major sale event."""
    results = []
    for sale in SALE_EVENTS:
        days, date = days_until_sale(sale)
        results.append({**sale, "days_until": days, "start_date": date.isoformat()})

    results.sort(key=lambda x: x["days_until"])
    return results


def estimate_sale_price(list_price, discount_rate):
    """Estimate price during a sale event."""
    return round(list_price * discount_rate, 2)


def estimate_daily_price(list_price, platform):
    """Estimate current daily price on a platform."""
    rate = DAILY_DISCOUNT.get(platform, 0.70)
    return round(list_price * rate, 2)


def search_price(title, isbn=None, publisher=None):
    """Search for book prices across platforms.

    Since e-commerce sites block automated scraping, this function:
    1. Returns estimated prices based on typical discount patterns
    2. Provides direct search URLs for manual verification
    3. Uses known book database if ISBN matches
    """
    list_price = None
    resolved_title = title

    if isbn and isbn in LIST_PRICES:
        list_price = LIST_PRICES[isbn]["price"]
        resolved_title = LIST_PRICES[isbn]["title"]
    elif title in LIST_PRICES:
        list_price = LIST_PRICES[title]["price"]

    # If list price unknown, agent should search manually
    if list_price is None:
        return {
            "resolved_title": resolved_title,
            "list_price": "需确认",
            "platforms": {},
            "search_urls": {
                "京东自营": f"https://search.jd.com/Search?keyword={urllib.parse.quote(title)}&enc=utf-8",
                "当当自营": f"https://search.dangdang.com/?key={urllib.parse.quote(title)}&medium=01",
                "淘宝": f"https://s.taobao.com/search?q={urllib.parse.quote(title)}",
            },
            "note": "List price unknown. Use search URLs to find current prices.",
        }

    # Generate estimated prices
    platforms = {}
    for platform, rate in DAILY_DISCOUNT.items():
        platforms[platform] = {
            "estimated_price": estimate_daily_price(list_price, platform),
            "list_price": list_price,
            "discount": f"{rate:.0%} of list",
        }

    return {
        "resolved_title": resolved_title,
        "list_price": list_price,
        "platforms": platforms,
        "search_urls": {
            "京东自营": f"https://search.jd.com/Search?keyword={urllib.parse.quote(resolved_title)}&enc=utf-8",
            "当当自营": f"https://search.dangdang.com/?key={urllib.parse.quote(resolved_title)}&medium=01",
            "淘宝": f"https://s.taobao.com/search?q={urllib.parse.quote(resolved_title)}",
        },
    }


def analyze_sale_timing():
    """Analyze current timing relative to upcoming sales."""
    now = datetime.now()
    next_sales = get_next_sale()

    output = {
        "current_date": now.isoformat(),
        "next_sales": next_sales[:3],  # Next 3 sales
        "recommendation": "",
    }

    # Find the best upcoming book-buying opportunity
    for sale in next_sales:
        if sale["days_until"] <= 7:
            output["recommendation"] = (
                f"{sale['name']} starts in {sale['days_until']} days! "
                f"Wait and buy during the sale. Expected discount: {sale['discount']}"
            )
            break
        elif sale["days_until"] <= 30:
            output["recommendation"] = (
                f"{sale['name']} is {sale['days_until']} days away. "
                f"If not urgent, wait for better prices. "
                f"Expected: ~{sale['book_discount_rate']:.0%} of list price"
            )
            break
    else:
        output["recommendation"] = (
            "No major sale events in the next 3 months. "
            "Buy now if needed, or wait for the next 618/Dual-11."
        )

    return output


def compare_batch(books):
    """Compare prices for multiple books."""
    results = []
    for book in books:
        title = book.get("title", "")
        isbn = book.get("isbn")
        publisher = book.get("publisher")
        results.append(search_price(title, isbn, publisher))
    return results


def print_price_table(results):
    """Print a markdown price comparison table."""
    if not results:
        return

    print("| 书名 | 定价 | 京东自营 | 当当自营 | 淘宝/天猫 | 拼多多 |")
    print("|------|------|---------|---------|---------|--------|")

    for r in results:
        title = r["resolved_title"]
        list_price = r.get("list_price", "?")
        platforms = r.get("platforms", {})

        jd = platforms.get("京东自营", {}).get("estimated_price", "?")
        dd = platforms.get("当当自营", {}).get("estimated_price", "?")
        tb = platforms.get("淘宝/天猫", {}).get("estimated_price", "?")
        pdd = platforms.get("拼多多", {}).get("estimated_price", "?")

        lp = f"¥{list_price}" if isinstance(list_price, (int, float)) else str(list_price)
        print(f"| {title} | {lp} | ¥{jd} | ¥{dd} | ¥{tb} | ¥{pdd} |")

    print()


def print_sale_analysis(analysis):
    """Print sale timing analysis."""
    print(f"当前日期: {analysis['current_date'][:10]}")
    print()
    print(" upcoming 促销节点:")
    for sale in analysis.get("next_sales", []):
        print(f"  - {sale['name']}: {sale['start_date'][:10]} ({sale['days_until']}天后)")
        print(f"    优惠: {sale['discount']}")
        print(f"    图书预估到手: ~{sale['book_discount_rate']:.0%} of 定价")
    print()
    print(f"建议: {analysis['recommendation']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Compare book prices across Chinese e-commerce platforms"
    )
    parser.add_argument("--title", type=str, help="Book title")
    parser.add_argument("--isbn", type=str, help="ISBN number")
    parser.add_argument("--publisher", type=str, help="Publisher name")
    parser.add_argument("--batch", type=str, help="JSON file with list of books")
    parser.add_argument("--sale-timing", action="store_true",
                        help="Show upcoming sale events and timing advice")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if args.sale_timing:
        analysis = analyze_sale_timing()
        if args.json:
            print(json.dumps(analysis, ensure_ascii=False, indent=2))
        else:
            print_sale_analysis(analysis)
        return

    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            books = json.load(f)
        results = compare_batch(books)
    elif args.title:
        results = [search_price(args.title, args.isbn, args.publisher)]
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_price_table(results)

        # If multiple books, calculate total
        if len(results) > 1:
            totals = {"京东自营": 0, "当当自营": 0, "淘宝/天猫": 0, "拼多多": 0}
            count = 0
            for r in results:
                for platform in totals:
                    price = r.get("platforms", {}).get(platform, {}).get("estimated_price", 0)
                    if isinstance(price, (int, float)):
                        totals[platform] += price
                        count += 1
            if count > 0:
                print("### 总计")
                for platform, total in totals.items():
                    if total > 0:
                        print(f"  {platform}: ¥{total:.2f}")


if __name__ == "__main__":
    main()
