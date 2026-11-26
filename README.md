# SKILLS

Claude Code skills for the N4 Studio Webflow workflow.

| Skill | What it does |
|---|---|
| [`task-intake`](task-intake/) | Starts a task from a Productive ticket, Slack thread or client message: finds the client, creates `N4 Studio/<Client>/#T<id> - <Task name>/` with `foundation/`, `development/` and `reference/`, and writes `foundation/context.md` (intake summary + raw ticket). Opens the folder if it already exists. |
| [`handoff-qa`](handoff-qa/) | Runs the pre-handoff QA checklist on a Webflow page (structure, media, links, embeds, component props, console, alt/ARIA, typos, 400% zoom, axe DevTools, Lighthouse) and builds an interactive dashboard of only the items that need fixing, with a "Copy for Claude" export. |
| [`internal-log`](internal-log/) | Writes the daily Productive update: `[UPDATE — DD/Mon]` with `[COMPLETED]`, `[QA]`, `[PENDING]`, `[TO CONFIRM]` and `[CLIENT CONFIRMATION]`, from the session's work, your notes and the handoff-qa export. |

## Install

```bash
git clone https://github.com/lucasnegri/SKILLS.git
cp -R SKILLS/task-intake SKILLS/handoff-qa SKILLS/internal-log ~/.claude/skills/
```

Restart Claude Code, then type `/task-intake`, `/handoff-qa` or `/internal-log` (or just ask, e.g. "new task #T10700", "run handoff QA", "write the internal log").

## Before you use them

- **internal-log** is written in Lucas's voice and refers to him by name. Replace "Lucas" in `internal-log/SKILL.md` with your own name.
- **task-intake** uses `~/Documents/Projects/N4 Studio` as the root. Set the `N4_ROOT` environment variable to use a different folder.
- Names in the examples (Acme, Venue A, Product A, example-staging.webflow.io) are placeholders.
