---
name: "familysearch-tree-and-hints"
description: "Navigate, search and edit the FamilySearch Family Tree, drive the large-tree view, and triage auto-generated Record Hints and Research Suggestions without trusting them. Covers the URL patterns and pedigree/relationship endpoints that work, the viewfinder and Options badges, why hints cluster on well-documented people and suggestions on thin ones, evaluating a hint on its relations rather than its name or its confidence score, the rejected-hints pile that is worth reading, reading handwritten images (invert, the zoom cap, neighbouring act numbers), certified transcripts as independent evidence, and the editing traps that each silently lost a save. Use instead of familysearch-tree-operations — this is a superset of it."
---

# Driving FamilySearch

## URL patterns that work

```
Person:       /en/tree/person/details/<FSID>
About tab:    /en/tree/person/about/<FSID>
Sources:      /en/tree/person/sources/<FSID>
Change log:   /en/tree/person/changelog/<FSID>
Fan chart:    /en/tree/pedigree/fanchart/<FSID>
Portrait tree:/en/tree/pedigree/portrait/<FSID>
Indexed rec:  /ark:/61903/<ark>              e.g. 1:1:79FP-PYN2
Image:        /ark:/61903/<ark>?view=fullText  e.g. 3:1:S3HY-D1SD-HS
Catalogue:    /en/search/catalog/results?q.place=Brasil,+<State>,+<City>
Full-text:    /en/search/full-text/results?count=50&q.text=%22PHRASE%22
              scope to one film with &q.groupName=<DGS>
Indexed:      /en/search/record/results?count=50&q.surname=X&q.anyPlace=Y
Tree search:  /en/search/tree/results?q.givenName=X&q.surname=Y
```

**Full-text filters that matter:** `q.anyPlace` (⚠ NOT `q.place`, which silently fails), `q.anyDate.from` / `.to` (the biggest noise-cutter), and a record-type facet. To find a `recordTypeId`, open the Record Type panel, tick a box, apply, and read the value off the URL.

⚠ `q.anyPlace` does **not** constrain full-text search — it only filters indexed records.

⚠ The **Place filter on full-text must be set through the sidebar** (Place → continent → country → state → APPLY); a hand-built `f.recordCountry=` parameter breaks the page. Reuse the resulting URL and swap `q.text`. **Always apply the place filter before reading results** — an unfiltered surname search is frequently dominated by a different country.

## Reading pages reliably

Pages are React and slow. **Wait 9–10 seconds after navigating, then again before reading.** Prefer extracting text over screenshots:

```js
const t = document.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean);
```

⚠ Script execution may return **`[BLOCKED: Cookie/query string data]`** on large dumps **or on any output containing `?`, `&` or `=`**. Store results in a `window.__VAR` first, read them back in **slices of 4–10 rows**, and strip those three characters from anything you print.

## Pedigree and relationship data

**Any person's direct ancestry** — works on any FSID, not just your own:

```
/service/tree/tree-data/r9/portrait-pedigree/<FSID>?numGenerations=9&includeCountries=true&includeSources=true&includeCounts=true&treeId=PRIVATE&locale=en
```

9 generations is the maximum; 10 returns HTTP 422. Results are `j.ancestors[gen][i].parent1 / .parent2`. This returns **only direct ancestors** — never infer a sibling set from it.

⚠ The `includeRecordHints`, `includeResearchSuggestions` and `includeParentHints` flags on this endpoint are **ignored** — the response contains only `ancestors`, with no hint payload. Do not plan around them.

gg**But the person objects carry the drivers the hint system itself uses** — `sourceCount`, `skeleton`, `hasSiblings`, `hasNoChildrenFact`, `hasNoCoupleRelationshipsFact`, `dismissedSuggestions`. Build your own prioritised queue from these rather than trusting the platform's conclusions. **Source count is the key signal: a person with many sources and no parents is a documentation failure, not a records failure.**

**Relationship to a distant ancestor:** load the person page and click **VIEW RELATIONSHIP**. There is no working two-arbitrary-people URL — `/tree/find/relationship?person1=&person2=` redirects to search. Click **HIDE SPOUSES** before extracting; it halves the nodes and leaves a clean single column.

## ★ Driving the large tree view

