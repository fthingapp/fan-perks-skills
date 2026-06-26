---
name: fan-perks-open-api
description: Use when an AI agent needs to call Fan Perks TKCPS open APIs for product deal search, product link conversion, member CPS orders, member commission/points/level lookup, withdraw applications, or withdraw record lookup. Requires a Fan Perks member API key.
---

# Fan Perks Open API

Use this skill to operate the Fan Perks TKCPS Open API on behalf of the member bound to the API key.

Fixed API base: `https://perks.fthing.cn/api`.

## Trigger Scenarios

- The user wants to search product deals, coupons, or CPS commission opportunities.
- The user wants to convert a product URL or keyword into a Fan Perks rebate link.
- The user asks about their CPS orders, commission status, red packet commission, points, growth value, or member level.
- The user wants to check current commission before withdrawing, submit a withdraw application, or list withdraw records.
- The user is configuring OpenAPI, MCP, OpenClaw, Hermes, Dify, LangChain, or a custom agent around Fan Perks.

## Required Inputs

- `api_key`: member API key generated in the Fan Perks member API console.

Optional inputs depend on the operation:

- `keyword`: product URL or keyword for deal search and product conversion.
- `amount`: withdraw amount, in yuan, for `apply_withdraw`.
- `withdraw_all`: set to `1` to apply for all currently withdrawable commission instead of passing `amount`.
- `page`, `limit`, `status`: list filters for orders or withdraw records.

Authenticate with either:

```http
Authorization: Bearer <api_key>
```

or:

```http
X-API-Key: <api_key>
```

## Safety Rules

- Never expose the full API key in chat, logs, PRs, screenshots, generated files, browser code, or mobile client bundles.
- Only query or act for the member bound to the API key.
- Do not ask for or store OpenID, phone number, payment account, full trade IDs, or other sensitive member data.
- Use the minimum scope needed for the task.
- Withdraw capability is limited to `apply_withdraw`; there is no API for audit, transfer, cancel, status repair, or admin notes.
- Before calling `apply_withdraw`, call `get_current_member`, check the current withdrawable `commission`, explain that the API only submits an application, and get explicit user confirmation for the amount or all-withdrawable amount.
- A member can have only one in-progress withdraw application. Do not submit another application while an existing one is pending audit, pending transfer, or transferring.

## Tool Mapping

Prefer these MCP-style operations:

| Tool | Method | Path | Scope |
| --- | --- | --- | --- |
| `search_deals` | GET | `/api/open/tkcps/v1/goods/search` | `goods:read` |
| `convert_product_link` | POST | `/api/open/tkcps/v1/goods/convert` | `goods:convert` |
| `get_current_member` | GET | `/api/open/tkcps/v1/me` | `account:read` |
| `get_orders` | GET | `/api/open/tkcps/v1/orders` | `order:read` |
| `get_withdraw_records` | GET | `/api/open/tkcps/v1/withdraw/list` | `withdraw:read` |
| `apply_withdraw` | POST | `/api/open/tkcps/v1/withdraw/apply` | `withdraw:apply` |

`GET /goods/search` accepts `keyword`, `platform`, `search_type`, `sort`, `cid`, `price`, `page`, and `page_size`. It always returns converted deal URLs.

Supported `platform` values:

- `tb`: 淘宝
- `jd`: 京东

Supported `search_type` values:

- Common: `quanwang` 全网搜索, `all` 全站领券, `dongdongqiang` 咚咚抢, `xiaoshi` 实时销量榜, `quantian` 全天销量榜, `shishi` 实时人气榜, `videos` 视频抖货, `yongjin` 红包排行, `pengyouquan` 朋友圈火爆, `price9` 9.9元, `price19` 19.9元, `high_commission` 超高红包, `today` 今日上新, `tmall` 天猫.
- TB only: `gold_seller` 金牌卖家, `taoqiangou` 淘抢购, `juhuasuan` 聚划算, `haitao` 天猫国际, `jiyoujia` 极有家, `tmall_market` 天猫超市.
- JD only: `jd_self` 京东自营, `jd_good_shop` 京东好店, `jd_pingou` 京东拼购, `jd_delivery` 京东配送, `jd_haitao` 京东国际, `jingxi` 京喜, `jd_market` 京东超市.

## Tool Calling Order

For shopping:

1. When the user gives a product URL or keyword, call `convert_product_link` first to get the primary rebate link.
2. Then call `search_deals` with the same input to provide recommended alternatives or similar deals.
3. Explain the relevant converted link, coupon, and estimated member commission fields.
4. Mention that commission is estimated until the CPS order settles.

For orders:

1. Call `get_orders` with the narrowest filters available.
2. Do not request or expose full trade IDs; rely on masked IDs and display fields.

For account and withdraw:

1. Call `get_current_member` for `commission`, points, growth value, member level, and order context.
2. Confirm amount or all-withdrawable amount and that the request only submits an application.
3. Call `apply_withdraw` with either `amount` or `withdraw_all=1`.
4. Use `get_withdraw_records` to show application status after submission.

## Error Handling

Successful responses use:

```json
{ "code": 1, "msg": "SUCCESS", "data": {} }
```

Failed responses use:

```json
{ "code": 0, "msg": "API key invalid", "data": { "error_code": "INVALID_API_KEY" } }
```

Handle common errors this way:

- `API_KEY_REQUIRED` or `INVALID_API_KEY`: ask the user to verify or reset the member API key. Do not ask them to paste the key into public chat if another secret channel exists.
- `SCOPE_DENIED`: tell the user which scope is missing and direct them to the API console.
- `WITHDRAW_APPLY_DISABLED`: explain that withdraw application is a separate high-risk scope and must be enabled first.
- `RATE_LIMITED`: stop retrying that endpoint for the day unless the user changes key or quota.
- `SERVER_ERROR`: retry only safe read operations; before retrying a withdraw application, check withdraw records because one member can have only one in-progress application.

Except `RATE_LIMITED`, which may return HTTP 429, business errors usually return HTTP 200 and must be judged by `code` and `data.error_code`.

## References

- Read `references/mcp-tools.json` when building OpenClaw, Hermes, or MCP tool adapters.
- Read `references/openapi-summary.md` when you need endpoint details, scopes, withdraw rules, and examples.
- Use `scripts/fan_perks_client.py` for quick manual calls from a shell. It uses only the Python standard library, calls `https://perks.fthing.cn/api`, and reads `FAN_PERKS_API_KEY`.
