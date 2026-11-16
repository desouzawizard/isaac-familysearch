---
name: "familysearch-fulltext-sweep"
description: "Query the FamilySearch full-text corpus programmatically through its XHR search API instead of the client-rendered results page — bulk counts, each document's full page OCR, place and collection facets, and partitioned co-occurrence sweeps. Covers what a quoted string actually matches (exact at the word level, no fuzzy spelling, words not forced adjacent), the deep-paging ceiling and how to partition a corpus into sub-1,000 slices, the place facet as a coverage test, finding the clerical formula before trusting any name search, and measured coverage outside Rio de Janeiro. Use when a search returns zero, when two terms must co-occur, or when you need to prove a record set is absent."
---

# FamilySearch full-text: API sweeps

The full-text results page is client-rendered, so fetching its HTML gives nothing. It calls an XHR
endpoint you can call yourself from any `familysearch.org` page. That turns a navigate + 10 s wait +
DOM read into one `fetch`, and it returns **each document's full OCR text** — which is what makes
everything below possible.

Requires JavaScript execution on familysearch.org, and a signed-in session: if the API returns
**503 with `text/html`** and pages redirect to `ident.familysearch.org`, the session has expired —
ask the person to sign in, and never enter credentials yourself.

## Setup

```js
window.__C='&c.collectionId=on&f.collectionId=<id>&f.collectionId=<id>'
        +'&m.defaultFacets=on&m.queryRequireDefault=on';
// ⛔ NO year filter by default. f.recordYear0 is a CENTURY BUCKET, not a lower bound — see Traps.
const CENT=c=>window.__C+'&c.recordYear1=on&f.recordYear0='+c;   // 1600|1700|1800|1900|2000
window.__q=async(p,n,off)=>fetch(
  '/service/search/fulltext/search?count='+n+'&offset='+(off||0)+window.__C
  +'&q.text='+encodeURIComponent(p),{headers:{accept:'application/json'}}).then(r=>r.json());

const j=await window.__q('"de nação Benguella"',1,0);
j.results   // the TOTAL — identical to the DOM's "Filtered Search Results (N)"
```

| Field | What |
|---|---|
| `results` | total count — independent of paging, but **inflated**; see adjacency below |
| `entries[].id` | **the image ark** — go straight to the image |
| `entries[].content.textDocument` | **the full OCR of the page** |
| `entries[].content.highlightTexts` | ★ **the match validator** — see adjacency below |
| `entries[].content.recordDate / recordPlace / title / recordType` | jurisdiction and film title |
| `entries[].collectionId / collectionTitle` | **the collection's real name** — verify it, don't trust a remembered label |
| `facets` | `Collection`, `Year`, `Place`, `Record Type` |
| `links.next.href` | the API's own next-page URL |

`count=100` works and is the practical maximum.

## ⛔⛔ What a quoted string actually matches

Matching is **exact at the word level** — `"Justyno dos Reis"`, `"Barrra Mansaa"` and other
misspellings all return **0**, so there is no fuzzy spelling tolerance. Diacritics are folded
(`"obitos"` and `"óbitos"` give the same count). A hyphen is treated as a space, so `"Barra-Mansa"`
and `"Barra Mansa"` are identical. Commas are ignored.

⛔ **But quoting does NOT force the words to be adjacent.** A hit may have the words scattered across
the page. `highlightTexts` tells you which:

| `highlightTexts` | meaning |
|---|---|
| **one** highlight, e.g. `[Justino dos Reis]`, and `textDocument.search(/phrase/i) >= 0` | ✅ **true phrase** |
| **several**, e.g. `[Justino ~ dos Reis]`, and `search()` returns `-1` | ⛔ **words found separately** |

★ **So positive counts are inflated.** Worked example: `"Justino dos Reis"` = 14, of which only **9**
are true phrases; two of the false ones are records whose declarant is *Manoel Gonçalves **dos
Reis*** with a *Justino* elsewhere on the page. **Run the highlight test before reporting any count
as a number of real hits.**

