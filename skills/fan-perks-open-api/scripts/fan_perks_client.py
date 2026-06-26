#!/usr/bin/env python3
"""Small Fan Perks Open API client.

This helper intentionally uses only Python standard-library modules so it can be
copied into agent sandboxes without installing third-party dependencies.

Environment:
  FAN_PERKS_API_KEY   Member API key generated in the API console
"""

import argparse
import json
import os
import sys
from urllib import error, parse, request

API_BASE_URL = "https://perks.fthing.cn/api"
PLATFORMS = ("tb", "jd")
SEARCH_TYPES = (
    "quanwang", "all", "dongdongqiang", "xiaoshi", "quantian", "shishi", "videos", "yongjin",
    "pengyouquan", "price9", "price19", "high_commission", "today", "tmall",
    "gold_seller", "taoqiangou", "juhuasuan", "haitao", "jiyoujia", "tmall_market",
    "jd_self", "jd_good_shop", "jd_pingou", "jd_delivery", "jd_haitao", "jingxi", "jd_market",
)


def call(api_key, method, path, data=None):
    url = API_BASE_URL.rstrip("/") + "/open/tkcps/v1" + path
    body = None
    headers = {"Authorization": f"Bearer {api_key}"}
    clean_data = {k: v for k, v in (data or {}).items() if v not in ("", None)}
    if method == "GET" and clean_data:
        url += "?" + parse.urlencode(clean_data)
    if method == "POST":
        body = parse.urlencode(clean_data).encode()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = request.Request(url, data=body, headers=headers, method=method)
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def require_value(parser, value, option, tool):
    if value in ("", 0, None):
        parser.error(f"{option} is required for {tool}")


def main():
    parser = argparse.ArgumentParser(
        description="Call Fan Perks TKCPS Open API tools without third-party dependencies."
    )
    parser.add_argument("tool", choices=[
        "search_deals",
        "convert_product_link",
        "get_current_member",
        "get_orders",
        "get_withdraw_records",
        "apply_withdraw",
    ])
    parser.add_argument("--api-key", default=os.getenv("FAN_PERKS_API_KEY", ""), help="Member API key or FAN_PERKS_API_KEY")
    parser.add_argument("--keyword", default="", help="Product URL or search keyword")
    parser.add_argument("--platform", choices=PLATFORMS, default="", help="Goods search platform: tb or jd")
    parser.add_argument("--search-type", choices=SEARCH_TYPES, default="", help="Goods search type")
    parser.add_argument("--sort", default="", help="Goods search sort option")
    parser.add_argument("--cid", default="", help="Goods category ID")
    parser.add_argument("--price", default="", help="Goods price filter")
    parser.add_argument("--page-size", type=int, default=20, help="Goods search page size, maximum 50")
    parser.add_argument("--amount", default="", help="Withdraw amount, for example 10.00")
    parser.add_argument("--withdraw-all", action="store_true", help="Apply to withdraw all currently withdrawable commission")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--status", default="", help="Withdraw status filter")
    parser.add_argument("--withdraw-type", default="", help="Withdraw type filter, for example wechat")
    parser.add_argument("--tk-status", default="", help="Order TK status filter")
    parser.add_argument("--commission-settled", default="", help="Order commission settled filter")
    parser.add_argument("--commission-status", default="", help="Order commission status filter")
    parser.add_argument("--start-time", default="", help="Order paid start date, Y-m-d")
    parser.add_argument("--end-time", default="", help="Order paid end date, Y-m-d")
    args = parser.parse_args()

    if not args.api_key:
        parser.error("--api-key/FAN_PERKS_API_KEY is required")

    if args.tool in ("search_deals", "convert_product_link"):
        require_value(parser, args.keyword, "--keyword", args.tool)
    if args.tool == "apply_withdraw" and not args.withdraw_all:
        require_value(parser, args.amount, "--amount", args.tool)

    mapping = {
        "search_deals": ("GET", "/goods/search", {
            "keyword": args.keyword,
            "platform": args.platform,
            "search_type": args.search_type,
            "sort": args.sort,
            "cid": args.cid,
            "price": args.price,
            "page": args.page,
            "page_size": args.page_size,
        }),
        "convert_product_link": ("POST", "/goods/convert", {"keyword": args.keyword}),
        "get_current_member": ("GET", "/me", {}),
        "get_orders": ("GET", "/orders", {
            "page": args.page,
            "limit": args.limit,
            "keyword": args.keyword,
            "tk_status": args.tk_status,
            "commission_settled": args.commission_settled,
            "commission_status": args.commission_status,
            "start_time": args.start_time,
            "end_time": args.end_time,
        }),
        "get_withdraw_records": ("GET", "/withdraw/list", {
            "page": args.page,
            "limit": args.limit,
            "status": args.status,
            "withdraw_type": args.withdraw_type,
        }),
        "apply_withdraw": ("POST", "/withdraw/apply", {
            "amount": args.amount,
            "withdraw_all": 1 if args.withdraw_all else 0,
        }),
    }
    method, path, data = mapping[args.tool]
    try:
        result = call(args.api_key, method, path, data)
    except error.HTTPError as exc:
        payload = exc.read().decode()
        try:
            result = json.loads(payload)
        except json.JSONDecodeError:
            result = {"code": 0, "msg": payload or str(exc), "data": {"http_status": exc.code}}
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