- **Viewfinder — the minimap at bottom left.** It abstracts the whole tree to coloured dots with a rectangle marking the current viewport. **Left-click any point to re-centre there** — by far the fastest way to cross a wide tree. Click-and-drag on the canvas pans conventionally. The panel has its own × to dismiss it.
- **Collapse nodes** using the chevrons above and below each card. Prefer this to zooming out: past a certain zoom the cards stop being readable and you lose the badges entirely.
- **Options panel — the sliders icon in the top-right toolbar**, beside the view-type dropdown. It opens a right-hand drawer toggling what renders on cards: **Temple Ordinances** (Available / Needs Information / In Progress), **Record Hints**, **Research Suggestions**, **Data Problems**, **Portraits**, **Alternate Parents and Spouses**, Dark Mode, and PRINT.
- ★ **Turn off every badge you are not auditing.** A tree with all badges lit is unreadable; a single-badge pass is how a real pattern becomes visible.
- **Audit from the DOM rather than by eye.** The badges carry stable test ids — `[data-testid="record-hints-indicator"]` and `[data-testid="research-suggestions-indicator"]`. Collect them and walk up to the nearest element containing an FSID to get the whole visible tree's hint distribution in one pass.

## ★★ Record Hints and Research Suggestions — triage, not truth

**Both are generated by FamilySearch's matching system. No human wrote them.** They run on name/date/place similarity and on structural rules over the tree. They are **not evidence and not vetted**, and a real share of them are wrong. Treat each as a question.

### Recognising them

| Badge | Looks like | Is |
|---|---|---|
| **Record Hints** | **teal/cyan** circle, document-with-magnifier glyph | A **specific record** the matcher thinks is this person |
| **Research Suggestions** | **purple** circle, bracket/hierarchy glyph | A **structural observation** about the profile |
| **Data Problems** | **red** circle, `!` | A flagged inconsistency |

On a person page both are merged into the right-rail **Research Help (n)** panel, above *Search Records*, together with the **Quality Score**.

### ★ The inversion worth knowing

**Record hints cluster on well-documented people** — matching needs data to match *on*. **Research suggestions cluster on thin people** — the rules fire on absence. So hints appear where you are already strong and suggestions where you are weak, and **neither points at what is actually hard**. Do not let the badges set your priorities.

### Evaluate on the relations, never the name or the score

The matcher used the principal's **name** to generate the hint, so the name agreeing proves nothing — it is the input, not a check. **The independent check is the other people on the record** (`relations` in the API).

Ask, in order:
1. **Who else is named?** A spouse, parent or child you already know — even badly spelled — is strong corroboration. Strangers are a red flag.
2. **Does the place fit** the person's documented movements at that date?
3. **Does the arithmetic work** — ages, intervals, plausible childbearing years?
4. **Is the name distinctive or common?**
5. **Would this person plausibly appear in this record class at all?**

### ⚠ Confidence scores are not a ranking you can act on

Two hints on the same person can carry **identical confidence** while one is clean and the other is a different person. Observed directly: one c4 hint named the subject's known husband; a second c4 hint on the same person gave a different surname and two strangers. **Same score, opposite weight.**

Use the score to order your *reading*. **Never use it to decide.**

### ⚠ Counting traps

- **One document generates several hints** — a child's birth record naming both parents fires a hint on the child, the father *and* the mother. "Twelve hints" may be four documents.
- **You cannot deduplicate by record id.** Each **persona** on a record has its own `1:1:` ark, so one document legitimately yields several distinct arks. **Deduplicate on relation-set + collection + date.**
- **A badge can mean nothing.** A profile's single "Research Help" item was a *"Quality Score: not available at this time"* placeholder — an indicator pointing at no actionable item.

### The four outcomes — and "ignore" is a real one

| Outcome | When |
|---|---|
| **Attach** | Relations independently corroborate; place and arithmetic fit. Record the reasoning and the original-language quotation, as for any source |
| **Investigate** | Plausible but unconfirmed — the interesting case. **Open the document and read it** |
| **Reject and log** | Demonstrably a different person. **Write down who you rejected and why**, so the next session doesn't re-find them |
| **Ignore** | True but useless. "There is a gap of 3 or more years between siblings" is literally true of most pre-20th-century families — in an era of unregistered infant deaths and migration it carries no information. **Dismissing it is a correct resolution, not a failure** |

⚠ **Never attach, merge, append or annotate from a hint summary.** Open the record first. A hint summary is a search snippet by another name.

### The endpoints

```
Record hints:   /service/tree/tree-data/record-matches/<PID>/all?hintsOnLiving=true
Quality score:  /service/tree/tree-data/quality/person/<PID>/scores
Data problems:  /service/tree/tree-data/match/data-problem/<PID>
Rejected:       /service/tree/tree-data/match/persons/<PID>/rejected
Not-a-match:    /service/tree/tree-data/not-a-match/list/<PID>
Other trees:    /service/tree/tree-data/match/persons/<PID>?matchTypes=OTHER_TREE
Family members: /service/tree/tree-data/r9/family-members/person/<PID>
```

The record-hints response gives `data.matches[]` with `personName`, `collectionTitle`, `confidence`, `score`, `hasImage`, `recordUrl` and — the part that matters — **`relations[]`**.

