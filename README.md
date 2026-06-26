# Fan Perks Skills

- 默认语言：中文
- English version: [English](#english)

Fan Perks 面向 Agent 的 TKCPS Open API 技能仓库。

当前技能：

| Skill | 说明 |
| --- | --- |
| `fan-perks-open-api` | 搜索商品优惠、转换返利链接、读取会员 CPS 订单、读取佣金/账户概要、读取提现配置、提交提现申请、查询提现记录。 |

## 前置要求

- 已安装 Node.js 环境。
- 能够运行 `npx` 命令；如果你的 Agent 环境使用 Bun，也可以用 `bunx` 执行同类命令。
- 已在 Fan Perks 会员中心生成 API Key。

## 安装

提示：本仓库目前只收录 `fan-perks-open-api` 一个 skill。后续如果增加多个 skill，请按需安装你真正会用到的那几个；每个加载的 skill 都会在 Agent 每次运行时占用额外上下文。

### 快速安装（推荐）

```bash
npx skills add fthingapp/fan-perks-skills
```

如需显式指定 skill 目录：

```bash
npx skills add fthingapp/fan-perks-skills/skills/fan-perks-open-api
```

### 手动安装

```bash
git clone https://github.com/fthingapp/fan-perks-skills.git
mkdir -p "$CODEX_HOME/skills"
cp -R fan-perks-skills/skills/fan-perks-open-api "$CODEX_HOME/skills/"
```

## 发布到 ClawHub / OpenClaw

ClawHub 按“单个 skill”安装，不是把整个仓库一次性装进去。发布到 ClawHub 后，用户可以按需安装：

```bash
clawhub install fan-perks-open-api
```

发布到 ClawHub 的 skill 应按 ClawHub registry 规则声明许可与元数据；API Key 不应写入仓库。

## 注册插件市场

在 Agent 中运行：

```text
/plugin marketplace add fthingapp/fan-perks-skills
```

安装技能：

```text
/plugin install fan-perks-skills@fan-perks-skills
```

也可以直接告诉 Agent：

```text
请帮我安装 github.com/fthingapp/fan-perks-skills 中的 Skills
```

## 安装后配置

Fan Perks API base 固定为 `https://perks.fthing.cn/api`。请在 shell、Agent secret store 或服务端密钥库中设置会员 API Key：

```bash
export FAN_PERKS_API_KEY="fp_xxx"
```

辅助脚本只使用 Python 标准库：

```bash
python3 skills/fan-perks-open-api/scripts/fan_perks_client.py --help
```

## 仓库结构

```text
.
├── README.md
├── LICENSE
├── skills/
│   └── fan-perks-open-api/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/fan_perks_client.py
├── plugins/
│   └── fan-perks-skills/
│       ├── .codex-plugin/plugin.json
│       └── skills/fan-perks-open-api/
└── .agents/plugins/marketplace.json
```

## API Key 规则

- 不要提交 API Key、站点私有配置、生成的响应或本地日志。
- 不要把 API Key 放进浏览器代码、移动端客户端、截图、提示词或公开 issue 评论。
- 优先使用环境变量、Agent secret store 或服务端密钥库。
- 如果 API Key 泄露，请在 Fan Perks 会员 API 控制台重置。

## OpenAPI 和 MCP

Fan Perks 网站是完整 API 文档的唯一事实来源：

- OpenAPI 页面：`/open/tkcps`
- OpenAPI JSON：`https://perks.fthing.cn/api/open/tkcps/v1/openapi.json`
- MCP tools JSON：`https://perks.fthing.cn/api/open/tkcps/v1/mcp.json`

本 skill 是给 Agent 使用的轻量操作指南，不替代 OpenAPI 文档，也不包含任何私有凭据。

## 安全边界

Open API 只操作 API Key 绑定的会员账户。提现能力有意保持窄边界：API 可以提交提现申请，但不能审核、打款、取消、修复或编辑后台备注。提交提现申请前必须先由用户确认；同一会员同一时间只能存在一笔进行中的提现申请。

---

## English

- Default language: Chinese
- 中文版本: [中文](#fan-perks-skills)

Fan Perks agent skills for TKCPS Open API workflows.

Current skill:

| Skill | Description |
| --- | --- |
| `fan-perks-open-api` | Search deals, convert rebate links, read member CPS orders, read commission/account summaries, read withdraw config, submit withdraw applications, and list withdraw records. |

## Requirements

- Node.js is installed.
- The `npx` command is available; if your agent environment uses Bun, you can use `bunx` for equivalent commands.
- You have generated an API key in the Fan Perks member center.

## Installation

Note: this repository currently contains only one skill, `fan-perks-open-api`. If more skills are added later, install only the ones you actually need; each loaded skill consumes extra context on every agent run.

### Quick Install (Recommended)

```bash
npx skills add fthingapp/fan-perks-skills
```

To explicitly specify the skill directory:

```bash
npx skills add fthingapp/fan-perks-skills/skills/fan-perks-open-api
```

### Manual Install

```bash
git clone https://github.com/fthingapp/fan-perks-skills.git
mkdir -p "$CODEX_HOME/skills"
cp -R fan-perks-skills/skills/fan-perks-open-api "$CODEX_HOME/skills/"
```

## Publishing to ClawHub / OpenClaw

ClawHub installs individual skills, not the entire repository at once. After the skill is published to ClawHub, users can install it as needed:

```bash
clawhub install fan-perks-open-api
```

Skills published to ClawHub should declare license and metadata according to ClawHub registry rules. API keys must not be committed to the repository.

## Register the Plugin Marketplace

Run this in the agent:

```text
/plugin marketplace add fthingapp/fan-perks-skills
```

Install the skill:

```text
/plugin install fan-perks-skills@fan-perks-skills
```

You can also ask the agent directly:

```text
Please install the Skills from github.com/fthingapp/fan-perks-skills
```

## Configuration After Installation

The Fan Perks API base is fixed at `https://perks.fthing.cn/api`. Set the member API key in your shell, agent secret store, or server-side vault:

```bash
export FAN_PERKS_API_KEY="fp_xxx"
```

The helper script uses only the Python standard library:

```bash
python3 skills/fan-perks-open-api/scripts/fan_perks_client.py --help
```

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── skills/
│   └── fan-perks-open-api/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       ├── references/
│       └── scripts/fan_perks_client.py
├── plugins/
│   └── fan-perks-skills/
│       ├── .codex-plugin/plugin.json
│       └── skills/fan-perks-open-api/
└── .agents/plugins/marketplace.json
```

## API Key Rules

- Do not commit API keys, site-private configuration, generated responses, or local logs.
- Do not put API keys in browser code, mobile clients, screenshots, prompts, or public issue comments.
- Prefer an environment variable, agent secret store, or server-side vault.
- Reset the key in the Fan Perks member API console if it is exposed.

## OpenAPI and MCP

The Fan Perks website remains the source of truth for complete API documentation:

- OpenAPI page: `/open/tkcps`
- OpenAPI JSON: `https://perks.fthing.cn/api/open/tkcps/v1/openapi.json`
- MCP tools JSON: `https://perks.fthing.cn/api/open/tkcps/v1/mcp.json`

This skill is a lightweight operating guide for agents. It does not replace the OpenAPI documentation and does not include private credentials.

## Safety Boundary

The Open API only operates on the member account bound to the API key. Withdraw support is intentionally narrow: the API can submit a withdraw application, but it cannot approve, transfer, cancel, repair, or edit admin notes. A withdraw application must be confirmed by the user first, and one member can have only one in-progress withdraw application at a time.
