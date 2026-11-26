---
name: handoff-qa
description: >-
  Run the pre-handoff QA on a Webflow page: HTML and heading structure, hero
  media, images, links and screen-reader text, embeds, component props, console
  output, missing alt and aria-labels, typos, 400% zoom, axe DevTools, and
  Lighthouse in incognito. Use when the user asks for handoff QA, a pre-handoff
  check, or to run the QA checklist. Write an interactive QA dashboard (one
  HTML file) of only the items that need revision, so they can be fixed,
  assigned, or ignored one by one.
user-invocable: true
---

# Handoff QA

Audit the page, then write a QA dashboard of what still needs revision. The user fixes each item manually. Do not edit the Webflow site, embeds, or project files as part of the audit.

## Scope

Every row runs on the main wrapper only: the `main` block, `#main`. Do not file findings in the navigation or the footer. Header, nav, and footer stay out of the checklist even on a whole-page pass.

If they limit the pass to one section, audit that section only, and it still has to sit inside `main`. Do not file full-page Lighthouse nodes that live outside `main`.

Their sheet legend says yellow rows apply only to projects in the internal system. Which rows are yellow is not recorded here. Run every row unless the user marks one out of scope.

## Evidence

Use every source that exists for this page:

1. Webflow Designer, when MCP is connected. Call `webflow_guide_tool` once per session before any other Webflow tool.
2. The published or staging URL in the browser.
3. Workspace `structure.html`, `styles.css`, and `script.js` when those files are the page under review.

If there is no URL and no Designer connection, audit the local files and leave the browser-only rows (runtime console, 400% zoom, large text, axe DevTools, Lighthouse) as manual checklist items.

## Checklist

Run every row. Judge pass, fail, partial, n/a, or manual.

