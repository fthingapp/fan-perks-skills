---
name: fan-perks-open-api
description: Use when an AI agent needs to call Fan Perks TKCPS open APIs for product deal search, product link conversion, member CPS orders, commission/account summaries, withdraw configuration, withdraw applications, or withdraw record lookup. Requires a Fan Perks member API key.
---

# Fan Perks Open API

Use this skill to operate the Fan Perks TKCPS Open API on behalf of the member bound to the API key.

Fixed API base: `https://perks.fthing.cn/api`.

## Trigger Scenarios

- The user wants to search product deals, coupons, or CPS commission opportunities.
- The user wants to convert a product URL or keyword into a Fan Perks rebate link.
- The user asks about their CPS orders, commission status, account balance, or member level.
- The user wants to check withdraw limits, submit a withdraw application, or list withdraw records.
- The user is configuring OpenAPI, MCP, OpenClaw, Hermes, Dify, LangChain, or a custom agent around Fan Perks.

## Required Inputs

- `api_key`: member API key generated in the Fan Perks member API console.

Optional inputs depend on the operation:

- `keyword`: product URL or keyword for deal search and product conversion.
- `id`: order ID returned by `get_orders`.
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
- Before calling `apply_withdraw`, call `get_withdraw_config`, check returned limits and balance, explain that the API only submits an application, and get explicit user confirmation for the amount or all-withdrawable amount.
- A member can have only one in-progress withdraw application. Do not submit another application while an existing one is pending audit, pending transfer, or transferring.

## Tool Mapping

Prefer these MCP-style operations:

| Tool | Method | Path | Scope |
| --- | --- | --- | --- |
| `search_deals` | GET | `/api/open/tkcps/v1/goods/search` | `goods:read` |
| `convert_product_link` | POST | `/api/open/tkcps/v1/goods/convert` | `goods:convert` |
| `get_orders` | GET | `/api/open/tkcps/v1/orders` | `order:read` |
| `get_order_detail` | GET | `/api/open/tkcps/v1/orders/{id}` | `order:read` |
| `get_account_summary` | GET | `/api/open/tkcps/v1/account/summary` | `account:read` |
| `get_withdraw_config` | GET | `/api/open/tkcps/v1/withdraw/config` | `withdraw:read` |
| `get_withdraw_records` | GET | `/api/open/tkcps/v1/withdraw/list` | `withdraw:read` |
| `apply_withdraw` | POST | `/api/open/tkcps/v1/withdraw/apply` | `withdraw:apply` |

The OpenAPI documentation also exposes `GET /me` and `GET /goods/detail`; use them when the user needs key validation or a specific product detail.

## Tool Calling Order

For shopping:

1. Call `search_deals` with the user's product URL or keyword.
2. Explain the relevant deal, coupon, and estimated commission fields.
3. Call `convert_product_link` only when the user wants a rebate link or the workflow explicitly requires conversion.
4. Return the converted link and mention that commission is estimated until the CPS order settles.

For orders:

1. Call `get_orders` with the narrowest filters available.
2. Use `get_order_detail` only for an order ID returned by `get_orders`.
3. Do not request or expose full trade IDs; rely on masked IDs and display fields.

For account and withdraw:

1. Call `get_account_summary` for balance and commission context.
2. Call `get_withdraw_config` before discussing a withdraw application.
3. Confirm amount or all-withdrawable amount, limits, fees, and that the request only submits an application.
4. Call `apply_withdraw` with either `amount` or `withdraw_all=1`.
5. Use `get_withdraw_records` to show application status after submission.

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