⚠ **The reading bug this causes.** Do not write
`t.slice(Math.max(0, t.search(/phrase/i) - 300), …)`: when the regex misses, `search()` returns
`-1`, the window silently becomes `slice(0, …)`, and you read the top of the document believing it
is the match. **Check the index is `>= 0`, or locate the hit from `highlightTexts`.**

### ⛔ Multi-word strings are not a usable AND
It is tempting to conclude a quoted string ANDs its words, and sometimes it behaves that way:
`"escravos Barra Mansa"` = 2, with highlights `escravos ~ Barra Mansa`.
⛔ **But a longer string can return 0 against known co-occurrences** — `"<priest> <town>"` returned
**0** while 4 of that priest's 5 documents demonstrably contained the town. A zero on a 3+ word
string **proves nothing**. Two *separate* quoted phrases are **OR'd** (verify once: A + B returns
exactly `count(A)+count(B)`).

★★ **Consequence for negatives.** A long phrase returning zero is **weak** evidence. Rest an absence
claim on the **regex sweep** and the **place facet**, and say which. "Zero across 28 phrasings"
sounds strong and isn't; "683 documents examined individually, none matching" is.

## ⛔⛔ The deep-paging ceiling

**`offset` works only to about 1,000. Past that the API silently returns PAGE ONE** — no error, no
empty result, just the top documents again. A loop paging to offset 5,000 re-fetches the first page
forty times and looks healthy throughout. Measured:

| offset (count=100) | overlap with page 1 |
|---|---|
| 100, 200, 400, 900 | 0 — real, disjoint pages |
| 1500, 2500 | **100 — identical to page 1** |

This produces false confidence both ways: **negatives that only examined the top 1,000 documents**,
and **counts inflated** by one document being counted on every phantom page (one ark appeared 14
times).

### Always verify disjointness before trusting a sweep
```js
const A=new Set((await window.__q(P,100,0)).entries.map(e=>e.id));
const B=new Set((await window.__q(P,100,900)).entries.map(e=>e.id));
[...A].filter(v=>B.has(v)).length   // 0 = real paging; ~100 = ceiling hit
```
Small overlaps (a few documents) between adjacent deep pages are normal — ranking is not perfectly
stable at score ties. A **total** overlap means the reset. ⚠ Probe with `count=100` and compare
**sets**; at `count=5` the behaviour is confusing and non-deterministic.

### ★ The fix: PARTITION the corpus into sub-1,000 slices
`results` counts and all filters are reliable, so cut the corpus into pieces each under ~1,000 and
sweep every piece to completion:

- **by collection** — one `f.collectionId` at a time; read the ids off the Collection facet's `params`
- **by place** — the place-facet chain below, one município at a time
- **by century** — `CENT(1600|1700|1800|1900|2000)`, one bucket at a time, and **sweep every bucket your
  question spans**. This is a partition, not a lower bound; see traps.
- **by narrowing the phrase** — a qualified form is often a tractable subset: a bare town name at
  2,957 became `"de <town>"` 715, `"Cidade de <town>"` 179, `"Juizo de Orfaos de <town>"` 46

**Check each slice's `results` is under ~1,000 before sweeping, and state your coverage.** "Swept the
first 1,000 of 5,168" is honest and useful; "swept 5,168" when you did not is not. Coverage belongs
next to every negative.

## Execution limits

- **Output**: the JS bridge rejects results containing `?`, `&` or `=`, or over ~1 KB. Always end with
  `.replace(/[?&=]/g,' ').slice(0,1200)`.
- **45 s call timeout.** Roughly 10–15 fetches per call is safe. For more, launch detached and poll:
  ```js
  window.__sweep(10).then(()=>{window.__fin=true});   // returns immediately
  ```
  Keep all state on `window` (`__off`, `__hits`) so a timeout loses nothing and the work resumes.
- **Only one heavy job at a time.** A detached sweep starves later calls and they time out. Kill it by
  setting its offset past the end (`window.__off=999999`) before starting something else.
- Put ~110–250 ms between fetches.

## The place facet — "does this corpus hold records for town X?"

The `Place` facet returns **only the top level** until its parent is selected. Add levels
progressively, then read `facets[Place]`, which then enumerates municípios:

