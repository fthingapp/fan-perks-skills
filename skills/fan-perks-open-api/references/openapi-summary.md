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
| GET | `/me` | `account:read` | on | 100/day | Current member profile and API key validation |
| GET | `/goods/search` | `goods:read` | on | 300/day | Search product deals by keyword or URL |
| GET | `/goods/detail` | `goods:read` | on | 300/day | Product detail, price, coupon, and commission fields |
| POST | `/goods/convert` | `goods:convert` | on | 100/day | Convert product link or keyword into rebate links |
| GET | `/account/summary` | `account:read` | on | 100/day | Commission account, order stats, member level |
| GET | `/orders` | `order:read` | on | 100/day | Member CPS order list |
| GET | `/orders/{id}` | `order:read` | on | 100/day | Member CPS order detail |
| GET | `/withdraw/config` | `withdraw:read` | on | 100/day | Withdraw config, balance, methods, business limits, and Open API limits |
| GET | `/withdraw/list` | `withdraw:read` | on | 100/day | Withdraw records |
| POST | `/withdraw/apply` | `withdraw:apply` | off | 3/day | Submit withdraw application |

## Scopes

| Scope | Covers | Notes |
| --- | --- | --- |
| `goods:read` | `/goods/search`, `/goods/detail` | Query only. |
| `goods:convert` | `/goods/convert` | Generates current-member rebate links. |
| `account:read` | `/me`, `/account/summary` | Member identity and commission account summary. |
| `order:read` | `/orders`, `/orders/{id}` | Current member orders only; trade IDs are masked. |
| `withdraw:read` | `/withdraw/config`, `/withdraw/list` | Read-only withdraw information. |
| `withdraw:apply` | `/withdraw/apply` | High-risk scope. Off by default and must be enabled separately. |

## MCP Tools

The MCP descriptor exposes 8 tools:

- `search_deals`
- `convert_product_link`
- `get_orders`
- `get_order_detail`
- `get_account_summary`
- `get_withdraw_config`
- `get_withdraw_records`
- `apply_withdraw`

`GET /me` and `GET /goods/detail` are available in OpenAPI but are not part of the default 8 MCP tools.

## Withdraw Application Rules

Rules:

- A member can have only one in-progress withdraw application.
- Pending audit, pending transfer, and transferring applications count as in-progress.
- Submit either `amount=10.00` or `withdraw_all=1`. `withdraw_all=1` uses the member's current withdrawable commission as the application amount.
- Before applying, call `/withdraw/config` and verify `open_api_withdraw_apply_enabled`, `single_max_amount`, `open_api_limits.daily_count`, `open_api_limits.daily_amount`, `open_api_limits.single_max_amount`, minimum amount, fee, and available balance.
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