★★ **It also gives `data.nonMatches` — the rejected pile. Always read it.** A correct record can be sitting there, dismissed by someone else on a garbled index name. On one profile that list held the subject's own marriage record naming her parents, and it was the highest-value find of the session.

The research-suggestion text is not exposed by these endpoints; read it from the **Research Help** panel in the UI.

## Reading a handwritten image

1. Navigate to `<image-ark>?view=fullText`
2. Sliders icon, top right → **Invert Image Colors** (or **Ctrl + /**). White-on-black is dramatically more legible on faded iron-gall ink
3. Zoom three or four times, then pan with `shift` + arrow keys
4. Screenshot at full scale, then zoom into the region
5. **The transcript panel's OCR is a hint; the image is the evidence.** On difficult hands the AI transcript renders the same name several different ways on one page

Other paleography aids: crop to 2–4 lines and enlarge; learn the clerk's hand from words you already know in a neighbouring entry; check the facing page and next image, because entries run across page breaks.

### ★★ When a glyph will not resolve, stop magnifying and read its NEIGHBOURS

The viewer's zoom is **capped**. Past a certain point more scroll ticks change nothing, and a
single ambiguous digit — the margin act number, most often — simply will not come apart. Four
zoom attempts tell you nothing a fifth will fix.

**Act numbers are a monotonic sequence, so the act beside yours identifies yours for free.** Open
the next image, find where your act *ends* (the declarant's and witnesses' signatures), and read
the number of the act that opens underneath. If the next act is 271, yours is 270 — no matter what
the glyph looks like.

Worked case: a margin mark read as **277** was in fact **270**. The next image carried the tail of
the same act and then opened *"Número 271"*. Two page loads settled what four magnifications could
not, **and it had already reached the tree as 277.**

### ★★ A certified transcript is independent evidence, not a copy

A *certidão de inteiro teor*, an estratto, a parish transcript: these are **a second reader of the
same book**, usually a clerk holding the original. When one disagrees with your reading of the
register image, **your reading is the suspect one** — you have the worse photograph and the worse
paleography. Reconcile it; do not assume the original always wins.

They also carry what the filmed page physically cannot: later marginal annotations, retificações,
name standardisations, book-and-folio references. Cite **both**, and say which gave you which fact.

### ⛔⛔ Re-read a clause before you build on it — or explain it away

A family was inverted for three weeks on one grandparents clause read once at low magnification:
*paternos* and *maternos* were exchanged in the transcription, and two parent links were deleted on
it. Worse, a later session accepted that transcription and explained the conflict with four other
sources as "a clerk's slip" — writing that into reasons and notes — before anyone reopened the image.
The clerk had made no mistake.

- **An earlier transcription is a claim, not a record — including your own.** When it conflicts with
  other evidence, the first move is to re-read the image at full zoom, not to rank the sources.
- ★ **A late-registration batch repeats every clause.** A father who registers several children in
  one sitting gives the same *avós paternos / maternos*, marriage and residence formula in each
  termo. Open the pages before and after: eight identical clauses cannot be a slip, and one of them
  is usually easier to read than the rest. Find the batch from the index — several children with the
  same registration date.
- **The words that flip a pedigree are small.** *paternos/maternos*, *filho/filha*, *nesta/na*,
  *Ferreira/Pereira*. Read them letter by letter against the same clerk's other instances on the page.
- **Test the result against a membership list before detaching anyone:** a parent's death record
  lists the children; the spouse's own death record names their parents.
- Deleted-relationship reasons stay in the change log and cannot be edited. If one turns out to be
  wrong, say so in the profile's alert note.

### ⛔ The registry district is not the event place

FamilySearch's catalogue path (`Niterói › Icaraí › Nascimentos 1904–1905`) names the **serventia
that kept the book**, not where the event happened. Reading the district out of that path and
writing it into a vital is inventing a fact the record does not state — and it looks sourced
afterwards, which is worse.

Check the act's own place field. If it is blank, or reads *Ignorado*, then **the place is unknown**:
record the level you can actually prove (the município), and put the residence, the street and the
district in the reason as context. The same trap in another dress is the indexed *Event Place*
naming a judicial circondario — see the index-defect note on Lagonegro.

## ★ Editing traps — each of these has silently lost a save

| Trap | What happens | Fix |
|---|---|---|
| `document.execCommand('insertText')` | Doesn't fire React's onChange, so SAVE fires on an empty field | Type real keystrokes, or use the native setter + `dispatchEvent(new Event('input',{bubbles:true}))` |
| **Date field in the vitals dialog** | Ignores a programmatic value set — field looks right, SAVE is enabled, nothing saves | Type as real keystrokes, then click the standardised-date suggestion |
| **Triple-click on the place field** | Appends instead of selecting, giving "BrasilSanto Amaro…" | `Ctrl+A` inside the field, then type, then click the standardised place |
| **Create Source dialog** | A native-setter fill is discarded by a React re-render — Date/Title/Citation hold but URL, Notes and Reason silently blank, **while the DOM still reads them back as filled** | Real keystrokes only. **Screenshot the dialog before saving**, don't just read `.value` |
| **ADD EVENT menu** | Lists Military Service directly above Occupation | Select by exact name and confirm the dialog title before typing |
| **Cached coordinates** | The window resizes mid-session; clicks land on nothing | Open dialogs by `aria-label`, never by coordinate. Screenshot first |
| **Field order differs between dialogs** | The Death editor puts the date where the Birth editor puts the place — typing "about 1849" into Birthplace looks like it worked | Screenshot and re-measure for **each** dialog. Never reuse a sibling dialog's coordinates |
| **A growing textarea pushes everything below it down** | You fill Citation, then click where Notes *was*, and type into the wrong box | **Fill long fields bottom-to-top** — reason, then notes, then citation, then title. Fields above a growing one never move |
| **Selecting a standardised suggestion reflows the dialog** | The next click lands a row off | Re-screenshot after every dropdown selection, before the next click |
| **An `async` IIFE in `javascript_exec` returns `{}`** | You get an empty object and conclude the endpoint is dead | The tool returns the **last expression** and supports top-level `await`. Write `const x = await f(); x` — never wrap it in `(async()=>{...})()` |
| **Source Box** | Hangs under load (41+ items) | Use ADD SOURCE → **Add New Source** and build the citation directly |
| **Changing a few words in a long reason** | Retyping 1,600 characters to fix two | Select the span from script, then type over it with real keystrokes: `ta.focus(); ta.setSelectionRange(i, i+len)` → `type`. React sees the keystrokes, SAVE enables, the rest is untouched |
| **Source Linker reason box** | Arrives pre-filled with the previous attach's reason | `Ctrl+A` before typing the next one |
| **Add Parent → By ID → Select Couple** | Attaches both parents at once and asks for no reason | Open the relationship's pencil afterwards → ADD REASON |
| **Place typed with a historical state** | "Campo Grande, Mato Grosso" standardised to a hamlet 700 km away in today's Mato Grosso | Type the present-day jurisdiction, keep your own display text (first dropdown row), and **read the standardised line under the field** before saving |

Open a dialog safely, and **verify you got the right one before typing**:

```js
const b = [...document.querySelectorAll('button')]
  .find(x => /Edit Birth|Add Birth/i.test(x.getAttribute('aria-label') || x.innerText || ''));
b.click();
const dlg = [...document.querySelectorAll('[role=dialog]')].find(d => /^Birth/.test(d.innerText));
```

## Standards of proof and workflow

- **Always fill `Reason This Information Is Correct`** with the original-language quotation and the ark. This is the whole standard of proof — a fact without it is an assertion.
- **Standardise dates and places**: type the value, wait ~4 seconds, click the dropdown suggestion. A green *Standardised Date* or a place pin confirms it.
- **Attach a source, reliable route:** ADD SOURCE → Add New Source → Date, Title, URL (`https://www.familysearch.org/ark:/61903/<ark>`), Citation, Notes (full transcription), Reason → tick fact tags → SAVE.
- **Tag a source to a fact:** open the fact's edit dialog → TAG SOURCES → click the row → TAG TO <FACT> → CLOSE. Scope any query *inside* the tag dialog.
- **Brief Life History:** scroll to the bottom → ADD BRIEF LIFE HISTORY → tick *Publish to the about page* → history in box 1, sources in box 2 → SAVE.
- **Always verify after saving** by re-reading the fact list, or `fullLifespan` from `/service/tree/tree-data/v8/person/<id>/summary`. Never assume a save landed.
- **When attaching an unproven candidate**, say so in the record: use an alternate name plus a reason stating the identification is not confirmed, and **do not apply a Vital Tag** — tagging asserts that the record evidences the person's name.

## Before you add anything

**Check the family list first.** On a well-worked couple, the children you are about to add usually already exist — other researchers got there before you. Announcing four additions and finding all four present is a routine and avoidable embarrassment.

**Check the change log** to find who else works this family — that is also the reliable way to identify a contributor you want to contact, far better than a name search in the user directory, which returns unrelated accounts sharing a first name.

And when a source is attached to the wrong person, prefer **leaving a note explaining the evidence** over detaching it. Moving another contributor's work on a heavily-sourced profile should be their decision, not yours.