```
&c.recordPlace1=on&f.recordPlace0=8                      // 8 = South America, 6 = Mexico
&c.recordPlace2=on&f.recordPlace1=8,Brazil
&c.recordPlace3=on&f.recordPlace2=8,Brazil,Rio de Janeiro
```

★ **The best tool here, because it is immune to the paging ceiling** — facet counts are aggregates,
not pages. To prove absence: search a formula that appears on every page of the record type
(`"baptisei"` for baptisms, `"falleceu"` for deaths, `"contrahentes"` for marriages), facet to
município, and read off which towns are covered. **Prefer a facet negative over a sweep negative,
and both over a phrase negative.**

⚠ **But a facet counts where a record was FILED, not every place its text names.** A town can be
absent from the facet while documents filed elsewhere quote its registers at length — which is
exactly how a never-filmed parish book gets found, as a certified extract bound into another
jurisdiction's court file. **Never read a facet absence as "unmentioned".**

The facet chain also doubles as the partition key for sweeps. Via the API a 4th level is fine; only a
hand-built **UI** URL breaks on it.

⚠ **Not everywhere.** For Italy (Basilicata) the chain stops at the **province**: `c.recordPlace4`
returns **HTTP 400 "Unable to map record_place4"**. Filter comuni client-side from each entry's
`recordPlace` / `title`.

## ★ The co-occurrence sweep — the only reliable AND

Fetch everything matching one broad phrase and grep the text for the other terms. Grep for **many
targets in the same pass** — once the documents are fetched, extra patterns are free.

```js
window.__T={person:/\b[AÁ]gueda/, place:/Barra.{0,3}Man[sz]a/i, father:/Ba[sz]ilio de Sou/i};
window.__hits={}; window.__snips={}; for(const k in window.__T) window.__hits[k]=[];
window.__sweep=async(pages)=>{for(let k=0;k<pages;k++){
  if(window.__off>=900){window.__ceiling=true;break}        // ★ stop at the ceiling
  const j=await window.__q(window.__P,100,window.__off);
  const es=j.entries||[]; if(!es.length){window.__done=true;break}
  for(const e of es){const t=String(e.content.textDocument||'');
    for(const key in window.__T){const m=t.search(window.__T[key]);
      if(m>=0){window.__hits[key].push(e.id+' '+e.content.recordDate);
        window.__snips[key+'||'+e.id]={ti:e.content.title, w:t.slice(Math.max(0,m-170),m+190)}}}}
  window.__off+=100; await new Promise(r=>setTimeout(r,110));} return 1};
```

**Capture the snippet on the first pass** — storing only arks means re-fetching to read the hits.
**Count DISTINCT arks, not hits**: dedupe with a `Set` before reporting any number.

⚠ **Co-occurrence is only meaningful in a narrative document.** Catalogue and finding-aid pages list
dozens of unrelated cases — one page held three different jurisdictions' probate entries — so two
terms on such a page mean nothing. Check `recordType`/`title` before treating a hit as a link.

## Traps

- ⛔ **The paging ceiling** and **the adjacency/highlight issue** above — the two most dangerous
  things here, because both fail silently.
- ⛔ **Never grep a bare name fragment.** `/gueda/i` matches **"Bangueda"** — OCR for *Benguela*;
  `/dos Reis/` matches **"Angra dos Reis"**, a município with 12,327 hits. **A place or an origin
  term can contain the letters of your person's name.** Anchor with `\b`, include the initial, and
  re-read every hit's context before counting it. The same trap works inside a name:
  `/Lina Fernandes/` matched *Umbellina Fernandes*, so write `/\bLina Fernandes/`.
- ⛔ **Deduplicate before reporting leads.** Records were filmed in duplicate, sometimes triplicate.
  Four arks collapsed to two documents; eight to four people. Compare `textDocument` — identical or
  near-identical text, or a shared film prefix, means one record. (Separately, duplicate filming is
  why a page missing from one filming may be readable in another.)
