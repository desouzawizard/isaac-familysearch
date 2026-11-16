# isaac-familysearch — genealogy research skills for Claude

Ten **Agent Skills** that teach Claude how to do Brazilian, Portuguese and Italian
genealogical research on FamilySearch and its partner archives: which URLs and APIs
actually work, what a zero result does and does not prove, how to read a handwritten
register page, and which edits silently fail to save.

Each one is hard-won procedural knowledge from real research sessions, not general
advice. The warnings are there because something broke.

**New here? Start with [QUICKSTART.md](QUICKSTART.md)** — what to do in your first
session, and how to begin from what you already know rather than from a search box.

---

## Part 1 — For the user

### What a skill is

A folder with a `SKILL.md` inside. The file has YAML frontmatter (`name` and
`description`) and then markdown instructions. Claude reads the descriptions of every
enabled skill cheaply, and loads the full instructions only when a task matches — so
having all ten on costs almost nothing until one is needed.

### How to install them

**claude.ai (web, desktop, mobile)** — skills upload one at a time, as ZIPs.

1. Turn on **Create and edit files** (code execution) in **Settings → Capabilities**.
   Skills run in the sandbox and will not appear without it.
2. Zip a single skill folder so `SKILL.md` sits at the top level inside it:
   ```bash
   cd skills && zip -r familysearch-tree-and-hints.zip familysearch-tree-and-hints
   ```
3. Go to **Customize → Skills**, click **+**, then **+ Create skill → Upload a skill**,
   and pick the ZIP.
4. Repeat per skill. Each then appears in the list with a toggle.

The folder name must match the `name` in the frontmatter, or the upload is rejected.

**Claude Code (terminal)** — filesystem, no upload:

```bash
cp -r skills/* ~/.claude/skills/              # available everywhere
# or, per project:
cp -r skills/* /path/to/project/.claude/skills/
```

**Cowork and cloud sessions** do *not* read `~/.claude/skills/`. They load whatever is
enabled on the claude.ai account, so a skill that only exists on a local disk will come
back "not found" in a scheduled task. Upload it to claude.ai for those.

**Claude API** — `POST /v1/skills`, then pass `{"type": "custom", "skill_id": "..."}` in
the request's `container.skills`. Max 8 skills per request, 8 MB per upload.

Skills do **not** sync between surfaces. claude.ai, the API and Claude Code are three
separate installs of the same folder.

### What they need to work

- **A signed-in FamilySearch session in the browser Claude is driving.** Most of these
  call `familysearch.org` endpoints from the page context. If the API starts returning
  503 with HTML, the session expired — sign in again. Claude will not enter credentials.
- **A browser Claude can drive** — Claude in Chrome, or the desktop app's built-in
  browser. These are not web-search skills; they operate the live site.
- **JavaScript execution on the page**, for the `fetch` and DOM-extraction recipes.
- `familysearch-ordinance-requests` additionally reserves temple ordinances on the
  account, which is a real action under FamilySearch's Reservation Policy. It asks for
  scope and consent before clicking anything.

### Two things that are gated, and one that goes stale

**Temple ordinances.** `familysearch-ordinance-requests` is only usable by members of The
Church of Jesus Christ of Latter-day Saints, through a FamilySearch account linked to
membership. For anyone else the Ordinances tab has nothing to reserve. The other eight
skills need nothing but a free FamilySearch account.

**Partner subscriptions.** FamilySearch's partners (Ancestry, MyHeritage, Findmypast and
the rest) are free *to subscribe to* only for Church members — the JOIN FOR FREE buttons
sit behind that gate. `genealogy-partner-sites` is built around this: its URL recipes work
on the partners' free public pages, which anyone can read, and it never signs up or signs
in. So the skill is useful to everybody; the free subscriptions are not.

**Measured coverage goes stale.** `familysearch-fulltext-sweep` carries coverage figures
measured in November 2026, and `familysearch-compiled-sources` a dated test log. Both are
dated on purpose. Treat them as a starting expectation, not a current fact — re-run the
control search rather than trusting a number that may be a year old.

### What generalizes beyond Brazil

