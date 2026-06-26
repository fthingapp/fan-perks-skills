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
| GET | `/goods/search` | `goods:read` | on | 300/day | Search product deals by keyword or URL; returns converted deal URLs by default |
| POST | `/goods/convert` | `goods:convert` | on | 100/day | Convert product link or keyword into rebate links |
| GET | `/orders` | `order:read` | on | 100/day | Member CPS order list |
| GET | `/withdraw/list` | `withdraw:read` | on | 100/day | Withdraw records |
| POST | `/withdraw/apply` | `withdraw:apply` | off | 3/day | Submit withdraw application |

## Scopes

| Scope | Covers | Notes |
| --- | --- | --- |
| `goods:read` | `/goods/search` | Query only. Supports `keyword`, `platform`, `search_type`, `sort`, `cid`, `price`, `page`, and `page_size`; converted deal URLs are always returned. |
| `goods:convert` | `/goods/convert` | Generates current-member rebate links. |
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

For shopping workflows, call `convert_product_link` first with the user's product URL or keyword, then call `search_deals` with the same input for recommendations.

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
