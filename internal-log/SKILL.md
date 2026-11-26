---
name: internal-log
description: >-
  Write the daily internal log (the task update posted on Productive) for the
  work done on a task: [UPDATE — DD/Mon] header, then [COMPLETED], [QA],
  [PENDING], [TO CONFIRM] and [CLIENT CONFIRMATION] sections in plain text, in
  the user's own voice. Pulls from what was done in the session, the user's notes, the
  handoff-qa "Copy for Claude" export, and links. Use when the user asks for the
  internal log, the log, the update for today, the Productive update, or to
  "log what I did", at the end of a work day or when closing a task.
---

# Internal log

At the end of each work day on a task (closed or not), the user posts an update on the task in **Productive**. This skill writes that update: same format, written in the user's own voice, ready to paste.

> **Hard rule: the log only contains work from the task where the skill is being used.** Every item must come from this session or from what the user gave for this task (notes, pasted export, links). Nothing from `references/examples.md`, nothing from older logs, nothing from other projects or other sessions, even when the work looks similar. If an item can't be traced to this task, it doesn't go in.

`references/examples.md` shows the **format and voice only** (structure, sentence shape, level of detail). Its first example is the **length benchmark**; the older ones below it are more detailed than wanted, so take only their structure. Read it before the first log of a session, then write the log from scratch. Never copy its items, names, numbers, pages, people, URLs or issue IDs.

## 1. Gather the material

**Scope:** the task being worked on right now, in this session and this project folder. If the session touched more than one task or project, ask which one the log is for (or offer one log per task). Earlier conversations and other projects are out of scope unless the user pastes them.

Use everything available for that task, in this order:

1. **This session:** what was actually built, fixed, checked, decided or found. Use tool results and files changed, not intentions. Something attempted but not finished is not COMPLETED.
2. **What the user pasted or said:** notes, a quick list, the client's message, issue numbers.
3. **The handoff-qa export** ("Copy for Claude" from the QA dashboard), if pasted. Map it with the table below.
4. **Links:** staging, branch or preview URLs of the pages worked on; the QA dashboard file if it's being attached.

If the session has nothing to log (fresh session, no notes), ask for a quick brain-dump: what got done, what's left, what's blocked and on whom. One question, not a form.

Don't invent work, numbers or names. If a count or URL isn't known, leave it out or ask. If there's very little to log, the log is short; never pad it.

## 2. The format

```
[UPDATE — 12/Nov]

[COMPLETED]

First completed item, one short sentence.

Second completed item.

[QA]

QA item.

[PENDING]

Pending item.

[TO CONFIRM]

Confirm whether …

[CLIENT CONFIRMATION]

Confirm whether …

Page preview:

https://…
```

- **Header:** `[UPDATE — DD/Mon]` (with the em dash) and today's date from `date "+%d/%b"` (e.g. `12/Nov`, `30/Oct`). Always included.
- **Plain text only.** Section labels in uppercase square brackets. One item per paragraph, a blank line between items, and a single blank line between sections. No bullets, no bold, no markdown, no emoji.
- **Section order:** `[COMPLETED]` → `[QA]` → `[PENDING]` → `[TO CONFIRM]` → `[CLIENT CONFIRMATION]` → closing lines. **Omit any section with nothing in it.** A log can be just `[COMPLETED]`.
- **Several pages or areas in one job:** sub-labels inside the section, one line each, with the items directly under them and no blank line between them:

```
[COMPLETED]

[PRODUCT A]
Updated icon labels, category titles, headings, and supporting copy across the PRODUCT A page.
Removed outdated sections and restructured the Intro page.
Issues solved: #7, #8, #9.

[PRODUCT B]
Fixed the trail animation on the services list on mobile.
Issues solved: #12, #13, #14.
```

## 3. What goes where

| Section | Holds | Who owns it |
| --- | --- | --- |
| `[COMPLETED]` | Work finished today: builds, fixes, CMS changes, scripts, research and findings, guidance given to someone, recommendations made | Done |
| `[QA]` | Only when a QA round happened: what QA checked and fixed (accessibility, images, embeds, Lighthouse, axe). Otherwise QA work goes in COMPLETED | Done |
| `[PENDING]` | **The user's own** unfinished work: what's left because the work day ended, the next steps they'll pick up tomorrow | The user |
| `[TO CONFIRM]` | **Internal**: questions for the team or PM, decisions to align on, work handed to another internal team | The team |
| `[CLIENT CONFIRMATION]` | **Waiting on the client**: content, assets, approvals, decisions, answers | The client |

Judgement calls:

- Something only the user can continue → PENDING, even if it's large.
- The user can't continue until the client sends or decides something → CLIENT CONFIRMATION, and if there's work for the user after that, a PENDING item too ("Populate the FAQs once the client sends the content").
- A doubt about whether something is intended (e.g. a page already live on production) → TO CONFIRM as a direct question.
- Waiting on another internal team (Development, Design, SEO…) → TO CONFIRM, naming the team: "Development team to fix the focus trap on the cloned marquee links."