| Skill | Portable? |
|---|---|
| `familysearch-tree-and-hints` | **Yes** — FamilySearch mechanics, hint triage, editing traps are the same everywhere |
| `familysearch-fulltext-sweep` | **Yes** — the API and its traps are global; the measured coverage figures are Brazil-specific |
| `familysearch-catalog-and-images` | **Yes** — catalog → film → page → attach works for any filmed archive |
| `familysearch-compiled-sources` | **Yes** — Digital Library, Genealogies and Cemeteries are global |
| `familysearch-platform-api-reads` | **Yes** — the `/platform` API is global; the jurisdiction example is Brazilian |
| `genealogy-research-audit` | **Yes** — the nine checks are country-agnostic |
| `familysearch-ordinance-requests` | **Yes**, within the membership gate above |
| `newspaperarchive-search` | **Mostly** — the URL grammar is general; NewspaperArchive's own holdings are strongest for the US |
| `genealogy-partner-sites` | **Partly** — recipes are general, the measured coverage is Brazil, Portugal and Italy |
| `brazilian-genealogy-search` | **No** — Brazilian corpora, record formulas and naming culture throughout |

Researching somewhere else? The first seven transfer unchanged. Replace
`brazilian-genealogy-search` with the equivalent knowledge for your own archives, and
keep its structure: a control word per record type, a spelling ladder, and where filiation
lives in that country's records.

---

## Part 2 — For the Claude session

Read this before starting genealogy work in this repo's domain.

### Routing — which skill for which problem

| The situation | Load |
|---|---|
| Any navigating, reading or editing of the Family Tree; triaging Record Hints or Research Suggestions | `familysearch-tree-and-hints` |
| A search returned zero, or two terms must co-occur, or a record set must be proven absent | `familysearch-fulltext-sweep` |
| A record should exist but name search *and* full-text find nothing | `familysearch-catalog-and-images` |
| Checking for a duplicate before creating a person; what a place was called on a date; pulling a family in one call; watching a profile for edits | `familysearch-platform-api-reads` |
| The ancestor is Brazilian; or records of enslaved or freed people are in scope | `brazilian-genealogy-search` |
| A name has stalled in the record index; an obituary or a death date is wanted | `newspaperarchive-search` |
| Looking for published genealogies, local histories, cemeteries, another researcher's tree | `familysearch-compiled-sources` |
| Checking whether Ancestry, MyHeritage, Geneanet and the rest hold anything, without paying | `genealogy-partner-sites` |
| Picking up prior research, writing a handoff, or stalled and unsure why | `genealogy-research-audit` |
| Reserving ordinances for a list of ancestors | `familysearch-ordinance-requests` |

If a session also has an older `familysearch-tree-operations` enabled, ignore it:
`familysearch-tree-and-hints` is a strict superset and was removed from this repo to stop
the two competing for the same trigger.

### The rules that cut across all of them

1. **A zero result proves nothing until the corpus is proven searchable.** Run a control
   search for a word that must appear on every page of that record type. An unverified
   negative is not a finding, and writing one down as a wall wastes the next session.
2. **Full-text matching is literal at the word level.** No fuzzy spelling. Quoting does
   not force adjacency. Spelling variants must be enumerated and tried.
3. **A hint, an index entry and an OCR transcript are leads, not evidence.** Open the
   image. Evaluate a hint on the *other people named on the record*, never on the
   principal's name (that was the matcher's input) and never on its confidence score.
4. **Nothing from a compiled source, a submitted tree or a partner site reaches the tree
   without confirmation on a primary image.**
5. **Every fact gets `Reason This Information Is Correct`,** carrying the
   original-language quotation and the ark. A fact without one is an assertion.
6. **Verify every save.** Re-read the fact list. Several FamilySearch dialogs accept a
   programmatic value, enable SAVE, and store nothing.
7. **Check the family list before adding anyone.** On a well-worked couple the children
   usually already exist.
8. **Log rejections.** Write down who was rejected and why, so the next session does not
   re-find them.
9. **The registry district is not the event place.** A catalogue path names the serventia
   that kept the book. If the act's place field is blank, the place is unknown.

### Repo layout

```
README.md          what you are reading
QUICKSTART.md      first-session guide for a new researcher
CONTRIBUTING.md    how to add or change a skill
Makefile           make check | make zips
skills/
  brazilian-genealogy-search/SKILL.md
  familysearch-catalog-and-images/SKILL.md
  familysearch-compiled-sources/SKILL.md
  familysearch-fulltext-sweep/SKILL.md
  familysearch-ordinance-requests/SKILL.md
  familysearch-platform-api-reads/SKILL.md
  familysearch-tree-and-hints/SKILL.md
  genealogy-partner-sites/SKILL.md
  genealogy-research-audit/SKILL.md
  newspaperarchive-search/SKILL.md
```

---

## Part 3 — The skills