| Category | Item | Details |
| --- | --- | --- |
| Structure | Check HTML Structure | Navigation - Main (with #main ID) with Sections - Footer |
| Structure | Check Heading Structure | Make sure there is only one H1 on the page. Very important to double-check if you are using Rich text as heading elements. Make sure headings are not skipped. |
| Media | Hero Image | Set to fetchpriority=high and loading=eager |
| Media | Hero Video | The same applies for Placeholder image as to the Hero Image. Make sure Hero video play on scroll is set to false if the video is in the hero section. |
| Media | Images | All images should have a set width and height. This is achieved by making every image sit within a container that has an aspect ratio or a specific size. All images should be an absolute 100% width and height. All images are to be converted to the WEBP format. Imported 2x the size of what’s in Figma. If images are small (logos, icons), make sure to disable responsiveness. |
| Links | Links | Make sure content of each link is set to aria-hidden=true. Social links is a good example where you will usually create a regular link block. In that case make sure svg is set to aria-hidden=true and link has aria-label=Facebook for example. Direct parent element of Clickable component must not have overflow hidden as focus will be clipped. In this situation nest one more div to fix this. Make sure to update Text for Screen readers from default Learn more about N4. |
| Code Quality | Console Logs | Make sure no console errors and logs. |
| Code Quality | Embed CSS and JS | CSS embed should always be first child of a section and JS embed must be last child of the section. Cleanup unsude media querries. |
| Code Quality | Components | Make sure all components have necessary properties. Use custom CSS to make sure they look good for client inside Designer view (.wf-design-mode .class {}). Add help text in same style as CMS. Important for Images! Make sure conditionals are working. Necessary properties examples: Heading, Heading Max Width, Button Text, Button Text SR, Button Link, etc. Add spacing options, themes and any other only when necessary. |
| Accessibility | 400% zoom and large text size | Check the site at 400% and text size large in browser settings. |
| Accessibility | axeDevTools | Run axeDevTools browser extension |
| Performance | Lighthouse | Run Lighthouse in Incognito mode. |

Then scan `main` for missing aria-labels, alt texts, and typos. Each hit is its own revision item. Skip the same issues in the nav and footer.

### How to judge

**Check HTML Structure.** Confirm `main` (`id="main"`) exists and the page sections sit inside it. Do not review or file the navigation or footer.

**Check Heading Structure.** One `h1`, and it lives in `main`. When a rich text field is used as a heading, read the tag it outputs. Do not skip levels inside `main`. Ignore headings in the nav and footer.

**Hero Image.** The hero `img` has `fetchpriority="high"` and `loading="eager"`. Other images stay lazy.

**Hero Video.** The placeholder image follows the hero image rule. If the video is in the hero, play on scroll is false.

**Images.** The parent has an aspect ratio or a set size. The image is absolute, 100% width, 100% height. Raster files are WebP. SVG icons can stay SVG. Pixel size is 2× the Figma frame. With no Figma frame in context, mark only the 2× part unverified. Logos and icons have responsiveness disabled (no srcset).

**Links.** Link content is `aria-hidden="true"` when the link has its own accessible name. A social link block keeps the svg `aria-hidden="true"` and sets `aria-label` to the network name, for example Facebook. The direct parent of a Clickable component must not have `overflow: hidden`. The fix is one extra wrapper div. Screen reader text must not stay on the default `Learn more about N4`.

**Console Logs.** No `console.*` left in embeds. No runtime errors after load. Quote the message.

**Embed CSS and JS.** The CSS embed is the first child of the section. The JS embed is the last child. "Cleanup unsude media querries" means remove unused `@media` rules. Flag them. Do not delete them during the audit.

**Components.** Props cover what the client edits. Examples: Heading, Heading Max Width, Button Text, Button Text SR, Button Link. Add spacing, themes, and other props only when that component needs them. Live CSS that hides an element needs a Designer override (`.wf-design-mode .class {}`) so the canvas still shows it. Image props need help text in the same style as that site's CMS help text. Each conditional branch shows and hides the right elements.

**400% zoom and large text size.** Check at 400% browser zoom and with the browser text size set to large. The automation stand-in for 400% zoom is a 320px-wide viewport (1280 at 400%). Look for clipped text, overlap, and content that only works by scrolling sideways. Large text cannot be set from automation. If you did not set it, keep it as a manual finding and write what the 320px pass showed.

**axeDevTools.** Run the extension. If it is not available in the automation browser, inject axe-core and run it on `main`. Each violation inside `main` is its own entry in `AXE_FINDINGS` (rule id, impact, WCAG criterion, one `nodes` entry per affected element). axe's "incomplete" results go in as `result:"incomplete"` (shown as Needs review). Drop violations whose node is in the nav or footer, and count them in `AXE.droppedOutsideMain`. If that run fails, set `AXE = null` and `AXE_FINDINGS = []`, and add one manual finding with `area:"axe"`: run axe DevTools on `main` and bring back the issues.

**Lighthouse.** Run it in Incognito so extensions and cache do not skew the score. The CLI stand-in is a fresh Chrome profile:

```bash
npx lighthouse "<url>" \
  --preset=desktop \
  --only-categories=performance,accessibility,best-practices \
  --chrome-flags="--incognito" \
  --output=json \
  --output-path=/tmp/handoff-lighthouse.json \
  --quiet
```

Put the three category scores, the five metrics (FCP, LCP, TBT, CLS, SI) and the passed-audit counts in `LH`. Each failed accessibility or best-practices audit is its own finding with `area:"lighthouse"` only when the node is inside `main`. For performance, file a finding only for a failed audit that affects `main` (LCP, CLS, unsized images, render-blocking). Skip minor opportunities. Skip any node in the nav or footer. Lighthouse's accessibility audits run on axe-core, so when one repeats an axe or checklist finding, keep it but set `dup` to the original (e.g. `"axe DevTools › color-contrast"`) and point its fix there. If Lighthouse cannot run, set `LH = null` and add one manual finding with `area:"lighthouse"`.

**Alt texts.** Flag a missing `alt`, a filename used as alt, and alts that only say "image" or "photo". `alt=""` is correct for a decorative image.

**Aria-labels.** Flag an icon-only link or button with no accessible name. This is in addition to the social-link rule above.

**Typos.** Read visible text, alt, aria-label, button text, and screen reader text. Quote the string and name the element. Skip brand names and intentional casing. Placeholder copy (lorem, TODO, internal notes) is a finding.

## What goes on the dashboard

| Status | Dashboard |
| --- | --- |
| pass (on the first audit) | Leave it out of findings. List it in `PASSING` as one short line. A finding that passes on a recheck stays on the list as `verified` (see Recheck). |
| n/a (pattern not on the page) | Omit |
| out of scope | Omit |
| fail, partial, manual | One finding per concrete problem |

Eight missing alts are eight findings. A category with no findings is hidden automatically.

If nothing needs revision, do not create a dashboard. Say the page passed and give the pass / n/a counts in chat.

## Dashboard

The template is `assets/dashboard-template.html` in this skill's directory. It is a single self-contained HTML file (dark dashboard, Chakra Petch from Google Fonts, no build step, no other network calls). Do not restyle it or change the code outside the data block.

1. Copy the template to `handoff-qa/<page-slug>.html` in the workspace. Create the folder if needed.
2. Replace everything between the `AUDIT DATA START` and `AUDIT DATA END` comments with this audit's data (keep both comment lines). The example data in the template shows every field; follow its shape exactly.
3. Open it in the browser, check the browser console is clean, and screenshot the Overview, Lighthouse and axe tabs to review them. Fix any data problem before handing it over.

### Data block

- `PAGE`: `name`, `slug` (kebab-case, also keys the saved progress, so keep it stable across rechecks), `url`, `scope` (`main#main`, or the section if the pass was limited), `date`, `pass` (`Pass 1`, `Pass 2`…).
- `AREAS`: keep the template's list and order. Checklist row → area key:

  | Checklist row | `area` |
  | --- | --- |
  | Check HTML Structure, Check Heading Structure | `structure` |
  | Hero Image, Hero Video, Images | `media` |
  | Links | `links` |
  | Console Logs, Embed CSS and JS, Components | `code` |
  | 400% zoom and large text size | `a11y` |
  | Alt texts, Aria-labels, Typos | `content` |
  | Lighthouse | `lighthouse` |
  | axeDevTools | `axe` (via `AXE_FINDINGS`) |

- `PASSING`: one line per checklist row that passed.
- `FINDINGS`: one object per problem. Findings are never deleted on later passes (see Recheck).
  - `id`: stable kebab-case, unique. Never reuse an id for a different problem.
  - `area`, `status` (`fail`, `partial`, `manual`), `rule` (the checklist row name).
  - `title` (one line), `where` (section › element, selectors in `<code>`).
  - `expected` and `found` (optional), `fix` (one line).
  - `lh` on Lighthouse findings: `cat` (`performance`, `accessibility`, `best-practices`), `audit` (Lighthouse audit id), `display` (e.g. `CLS 0.14`, `Est. savings 320 ms`), `r` (`good`, `avg`, `bad`), `help` (Chrome docs URL).
  - `dup` (optional): which other finding this repeats.
  - `verified` (optional, rechecks only): the pass that confirmed the fix, e.g. `"Pass 3"`. The template shows it as Fixed in any browser, adds a green "Verified" tag, and leaves it out of the "please re-verify" export. `AXE_FINDINGS` entries take it too.
- `LH`, `AXE`, `AXE_FINDINGS`: see the Lighthouse and axeDevTools rules above. `LH.insight` is one sentence on what holds the Performance score back.
- `HOWTO[id]` for every finding: `why` (one line), `steps` (ordered, written for Webflow Designer), optional `code`, optional `ref` `{label, url}`.

All values are HTML strings. Escape `<`, `>` and `&` in visible text. Never write a literal closing script tag inside the data; write `<\/script>`.

### What the user does with it

Everything below is built into the template. Do not reimplement it.

- **Status** per finding. Open: Open. Closed: Fixed, This is not an error, False positive, Intentional / won't fix. Pending: Pending client, Not my responsibility (asks for the responsible team), Needs discussion. The checkbox is a shortcut for Fixed.
- **Ignore** per finding, per tab, and per Lighthouse category. Ignored findings leave all counts and the export. Restore brings them back unchanged.
- **Notes** per finding, and **How to fix** panels from `HOWTO`.
- Progress is saved in the browser's localStorage, keyed by `PAGE.slug` and finding `id`. Claude can't read it. The user brings it back with **Copy for Claude**, which exports:

```
## PENDING: other teams
### <team>
- [id] title (where)
## PENDING: client
## PENDING: needs discussion
## Closed without a fix        (each line names the reason)
## Fixed by me (please re-verify)
## Notes on open items
(N ignored items left out on purpose. Don't add them to the internal log.)
```

The internal log skill reads the three PENDING sections. Ignored findings never appear in the export and must not be logged.

In chat, give the open / manual counts and the Lighthouse scores, and a markdown link to the dashboard file using its full absolute path. Do not paste the full finding list.

## Recheck

The user pastes the Copy for Claude export, or names items they fixed.

1. Re-verify each item under "Fixed by me" and "Closed without a fix", and any item the user names.
2. If it passes, keep it in `FINDINGS` and `HOWTO` and add `verified:"Pass N"` (the pass that confirmed it). Rewrite `found` as what was fixed and how you confirmed it, e.g. `Fixed (Pass 3): …`. Add a line to `PASSING` if that checklist row now passes. Items the user confirms by hand (manual rows you can't automate) get `verified` too, and `found` says it was confirmed by the user.
3. If it still fails, keep its `id` and update `found` and `fix`, and tell the user it's still failing so they reopen it.
4. Leave PENDING and ignored items alone. Add new problems with new ids.
5. Bump `PAGE.pass` and `PAGE.date`, keep `PAGE.slug`, rewrite the data block in the same file, and re-run Lighthouse and axe if the page changed.

Keeping the slug and ids means the user's saved statuses, notes and ignores carry over. Then tell them what changed: verified fixed, still failing, new.

**Never delete a finding.** Once an id is on the dashboard it stays there for good, so the history of what was found and fixed is kept for later. This applies to every pass and to every status: fixed, closed, pending, ignored. Never remove a finding's `HOWTO` either. Only the first audit decides what goes on the list (see "What goes on the dashboard"). After that, findings are only added or updated.
