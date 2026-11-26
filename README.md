# SKILLS

Three [Claude Code](https://claude.com/claude-code) skills for the N4 Studio Webflow workflow. Each one covers a step of a task:

```
task-intake    →    (build / fix the page)    →    handoff-qa    →    internal-log
start the task                                     check the page     post the daily update
```

- [task-intake](#task-intake)
- [handoff-qa](#handoff-qa)
- [internal-log](#internal-log)
- [Install](#install)

---

## task-intake

**Sets up a new task in under a minute, so every task starts with the same folder and context.**

### When to use it
At the start of any task. Paste the Productive ticket (description and comments), a Slack thread or a client message, or just say `new task #T10700`.

### What it does
1. **Works out the client** from the ticket's code (e.g. `ACME | Lead attribution issue`) and matches it to an existing client folder. If it isn't sure, it asks you.
2. **Creates the task folder:**
   ```
   N4 Studio/
   └── Acme/
       └── #T10688 - Lead attribution issue/
           ├── foundation/
           │   └── context.md     ← intake summary + the raw ticket
           ├── development/       ← code, section files, exports
           └── reference/         ← screenshots, PDFs, client files
   ```
3. **Writes `context.md`** with a short summary on top: the ask, scope, deliverables, people, due date, links, open questions and the first step. The original ticket is kept underneath, unchanged.
4. **Suggests the next step** for the type of task, e.g. scaffolding a section, debugging an animation or a page review.

If the task folder already exists, it opens it instead of creating a duplicate, and can add new ticket comments under `## Updates`.

### Try it
> `/task-intake` and paste the ticket
> "new task #T10700 for Acme: fix the hero on /about"

---

## handoff-qa

**Runs the pre-handoff QA checklist on a Webflow page and gives you a dashboard of only what still needs fixing.**

### When to use it
Before handing a page over, when a build or a round of fixes is done.

### What it checks
It checks only the page's `main` content (not the nav or footer):

| Area | Checks |
|---|---|
| Structure | HTML landmarks, one H1, no skipped heading levels |
| Media | Hero media, image sizes and formats, loading priority |
| Links | Link labels, screen-reader text, `aria-hidden` on decorative content |
| Code | CSS/JS embed order, unused `@media` rules, console errors, component props |
| Content | Missing alt text and aria-labels, typos, placeholder copy |
| Accessibility | 400% zoom, large text, keyboard access, axe DevTools |
| Performance | Lighthouse in incognito |

It uses everything it can reach: the Webflow Designer (via the Webflow MCP), the staging or live URL, and any local section files.

**The audit doesn't change anything.** It doesn't edit the site or your files; you make the fixes.

### What you get
A single HTML **QA dashboard** (`handoff-qa/<page>.html`) that you open in the browser:
- **One card per problem**, with where it is, what was expected, what was found and how to fix it
- **A status per item:** Fixed, False positive, Intentional, Pending client, Not my responsibility (with the team) or Needs discussion
- **Ignore** single items, a whole tab or a Lighthouse category
- **Notes** on each item. Your progress is saved in the browser.
- **Copy for Claude:** exports your statuses and notes so Claude can recheck your fixes, and so internal-log can use them

### Rechecks
Paste the **Copy for Claude** export back into Claude. It re-verifies everything you marked as fixed, marks each item as verified or still failing, adds any new problems, and updates the same dashboard. Items are never deleted, so the dashboard keeps the full history of what was found and fixed.

If the page passes everything, you get a short summary in chat instead of a dashboard.

### Try it
> "run handoff QA on https://example-staging.webflow.io/about"

---

## internal-log

**Writes the daily task update for Productive in the team's usual format, ready to paste.**

### When to use it
At the end of the work day on a task, finished or not.

### What it does
It drafts the update from:
- what was done in the Claude session
- your own notes (paste them in)
- the handoff-qa **Copy for Claude** export
- staging links, Lighthouse scores and attachments

And sorts each item into the right section:

| Section | What goes in it |
|---|---|
| `[COMPLETED]` | Work finished today: builds, fixes, CMS changes, research, guidance given |
| `[QA]` | Only when a QA round happened: what was checked and fixed |
| `[PENDING]` | Your own unfinished work, i.e. what you'll pick up next |
| `[TO CONFIRM]` | Questions or handoffs for the internal team or PM |
| `[CLIENT CONFIRMATION]` | Content, decisions or approvals needed from the client |

### What you get
One plain-text block, starting with `[UPDATE — DD/Mon]`, that you can paste straight into Productive. Each item is one short past-tense sentence ("Fixed…", "Updated…", "Built…"). Items you ignored in the QA dashboard are left out.

Ask for changes in plain words, e.g. "make it shorter" or "move X to pending", and it rewrites the whole block.

### Try it
> "write the internal log"
> "internal log for today, plus these notes: …"

---

## Install

```bash
git clone https://github.com/lucasnegri/SKILLS.git
cp -R SKILLS/task-intake SKILLS/handoff-qa SKILLS/internal-log ~/.claude/skills/
```

Restart Claude Code. Then call a skill by name (`/task-intake`, `/handoff-qa`, `/internal-log`) or just ask in plain words.

### Notes
- **task-intake** creates task folders under `~/Documents/Projects/N4 Studio`. To use a different folder, set the `N4_ROOT` environment variable.
- **handoff-qa** works best with the Webflow MCP connected and a browser available for axe DevTools and Lighthouse. Without them, those checks appear as manual items on the dashboard.
- Client names, people and URLs in the examples (Acme, Venue A, Product A, example-staging.webflow.io) are placeholders.
