# Fan Perks Skills

English | [中文](README.md)

Fan Perks agent skills for TKCPS Open API workflows.

Current skill:

| Skill | Description |
| --- | --- |
| `fan-perks-open-api` | Search deals, convert rebate links, read member CPS orders, read member commission/points/level data, submit withdraw applications, and list withdraw records. |

## Requirements

- Node.js is installed.
- The `npx` command is available; if your agent environment uses Bun, you can use `bunx` for equivalent commands.
- You have generated an API key in the Fan Perks member center. Visit [https://perks.fthing.cn](https://perks.fthing.cn), sign in, then generate or copy the API key from the member center.

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

The Fan Perks API base is fixed at `https://perks.fthing.cn/api`. You can get the API key from the Fan Perks member center after signing in at [https://perks.fthing.cn](https://perks.fthing.cn). Set the member API key in your shell, agent secret store, or server-side vault:

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
├── README.en.md
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