- ⛔ **`f.recordCountry` breaks both the full-text and catalogue endpoints.** Never use it.
- ⛔ **`q.anyPlace` does not constrain full-text search** — it filters only *indexed* records.
- ★ **Scoping to one film works:** `&q.groupName=<DGS>` or `&f.groupName=<DGS>` (tested 15 Nov 2026: «"Barão do Rio Claro"» 247 → 35 with either). ⛔ **A wrong DGS returns 0, not an error.** A mistyped film number (106… for 105…) once produced a "film scoping doesn't work" note that voided a negative. Take the DGS from the viewer («Film # …»), not from notes, and run one phrase you know is on that film before trusting a scoped zero.
- ⛔⛔ **`f.recordYear0` is NOT a lower bound — it selects a CENTURY BUCKET.** `f.recordYear0=1800`
  means *the 1800s only* and silently drops everything from 1900 on. Measured: `"Agueda"` across
  three collections = **1,149** with it and **9,784** without; the 1900 bucket alone held 6,143
  documents that every sweep had missed. The Year facet says so openly, returning buckets
  `1600/1700/1800/1900/2000`. Use it **deliberately as a partition key**, one century per slice,
  and **never as "from year X onward"**. Filter by exact year after the fact, in your own code.
- ⛔ **Before you trust any filter, take a document you KNOW is in the corpus and confirm the filter
  returns it.** A 1963 document in collection 1582573 returned 0 filtered and 1 unfiltered;
  `"Manoel Antonio Moreira"` in the 1800s bucket dropped **both** known 1827/1833 acts. A filter
  that silently drops a century is indistinguishable from a thorough search — the sweep *reports
  itself complete either way*. One positive control costs one call and is the only thing standing
  between you and a confident false negative.
- ⚠ **A sweep inherits whatever was in `window.__C` when it ran.** When you report a negative, report
  the filter string with it. "Nothing found" without the filter is not a finding.
- ⚠ **The index date can be the EVENT date, not the document's.** A certificate indexed 1846 proved
  to be an 1856 document quoting an 1846 birth. Don't filter by year on that assumption.
- ⚠ **Verify the collection's real name** from `collectionTitle`. A collection labelled for one record
  type is often an umbrella holding several — probate, civil registration and parish books together.
- ⚠ In the UI, result lists **lazy-load**: `count=50` does not put 50 cards in the DOM. Use the API,
  or scroll. Read the total from the header `Filtered Search Results (N)`, never a loose
  `\d+ results` regex.

## ★★ Before trusting any name search: find the clerical formula

The most expensive error is a well-run search for the wrong phrase. Registers are formulaic, and the
formula varies by parish, clerk and decade. **Read one real page of the register you are searching,
then build the phrase from what the clerk actually wrote.**

A worked example: seven variants of `"<name> de nação <X>"` all returned zero, with controls alive in
the thousands. The register wrote origin as a **bare surname** — *"Ricardo Moçambique"*, *"Luiza
Benguella"* — so every variant tested a shape that clerk never used. The same register also wrote
*"de nação"* with **no origin named at all**, which is why the generic phrase had 5,166 hits while the
named origins had ~685 between them.

Related habits:

- **Run both spellings and keep the larger — don't assume the archaic one wins.** `Benguella` 67 beat
  `Benguela` 6, but `Moçambique` 73 beat `Mossambique` 4. Also ph/f, y/i, z/s.
- **Test whether a film is OCR'd before trusting a zero.** Search a word that must appear on every
  page of that record type. Hundreds of hits means your zero is meaningful; zero for the common word
  means the film is dark and must be browsed. ⚠ **One control word can still miss pages:**
  `"matrimonio"` reached only 31 of a marriage book's 38 pages and missed a known act;
  `"Ritual Romano"` recovered it. Run **two unrelated formula words per book** and union them.
- **Search the people standing next to the person** — declarants, witnesses, godparents, heirs.
- **Search the record number**, not the name, when a name search fails.
- **Search the official, not the family.** A parish priest's name retrieved four extracts from his own
  registers across fifteen years; the register's boilerplate (`"assentos de baptismo"`,
  `"certifico que no livro"`) retrieved the rest. Officials recur where families appear once.
- **An identifier can outlive its institution.** Origin was still recorded in civil registrations
  years after the practice it described had ended; don't cap the window at the institutional end date.
