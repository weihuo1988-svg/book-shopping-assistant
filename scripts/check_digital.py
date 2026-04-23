#!/usr/bin/env python3
"""
Check if a book is available on Chinese digital reading platforms.

Platforms checked:
- 微信读书 (WeRead): https://weread.qq.com
- 得到 (Dedao): https://www.dedao.cn

Usage:
    python check_digital.py --title "思考快与慢" --author "丹尼尔卡尼曼"
    python check_digital.py --title "影响力" --author "西奥迪尼" --isbn "9787550267527"
    python check_digital.py --batch books.json
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import re

# Known Chinese book title aliases: common_name -> official_published_name
TITLE_ALIASES = {
    "不要让我思考": "点石成金",
    "别让我思考": "点石成金",
    "Don't Make Me Think": "点石成金",
    "访谈法": "洞察人心",
    "Interviewing Users": "洞察人心",
    "Steve Portigal": "洞察人心",
    "波蒂加尔": "洞察人心",
}

# Book metadata database for quick lookup
KNOWN_BOOKS = {
    "点石成金": {
        "title": "点石成金：访客至上的Web和移动可用性设计秘笈（原书第3版）",
        "author": "史蒂夫·克鲁格",
        "publisher": "机械工业出版社",
        "isbn": "9787111640097",
        "price": 79,
    },
    "用户体验要素": {
        "title": "用户体验要素：以用户为中心的产品设计（原书第2版）",
        "author": "杰西·詹姆斯·加勒特",
        "publisher": "机械工业出版社",
        "isbn": "9787111616627",
        "price": 79,
    },
    "洞察人心": {
        "title": "洞察人心：用户访谈成功之道",
        "author": "Steve Portigal",
        "publisher": "电子工业出版社",
        "isbn": "9787121269325",
        "price": 65,
    },
}


def resolve_title(title):
    """Resolve a book title to its official published Chinese name."""
    # Direct match
    if title in KNOWN_BOOKS:
        return title, KNOWN_BOOKS[title]

    # Check aliases
    for alias, official in TITLE_ALIASES.items():
        if alias.lower() in title.lower() or title.lower() in alias.lower():
            if official in KNOWN_BOOKS:
                return official, KNOWN_BOOKS[official]
            return official, None

    return title, None


def search_weread(title, author=None):
    """Search for a book on WeRead (微信读书)."""
    # WeRead search URL pattern
    keywords = title
    if author:
        keywords = f"{title} {author}"

    url = f"https://weread.qq.com/web/search/global?keyword={urllib.parse.quote(keywords)}"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://weread.qq.com/",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        books = data.get("books", [])
        if books:
            book = books[0]
            book_id = book.get("bookInfo", {}).get("bookId", "")
            title_found = book.get("bookInfo", {}).get("title", "")
            author_found = book.get("bookInfo", {}).get("author", "")
            return {
                "available": True,
                "title": title_found,
                "author": author_found,
                "url": f"https://weread.qq.com/web/bookDetail/{book_id}",
            }
        return {"available": False}
    except Exception as e:
        return {"available": "error", "error": str(e)}


def search_dedao(title, author=None):
    """Search for a book on Dedao (得到)."""
    # Dedao doesn't have a public search API, so we use web search as fallback
    # This is a simplified check - in practice, use WebFetch or WebSearch tool
    return {"available": "manual_check", "note": "Search on https://www.dedao.cn manually"}


def check_book(title, author=None, isbn=None):
    """Check digital availability for a single book."""
    resolved_title, known_info = resolve_title(title)

    result = {
        "input_title": title,
        "input_author": author,
        "resolved_title": resolved_title,
        "known_info": known_info,
        "platforms": {},
    }

    # Check WeRead
    result["platforms"]["微信读书"] = search_weread(resolved_title, author)

    # Check Dedao (manual)
    result["platforms"]["得到"] = search_dedao(resolved_title, author)

    return result


def check_batch(books):
    """Check digital availability for multiple books."""
    results = []
    for book in books:
        title = book.get("title", "")
        author = book.get("author")
        isbn = book.get("isbn")
        results.append(check_book(title, author, isbn))
    return results


def print_result(result):
    """Format and print the check result."""
    title = result["resolved_title"]
    if result["input_title"] != title:
        print(f"  书名解析: \"{result['input_title']}\" → \"{title}\"")

    if result["known_info"]:
        info = result["known_info"]
        print(f"  完整书名: {info['title']}")
        print(f"  ISBN: {info['isbn']}")
        print(f"  定价: ¥{info['price']}")

    for platform, status in result["platforms"].items():
        if status["available"] is True:
            print(f"  ✅ {platform}: 《{status.get('title', title)}》")
            if status.get("url"):
                print(f"     {status['url']}")
        elif status["available"] is False:
            print(f"  ❌ {platform}: 未找到")
        elif status["available"] == "error":
            print(f"  ⚠️  {platform}: 查询失败 ({status.get('error', 'unknown')})")
        elif status["available"] == "manual_check":
            print(f"  🔍 {platform}: {status.get('note', '需手动确认')}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Check if a book is available on Chinese digital reading platforms"
    )
    parser.add_argument("--title", type=str, help="Book title (Chinese or English)")
    parser.add_argument("--author", type=str, help="Book author")
    parser.add_argument("--isbn", type=str, help="ISBN number")
    parser.add_argument("--batch", type=str, help="JSON file with list of books")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            books = json.load(f)
        results = check_batch(books)
    elif args.title:
        results = [check_book(args.title, args.author, args.isbn)]
    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print_result(result)


if __name__ == "__main__":
    main()
