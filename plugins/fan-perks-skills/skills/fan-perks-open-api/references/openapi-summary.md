# Fan Perks TKCPS OpenAPI Summary

API base: `https://perks.fthing.cn/api`

Base path: `/api/open/tkcps/v1`

Authentication:

```http
Authorization: Bearer <api_key>
```

Compatible authentication:

```http
X-API-Key: <api_key>
```

Download full descriptors from the Fan Perks site:

- OpenAPI JSON: `https://perks.fthing.cn/api/open/tkcps/v1/openapi.json`
- MCP tools JSON: `https://perks.fthing.cn/api/open/tkcps/v1/mcp.json`

## Response Envelope

Success:

```json
{
  "code": 1,
  "msg": "SUCCESS",
  "data": {}
}
```

Failure:

```json
{
  "code": 0,
  "msg": "API key invalid",
  "data": { "error_code": "INVALID_API_KEY" }
}
```

Except for `RATE_LIMITED`, which may return HTTP 429, business failures usually return HTTP 200. Always check `code` and `data.error_code`.

## Endpoints

| Method | Path | Scope | Default | Quota | Purpose |
| --- | --- | --- | --- | --- | --- |
| GET | `/me` | `account:read` | on | 100/day | Current member profile, `commission`, points, growth value, member level, order stats, and API key validation |
| GET | `/goods/search` | `goods:read` | on | 300/day | Search product deals by keyword or URL; returns product references and estimated member rewards, without promotion links |
| POST | `/goods/convert` | `goods:convert` | on | 100/day | Generate a selected product deal link using product_ref or keyword + platform |
| GET | `/orders` | `order:read` | on | 100/day | Member CPS order list |
| GET | `/withdraw/list` | `withdraw:read` | on | 100/day | Withdraw records |
| POST | `/withdraw/apply` | `withdraw:apply` | off | 3/day | Submit withdraw application |

## Scopes

| Scope | Covers | Notes |
| --- | --- | --- |
| `goods:read` | `/goods/search` | Query only. Supports `keyword`, `platform`, `search_type`, `sort`, `cid`, `price`, `page`, and `page_size`; product_ref and member_commission_status are returned; promotion URLs are not returned. |
| `goods:convert` | `/goods/convert` | Generates current-member deal links; requires product_ref or one keyword input, and platform when ambiguous. Results are reused for ten minutes. |
| `account:read` | `/me` | Member identity, commission account summary, points, growth value, and member level. |
| `order:read` | `/orders` | Current member orders only; trade IDs are masked. |
| `withdraw:read` | `/withdraw/list` | Read-only withdraw records. |
| `withdraw:apply` | `/withdraw/apply` | High-risk scope. Off by default and must be enabled separately. |

## MCP Tools

The MCP descriptor exposes 6 tools:

- `search_deals`
- `convert_product_link`
- `get_current_member`
- `get_orders`
- `get_withdraw_records`
- `apply_withdraw`

For shopping workflows, call `search_deals`, let the user select a product, then call `convert_product_link` with its `product_ref` when they want to buy, copy, or share. An explicit request to convert a single URL or command may call conversion directly. Do not convert recommendations before the user selects one.

## Goods Search Parameters

`platform` values:

- `tb`: 淘宝
- `jd`: 京东

`search_type` values:

- Common: `quanwang` 全网搜索, `all` 全站领券, `dongdongqiang` 咚咚抢, `xiaoshi` 实时销量榜, `quantian` 全天销量榜, `shishi` 实时人气榜, `videos` 视频抖货, `yongjin` 红包排行, `pengyouquan` 朋友圈火爆, `price9` 9.9元, `price19` 19.9元, `high_commission` 超高红包, `today` 今日上新, `tmall` 天猫.
- TB only: `gold_seller` 金牌卖家, `taoqiangou` 淘抢购, `juhuasuan` 聚划算, `haitao` 天猫国际, `jiyoujia` 极有家, `tmall_market` 天猫超市.
- JD only: `jd_self` 京东自营, `jd_good_shop` 京东好店, `jd_pingou` 京东拼购, `jd_delivery` 京东配送, `jd_haitao` 京东国际, `jingxi` 京喜, `jd_market` 京东超市.

## Withdraw Application Rules

Rules:

- A member can have only one in-progress withdraw application.
- Pending audit, pending transfer, and transferring applications count as in-progress.
- Submit either `amount=10.00` or `withdraw_all=1`. `withdraw_all=1` uses the member's current withdrawable commission as the application amount.
- Before applying, call `/me` and check the available account `commission`.
- Business withdraw settings and Open API withdraw limits are enforced by `/withdraw/apply`; handle validation errors without retrying blindly.
- The API submits an application only. It does not approve or transfer funds.

## Error Codes

| Error code | HTTP | Meaning | Agent handling |
| --- | --- | --- | --- |
| `OPEN_API_DISABLED` | 200 | Platform Open API switch is off. | Stop and tell the user the site must enable Open API. |
| `ENDPOINT_DISABLED` | 200 | This endpoint is disabled. | Stop or choose a different endpoint. |
| `API_KEY_REQUIRED` | 200 | Missing auth header. | Ask for secret configuration, not public disclosure. |
| `INVALID_API_KEY` | 200 | Key does not exist, is disabled, or was reset. | Ask the user to verify/reset the key. |
| `SCOPE_DENIED` | 200 | Key lacks required scope. | Name the missing scope and direct user to API console. |
| `WITHDRAW_APPLY_DISABLED` | 200 | Withdraw application scope is not enabled. | Explain it is separate and high-risk. |
| `RATE_LIMITED` | 429 | Daily endpoint quota reached. | Do not keep retrying. |
| `SERVER_ERROR` | 200 | Server-side error. | Retry only safe reads; check withdraw records before retrying a withdraw application. |

## Examples

Validate key:

```bash
curl -H "Authorization: Bearer $FAN_PERKS_API_KEY" \
  "https://perks.fthing.cn/api/open/tkcps/v1/me"
```

Search deals:

```bash
curl -H "Authorization: Bearer $FAN_PERKS_API_KEY" \
  "https://perks.fthing.cn/api/open/tkcps/v1/goods/search?keyword=%E5%95%86%E5%93%81%E9%93%BE%E6%8E%A5"
```

Convert a product link:

```bash
curl -X POST "https://perks.fthing.cn/api/open/tkcps/v1/goods/convert" \
  -H "Authorization: Bearer $FAN_PERKS_API_KEY" \
  -d "keyword=https://example.com/item"
```

Apply withdraw:

```bash
curl -X POST "https://perks.fthing.cn/api/open/tkcps/v1/withdraw/apply" \
  -H "Authorization: Bearer $FAN_PERKS_API_KEY" \
  -d "amount=10.00"
```

Apply all withdrawable commission:

```bash
curl -X POST "https://perks.fthing.cn/api/open/tkcps/v1/withdraw/apply" \
  -H "Authorization: Bearer $FAN_PERKS_API_KEY" \
  -d "withdraw_all=1"
```

## Product query and conversion contract

Search responses contain `product_ref` (24-hour reference) and `member_commission_status=estimated|unknown`. Unknown amounts are omitted; a known zero amount is `0.00`. Search never returns `goods_url`, `goods_short_url`, or `tkl`.

Call `POST /api/open/tkcps/v1/goods/convert` only for a selected product, using `{ "product_ref": "<reference from search>" }`, or `{ "keyword": "<one product URL or command>", "platform": "jd" }`. Product names use search. Conversion returns `expires_at` as the service reuse deadline, not a guarantee of URL validity. Do not retry or generate alternative-platform links automatically.

Local-life activity venues (`eleme` / `meituan`) return `item_type=venue`. Generate their activity links only on an explicit open/share action, reusing the same member cache. They omit single-product prices and member reward amounts; do not promise Fan Perks order tracking, settlement, or cashback for these venues. Regular goods use `item_type=product`. Venue browsing needs no conversion or commission lookup.

## Taobao Authorization Before Reward Payout

`GET /api/open/tkcps/v1/orders` may return `reward_stage=waiting_taobao_auth`. Tell the member to complete personal Taobao authorization in Fan Perks member center. Deal lookup and purchase may happen first; reward payout requires a valid personal authorization. An already-authorized member skips this step. Previously attributed valid orders remain with the member and resume under their original settlement conditions after authorization, even when the authorized account changes the internal tracking relationship. Authorization does not restart the waiting period. Accelerator coupons also require authorization and are not consumed when authorization is missing. Invalid and already-paid order states take precedence. No new OpenAPI authorization endpoint is introduced; never ask users for internal tracking identifiers.
