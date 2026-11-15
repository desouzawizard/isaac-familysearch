---
name: "familysearch-compiled-sources"
description: "Search FamilySearch's compiled and secondary sources by API — the Digital Library (books, with OCR retrievable even for protected titles), Genealogies (submitted trees) and Cemeteries. Covers how to query each from a signed-in session, what each actually returns, and how to judge what it adds: these give leads, sibling sets, conflicts, archival call numbers and coverage checks, never proof. Use when hunting published genealogies, local histories, cemetery records or another researcher's tree — and never let anything found here reach the tree without confirmation on a primary image."
---

# Books, Genealogies, Cemeteries

Three FamilySearch tools that return **other people's work**, not records. They are good for leads,
siblings, conflicts, archival call numbers and coverage checks. They are never proof: anything they
give must be confirmed on a primary image before it reaches the tree.

Run everything from a signed-in `familysearch.org` tab. Output filter first:
`window.out = s => String(s).replace(/[?&=]/g,' ').slice(0,1200);`

## 1. Books (Digital Library) — the most useful of the three

~680,000 items in three access levels: **Available Online** (full viewer) · **Viewable in Library**
(FamilySearch premises only) · **Protected** (search only — almost every Brazilian genealogy).

★ **The search-inside API returns the full OCR of matching pages even for Protected books:**

```js
const j = await fetch('/library/books/api/altopages?item_id=<item_id>&limit=50&q='
  + encodeURIComponent('"Pereira da Rocha"')).then(r=>r.json());
// j._meta.total ; j.items[] = { medianame:"<identifier>_<image6>", content:<page OCR>, highlights }
```

- `item_id` is required. `AND` works inside a book; a space is OR.
- ⚠ HTTP 429 after ~15 quick calls. Pace **1.2–1.3 s**, back off 8 s on a 429.
- **Scan image ≠ printed page.** `medianame …_000529` was printed p. 526. Cite both.
- To read a hit, locate the match in `content` and slice around it; check the index is `>= 0`.

Finding books: **navigate the results page in the tab** (⛔ a scripted fetch of results pages raises a
"slide to prove you are human" challenge; never solve it), then read item ids from the links:

`/library/books/records?page=N&perpage=10&search_submit=1&search=<Q>&fulltext=1&main_keyword=<Q>`

```js
[...new Set([...document.querySelectorAll('a[href*="/item/"]')]
  .map(a => (a.getAttribute('href').match(/item\/(\d+)/)||[])[1] + ' ' + a.innerText.trim().slice(0,70))
  .filter(s => !/^undefined/.test(s) && !/ $/.test(s)))]   // each item appears twice (image + title link)
```

- ⛔ **Without `fulltext=1` only titles and catalogue fields are searched** (`"Pereira da Rocha"` 0 → 107).
- Space = OR (`Rezende Uberabinha` 1,756 = the union); use `AND`. Quotes make a phrase.
- Fields: `Title:"…"`, `Creator.title:`, `Subject:`, `Identifier:`.
- Matching is fuzzy and stemmed (`Passari` finds *Passarinho*). Read every hit.
- The library has its own login that passes silently through the FamilySearch session — that
  redirect is not an expired session.

★ **Portuguese coverage check before any search in Portugal.** The *Inventário colectivo dos registos
paroquiais* (vol. 2 = item **928279**) prints, per freguesia, the surviving register years, series and
custodian. One altopages call on the parish name returns it. Tested: Paço Vedro de Magalhães (Ponte
da Barca) → *"Datas extremas 1651–1885"*, microfilm at the district archive, plus the parish's
administrative history. Use it to know which years exist before opening Digitarq or a film.

Cite as: *Author, Title*, FamilySearch Digital Library item `<item_id>` (identifier `<id>`), scan image
N (printed p. M), accessed date. Quote short passages only.

**Demonstrated:**
- Barbosa, *Dicionário histórico-geográfico de Minas Gerais* (item 1087591, Protected), image 529 /
  p. 526: Uberlândia's founder arrived in 1818; his sesmaria is dated 19 May 1821, with an archive
  call number (*Cód. 384, fl. 96, A.P.M.*) — a route to the original grant and a date conflict with
  the family's published genealogy.
- *Os Magalhães: sete séculos de aventura* (item 86874): 9 pages on Paço Vedro de Magalhães, the
  ancestral Magalhães tower and parish; 0 for the family surname — context, not lineage.

Controls before a zero counts: a common word in the same book must hit.

## 2. Genealogies (submitted trees)

**Search API:** `GET /service/search/lls/v2/personas?count=100&offset=0&m.defaultFacets=on&m.queryRequireDefault=on&<params>`
Params: `q.givenName` `q.surname` `q.spouseGivenName` `q.spouseSurname` `q.fatherGivenName/Surname`
`q.motherGivenName/Surname` `q.birthLikePlace` `q.birthLikeDate.from/.to` `q.anyPlace`; one
collection: `&c.collectionId=on&f.collectionId=<id>`; one submitted tree: `q.subcollectionId=2:2:2:<treeId>`.
UI equivalent: `/en/search/genealogies/results?<same params>`.