### `familysearch-tree-and-hints`
*The main FamilySearch skill — 249 lines.* Navigating, searching and editing the Family
Tree, plus triage of auto-generated hints. Holds the URL patterns that work, the
portrait-pedigree and relationship endpoints, the large-tree viewfinder and Options
badges, and the hint-system inversion worth knowing: Record Hints cluster on
well-documented people because matching needs data to match on, while Research
Suggestions cluster on thin people because the rules fire on absence — so neither points
at what is actually hard. Also: why two hints with identical confidence can be one clean
and one a different person entirely, why the *rejected* pile deserves reading, how to
read a handwritten image past the viewer's zoom cap by reading neighbouring act numbers
instead of magnifying further, why a certified transcript is independent evidence rather
than a copy, and a table of editing traps that each silently lost a save.

### `familysearch-fulltext-sweep`
*312 lines.* Calls the full-text search API directly instead of scraping the
client-rendered results page — one `fetch` in place of a navigate plus a ten-second wait,
and it returns each document's full page OCR. Covers the deep-paging ceiling and
partitioning a corpus into sub-1,000 slices, the place facet as a coverage test, the
co-occurrence sweep as the only reliable AND, triage without opening the viewer, finding
the clerical formula before trusting a name search, and measured coverage outside Rio de
Janeiro. Also: scoping a search to one film with `groupName`, and why a wrong film number
returns a silent zero.

### `familysearch-catalog-and-images`
*245 lines.* The pipeline for records no index reaches: jurisdiction → catalog → film →
page → attach. Access rights in film lists, the Images API over GraphQL with a bearer
token, locating a page by date within a film, reading DeepZoom tiles directly to get past
the viewer's zoom cap, and checking the tree before declaring a find. Written for the
case where the image exists but was never indexed, or was indexed under a mangled name —
a Genzano birth indexed as *Parisi* for *Passeri*. Also warns that a catalog's *place* is
a claim: one "Rio de Janeiro" parish film turned out to be Minas Gerais.

### `familysearch-platform-api-reads`
*104 lines.* The documented `/platform` API, called read-only from a signed-in tab with the
user's own session: tree search as a duplicate check before Add Child or Add Spouse,
family and pedigree pulls, the change feed to find collaborators, conditional GETs to
notice when a profile is edited, the places API for what a town was called (and which
seat held its records) on a given date, and date standardizing before a vitals save. The
traps: per-resource Accept headers, errors that live in the `Warning` header, `q.*` terms
that score rather than filter. Human pace; stops on any 403, 429 or licence notice.

### `brazilian-genealogy-search`
*237 lines.* Brazilian records specifically. Opens with the prime directive — never trust
a zero — and a table of control words per record type. Then literal-spelling variant
ladders, where filiation actually lives in a Brazilian act, the records of enslaved and
freed people including how to get the enslaver's name when you don't have one and the
*nação* phrase ladder for African-born ancestors, the working Hemeroteca Digital recipe
with its stale-render trap and URL-driven paging, a corpus map, and how to calibrate
expectations to the aperture you actually have.

### `newspaperarchive-search`
*266 lines.* Free with a FamilySearch account, and a different corpus from the registers:
it reaches people who appear in no vital record at all — as a creditor, a voter, a
mourner, a defendant, a name in a subscription list. The `tags/` URL grammar, why a
`pf`/`pl` tag hit is fuzzy and not a name match, pulling every row in one call, turning a
row into a citable URL, verification, sourcing back to FamilySearch, token discipline,
and proving a negative.

### `familysearch-compiled-sources`
*139 lines.* The Digital Library, Genealogies and Cemeteries — three tools that return
other people's work rather than records. Good for leads, sibling sets, conflicts,
archival call numbers and coverage checks; never proof. Includes a dated test log of what
each actually returned.

### `genealogy-partner-sites`
*121 lines.* The eight FamilySearch partners plus Portuguese tombo.pt, worked from their
free public pages with no account: what each shows for free, hand-built and tested URL
recipes, measured coverage for Brazil, Portugal and Italy, and how to get back to a free
image. Signs up for nothing, signs in to nothing, pays nothing, solves no CAPTCHA.

### `genealogy-research-audit`
*89 lines.* Nine checks, in order, for research that has stalled. Starts with the
corpus-monoculture check: hundreds of searches against a single platform concluding "this
is the edge of the archive" is usually the edge of *that platform*. Then void negatives,
source counts as a diagnostic, placeholder dates presented as facts, misattached sources,
duplicates from truncated indexes, one-document conclusions, who has genuinely been
searched, and leads needing no archive.

### `familysearch-ordinance-requests`
*135 lines. Church members only — see the gating note above.* Walks a list of profiles,
opens each Ordinances tab, and reserves what FamilySearch shows green and Ready. Scope and consent first, then the deceased, 110-year
and living-relative boundaries, then reading every row before touching anything. The
living boundary is established from the user at the start of each run; no names are
baked into the file.
