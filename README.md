# Fan Perks Skills

Fan Perks agent skills for TKCPS Open API workflows.

Current skill:

| Skill | Description |
| --- | --- |
| `fan-perks-open-api` | Search deals, convert rebate links, read member CPS orders, read commission/account summaries, read withdraw config, submit withdraw applications, and list withdraw records. |

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

The Fan Perks site is fixed at `https://perks.fthing.cn/`. Set the member API key in your shell, agent secret store, or server-side vault:

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
- OpenAPI JSON: `/open/tkcps/v1/openapi.json`
- MCP tools JSON: `/open/tkcps/v1/mcp.json`

This skill is a lightweight operating guide for agents. It does not replace the OpenAPI documentation and does not include private credentials.

## Safety Boundary

The Open API only operates on the member account bound to the API key. Withdraw support is intentionally narrow: the API can submit a withdraw application, but it cannot approve, transfer, cancel, repair, or edit admin notes. A withdraw application must be confirmed by the user first and must include a unique `Idempotency-Key`.