### The handoff-qa export

| Export section | Log section | How to write it |
| --- | --- | --- |
| Fixed by me | `[QA]` (or COMPLETED if no QA round) | One item per fix or group of similar fixes, past tense |
| Closed without a fix (not an error, false positive, intentional) | `[QA]` | Group them: "Reviewed the flagged X; confirmed not an error because…" Only when the reason is useful to the reader |
| PENDING: client | `[CLIENT CONFIRMATION]` | What the client has to send or decide |
| PENDING: other teams | `[TO CONFIRM]` | "\<Team> team to …", one item per finding or group |
| PENDING: needs discussion | `[TO CONFIRM]` | As a question |
| Notes on open items / open items | `[PENDING]` | Next step the user will take |
| Ignored items | Nothing | Never mentioned, never logged |

Group related findings into one item instead of one line per finding ("Fixed accessibility issues across heading hierarchy, landmarks, link labels, and axe errors"). Mention the QA dashboard as an attachment when the user will attach it.

## 4. The voice

- **COMPLETED and QA items** start with a past-tense verb: Fixed, Updated, Implemented, Built, Created, Reviewed, Investigated, Conducted, Refined, Optimized, Cleaned up, Preserved, Documented, Provided, Recommended, Suppressed, Added, Removed, Resolved.
- **Short and outcome-first.** One sentence per item (two only when the second adds a finding the reader needs), about 12–25 words. Say what was done and the result, not how it was done.
- **No implementation detail.** Leave out class names, selectors, attributes, file names, breakpoints in em/px, pixel measurements, code behavior, before → after strings, test widths and states. The reader is the PM and team, not a developer reading the diff. ❌ "A global Starter rule makes every button full width below 62em, so the button overflowed the card by about 150px…" ✅ "Fixed tablet/mobile role card layouts, resolving button overflow, title spacing, and chip wrapping."
- **Merge related work** into one item (one item for the whole layout fix, not one per symptom). Aim for about 5 COMPLETED items on a full day; more only when the work really covers separate areas.
- **Don't log the routine:** testing and verification passes, re-checks, file housekeeping, and small follow-up tweaks made inside work that's already logged.
- **Keep the useful specifics:** a count that matters ("the job board API has 2 open roles, while the page displayed only 1"), real page and section names, issue numbers.
- **Say why only when a reviewer would question it**, in a few words, not a paragraph.
- **Short asides in parentheses** only when they change how the item reads: "(DESKTOP ONLY)".
- **Uppercase for emphasis** (DESKTOP, MOBILE), never formatting.
- **People** by first name (Anna, Ben) when they were involved.
- **PENDING items** are short, imperative or a noun phrase, and only real remaining work (not "paste the embed" or "do a final check"): "Build the See Inside tabs and FAQs.", "Review MOBILE responsiveness for the sections built today.", "Page metadata (SEO title, description, 1200×630 cover image)."
- **TO CONFIRM items** are one short line, with no background or explanation of the options: "Confirm whether to …", a direct action for the team ("Add the staging domain to the cookie banner allow-list."), or "\<Team> team to …".
- **CLIENT CONFIRMATION items** are one short line saying what the client has to send or decide: "Confirm whether …", "Client to send …".
- Professional and factual, never salesy, no filler ("successfully", "seamlessly").
- Fix spelling and grammar, keep the user's voice. Write in English even when the session is in another language.

## 5. Closing lines (when relevant)

After the last section, each separated by a blank line:

- `Page preview:` followed by each staging URL on its own line. For a branch: `Page handoff (still branched): <url>`.
- `Page is ready to be reviewed again.` when the work is back with the reviewer.
- `Issues solved: #7, #8, #9.` or `Result: Solved IL-02 and IL-12 as per task request.` when the task tracks issue numbers.
- `Lighthouse: Performance 98, Accessibility 86, Best Practices 73` (with an aside if a score is low for a known reason).
- `Attached on this message there is also a .html file with all of the points that were checked/fixed/solved.` when the QA dashboard goes with the log.

## 6. Deliver

- Check before handing over: every item traces back to this task (if one reminds you of an example log, delete it); date is today; every section non-empty; items in the right section by owner; nothing ignored is mentioned; no markdown slipped in; no invented numbers; every item is one short sentence with no class names, selectors, pixel values or code detail. If an item reads like a changelog for developers, cut it down.
- Output the log in **one plain code block** (so it copies cleanly into Productive), and nothing else except, if needed, one line below it listing anything you left out or weren't sure about.
- Don't save it to a file unless asked.
- If the user asks to adjust it ("make it shorter", "move X to pending"), rewrite the whole block.