Entries carry `content.gedcomx` (principal + relatives + relationships + `sourceDescriptions` with the
collection or tree title). `results` is the loose total (tens of thousands) — never report it as hits.

**Detail:** `GET /ark:/61903/<ns>:<id>?includeEntireFamily=true` with `accept: application/x-gedcomx-v1+json`
→ submitter, upload date, GEDCOM filename and source program, notes. Namespaces: `2:1` IGI · `2:2` Pedigree
Resource File · `2:3` user/partner trees · `2:5` computer-generated. A wrong namespace 404s.
**Climb inside a submission:** `/service/gen/sforge/r9/portrait-pedigree/<ns>:<id>?numGenerations=6`.

Collections: PRF 3 · IGI 5 · Community Trees 8 · Oral Genealogies 9 · RootsFinder 1 · American
Ancestors 11 · Computer-Generated 10000130 · MyTrees 10000120 · Storied 10000204.

How to use it without being misled:
1. Search **husband given + surname + wife's given name**; default search is extremely loose.
   `.exact=on` is unpredictable — filter client-side instead (both spouses' given names present).
2. Keep a hit only if the relatives match (both spouses' given names, birth year ±15).
3. ⛔ **IGI entries are often copies of the Family Tree** — some carry the tree PID as their id. They
   are not independent evidence. Drop them as proof.
   ★ But read them as **history**: an IGI copy can preserve an *older state* of the tree. Tested: IGI
   `2:1:MY42-RPT` lists Maria Custódia de Oliveira in Antônio Honostório's family, while today's tree
   files her as a daughter of her husband's parents — evidence of when an error entered.
4. Compare with the tree (`/service/tree/tree-data/r9/family-members/person/<PID>`) and classify:
   EXTENDS · CONFLICTS · ADDS SIBLINGS · REPEATS.
5. Diagnostic for a wall: `q.anyPlace=<town>&q.anyPlace.exact=on`, then tally surnames. Genzano di
   Lucania held 292 people and no Passeri or Milone — a fast way to know the tool cannot help.

Measured on one family (172 couples): submitted trees cover the **colonial / Portuguese** generations
(59 of 67 non-IGI hits at g10–g12) and almost nothing in the 19th-century Brazilian or Italian layer.
Use it as a sibling-and-conflict checker for old lines, not as a wall-breaker.

## 3. Cemeteries

An experimental directory of **sites**, each listing Family Tree persons linked to it, with one partner
link (Find a Grave or BillionGraves). Not an index of stones.

API under `/service/eurona/experience/travel-sites/`: `sites/autosuggest?searchTerms=` ·
`sites/geo-search?neLat&neLng&swLat&swLng&categories=` · `sites?personName=` · `sites/<id>` ·
`persons/metadata?siteId=`. ⚠ **HTTP 404 means zero results**, not an error. Run a control name that
is known to be present first (a tested control returned 200 with its site).
UI: `/en/cemeteries/sites?selectedSiteTypes=CEMETERY&placeId=<id>&personName=<n>&myFamilySites=true`.

Traps: a place search becomes a map box, so neighbouring towns leak in; same-named cemeteries in
different cities (Rio's "Campo Grande" vs Mato Grosso do Sul). The **"My relatives"** filter is the
one useful feature — it surfaced a third cousin's grave nobody had found. Coverage for Brazilian
towns is near zero (Brazil ≈ 1,056 sites).

★ **Read the burial clause before searching.** A 1912 death record said *"enterrado no cemitério
particular da dita fazenda"* — a private farm cemetery that no directory will hold. The 404 for his
name was explained by the record, not by a gap in the tool.

## 4. Standing rules

- A compiled source never sets a date or a parent on its own. Log it, then find the record.
- Record each rejection with its reason (wrong spouse, impossible dates, different parish).
- Watch famous namesakes: the "Soares de Souza" of Barra Mansa and Niterói in every compiled source
  was the Visconde do Uruguai's family, not this one.

## 5. Test log (13 Nov 2026)

| Tool | Query | Result |
|---|---|---|
| Genealogies | José Lino Pereira + spouse Maria Custódia; Maria Custódia + father Honostório | IGI only (8 + 6 relational hits); REPEATS, plus one older-state clue (§2 step 3) |
| Books | `"Paço Vedro"`, fulltext | 7 items; altopages gave parish register years 1651–1885 and the Magalhães context |
| Cemeteries | Manoel Lino de Rezende; control Luiza Bulhões de Azambuja | 404 vs 200 — explained by the fazenda burial |