- **A lost register can survive as a quoted extract.** Certified transcripts of parish books were
  copied into probate and notarial files, which may be OCR'd even when the register itself was never
  filmed. Courts demanded them as proof, so follow the procedure that generated the copy.
- **Know which fields a record type actually carries** before building a plan on it. One register
  recorded *name, colour, age, status, parentage, occupation* — and **not** origin, the one field the
  research needed. Read one example before treating a series as the answer.

## Coverage outside Rio de Janeiro (measured Nov 2026)

Control words per place facet (`baptizei` / `baptisei` / `matrimonio` / `falleceu`). Check these before
reading any zero as absence.

| Region | Full-text reach | Watch for |
|---|---|---|
| MG, Triângulo (Uberaba, Uberlândia, Indianópolis, Monte Alegre, Sacramento, Araguari) | good from c.1865; patchy before | Uberlândia's "Bapt 1855–70" is a **slave register**; Indianópolis has only 1823–34 and 1836–44 before 1868 |
| MG, Itabirito / Moeda / Belo Vale | 1700s thin or **0** | Itabirito's 18th-c. baptisms start in 1795 |
| SP, Cajuru | baptisms 1856–1919 | |
| SP, Mococa | **nothing before 1929** (civil 1929–54) | |
| MS (whole state) | ⛔ **19th c. dark**: `baptizei` 0; Campo Grande = civil 1979–2015 only | see below: it IS indexed |
| Basilicata | Genzano Tribunale 1866–1910 ≈12k docs; Oppido's State Archive registers OCR'd, Genzano's **not** | facet stops at the province |
| Portugal | heavy, every district | 1700s name hits are dominated by Braga/Lisbon worthiness and blood-purity files |

★★ **Dark in full text ≠ unsearchable.** A place can be dark here and fully **indexed**: MS civil
registration 1875–2019 is in `/service/search/hr/v2/personas` (`q.deathLikePlace`, parents'
names). One indexed search for a wife's own death settled a disputed parentage that full text could
never reach. **Run the indexed search before calling a place dark.**

```js
// indexed search: same-origin, bearer = the fssessionid cookie; count=100, page with offset
const r = await fetch('/service/search/hr/v2/personas?count=100&offset=0'
  + '&q.givenName=Maria%20Custodia&q.surname=Oliveira'
  + '&q.deathLikePlace=Mato%20Grosso%20do%20Sul%2C%20Brasil&q.deathLikeDate.from=1904&q.deathLikeDate.to=1960',
  {headers:{accept:'application/json', authorization:'Bearer '+tok}}).then(r=>r.json());
// r.entries[].id = persona id; .content.gedcomx = persons (one has principal:true), facts, relationships
// also: q.fatherGivenName/q.fatherSurname/q.motherGivenName/q.motherSurname, q.spouseGivenName/q.spouseSurname
// full record + image ark: GET /platform/records/personas/<id>  (accept application/x-gedcomx-v1+json)
```

- ⛔ **`results` is fuzzy and huge** (27,000 for one couple). Filter client-side: keep entries whose
  **principal** name matches, and whose first place matches the jurisdiction.
- ★ **Search each spouse's own death by name**, not only the children's records. Children's records
  repeat the parents' names; only a person's own death or marriage names *their* parents.
- An indexed age can be badly wrong (a woman married c.1881 was indexed "born 1883" from an age of 69
  given by a non-relative). Test identity on the parents, the place and the marital status instead.

⚠ `content.title` carries the **film's start year**, not the event's. OCR misreads years
(1872 → "1892", 1864 → "1862"), so take the date from the image.

## Triage without opening the viewer

`textDocument` is the whole page, so most candidates can be killed or kept from the search result
alone: check the date against the person's known life span, the jurisdiction against where they
lived, and the named relatives against the known family. ★ **Filiation is often the fastest
discriminator** — someone foreign-born appears with *parents unknown*, so a namesake with named
parents is excluded on sight.

Open the image only for a candidate that survives all three. **Record each rejection with its
reason**, so the next session doesn't re-open it.