---
name: "brazilian-genealogy-search"
description: "Search Brazilian genealogical records across FamilySearch full-text and indexed collections, the Almanak Laemmert, the Hemeroteca Digital Brasileira and provincial presidential reports — including the baptism, marriage and death records of enslaved and freed people. Covers the control-search method that makes a zero result mean something, literal-spelling variant ladders for Brazilian names, how to read a parish or civil act for filiation and naming culture, the nacao phrase ladder for African-born ancestors, and the Hemeroteca URL recipe with its stale-render trap. Use when researching a Brazilian ancestor, when a search returns nothing and the negative has to be proven, or when a record that should exist in Brazil will not surface."
---

# Searching Brazilian records

## THE PRIME DIRECTIVE: never trust a zero

A zero result means nothing until you prove the corpus is searchable. **Before accepting any negative, run a control search for a word that must appear on every page:**

| Record type | Control word |
|---|---|
| Death books | `falleceu`, `sepultei`, `cemiterio` |
| Baptism books | `baptisei` |
| Marriage books | `casamento`, `contrahentes` |
| Any Brazilian corpus | the município name alone |

Hundreds of hits means the corpus is searchable, so your zero is **meaningful**. Zero for the control word means the corpus is **dark** — it must be browsed, and your negative is worthless.

Apply this to every corpus, not just the first. A rule learned on one archive does not transfer automatically.

**The companion directive: never trust a number you did not watch arrive.** Search interfaces redisplay the *previous* query's totals while the new one runs. See the stale-render trap below — it is the single most productive source of false findings in this work.

## Spelling — full-text search is literal

Run **every** variant. These are not edge cases; they routinely halve or zero a result set.

- **z / s** — `Basilio` vs `Bazilio`, `Souza` vs `Sousa`
- **y / i** — `Luiz` vs `Luis`, `Nictheroy` vs `Niterói`
- **ph / f** — `Josepha` vs `Josefa`, `Lindolpho` vs `Lindolfo`
- **Doubled consonants in period orthography** — `Benguella` not `Benguela`, `Mança` for `Mansa`, `ç` for `s`. This matters most for the *nações*: run both spellings of every one.
- **Accents** — strip and restore them; OCR drops them inconsistently
- **Hyphenation of place names** — printed sources hyphenate (`Barra-Mansa`), and the two systems behave differently, so measure per system rather than carrying a rule across:
  - **FamilySearch full-text: the hyphen is IRRELEVANT.** Measured 19 Oct 2026 — `"Barra-Mansa"` = 2,957 and `"Barra Mansa"` = 2,957, identical; the engine treats a hyphen as a space. ⛔ An earlier version of this rule claimed 0 → 608 here. **That claim was itself the error** — the 0 → 608 measurement came from Internet Archive, not FamilySearch — and it was withdrawn once measured. If you meet it again in an older doc, it is wrong.
  - **Hemeroteca: the hyphen is poison.** `"Barra Mansa"` = 130,681 but `"Barra-Mansa"` = 1,140,797, because the index splits on the hyphen and matches *Barra* / *Mansa* loose.
  - ★ **The tell is the impossible number.** A small town cannot appear on 1.1 M pages. A result far larger than the term could plausibly support means the index tokenised your term — treat the count as evidence about the engine, not about the town.
  - ★★ **The general rule this is an instance of: a spelling or syntax finding is a fact about one search engine, not about the name.** Re-measure it on each system before relying on it, and when you withdraw one, sweep every doc and skill that repeats it — a correction that reaches only one of its homes leaves the other homes contradicting it.

**Run the full name AND the short name separately, then compare.** A man printed as *Antonio Justino dos Reis* also matches a search for *Justino dos Reis* — but the short form additionally catches **other men**. Where the two disagree about which years a person appears in, the full-name result is the reliable one and the short-name extras must be read before being claimed.

Indexers also garble given names badly. One woman appeared as *Georgina, Dionysia, Olimpia, Piomyria* and *Thamazia* — all the same person. **Anchor identity on the parents' names, never on the given name.**

## Core techniques

1. **Records were kept in DUPLICATE** — civil *and* parish, and each filmed separately. A page missing from one film is not a missing record. A lost parish book may survive as a **diocesan copy**. Always ask for both.
2. **Search the record NUMBER, not the name**, when a name search fails. A termo number is unique and appears in both copies.
3. **Search the people standing next to the person** — declarants, witnesses, godparents, the person who signed for an illiterate relative, in-laws, employers, former enslavers. This finds records no name search reaches. Godparents in Brazilian baptisms are overwhelmingly kin, and for slavery-era work **the enslaver's name is the index key** to the records that name the ancestor.
4. **Check the CATALOGUE before concluding a record doesn't exist.** Absence of a subject heading is proof; failed searches are not.
5. **Read the IMAGE, not the index.** Indexes carry wrong years, invented names and impossible dates.
6. **A place-name on a profile can be a standardiser artifact.** Check the source document before believing a jarring birthplace.
7. **Indexed search and full-text search have DIFFERENT coverage.** Always run both.

## Reading a Brazilian record — where the genealogy actually lives

A birth entry follows a fixed clause order (Decreto 9.886/1888, art. 58). The genealogy is in clauses 5 and 6:

- **Filiação** — *filho legítimo do declarante e de sua mulher Dona [—]*
- **★ Avós** — *neto paterno de [—] e [—], e materno de [—] e [—]* ← **this names the generation above**

Words to hunt: `neto paterno de` · `filho natural` · `pai incógnito` · *já fallecid**a*** (feminine singular) vs *já fallecid**os*** (plural). **That grammatical difference is evidence** — one grandparent named in the feminine singular means no grandfather was declared.

⚠ A grandchild's record names the **grandparents**, not the great-grandparents. To reach generation N you need the birth records of generation N−2's children. Getting this wrong wastes whole sessions.

## Records of enslaved and freed people

**Parishes kept SEPARATE books for enslaved people.** A clerk searching only the free-people's register will correctly report "no entry." Any request for a pre-1871 baptism must name these explicitly:

- `Batismos de filhos livres de escravos` / `Óbitos de filhos livres de escravos` (Free Womb Law, 1871–1888)
- `Batismos de escravos` / `Óbitos de escravos`
- `Batismos de ingênuos`, `Livro de matrícula de escravos`, `Cartas de alforria`, `Livro de notas`

In these books the mother has **one given name and no surname**; the second name on the entry is the **ENSLAVER**, not the father.

**The documentary chain to origin:**

> baptism names the enslaver → **1872 matrícula (indexed BY OWNER, unusable without that name)** → the owner's **inventário** (lists people as property, with ages and family groupings) → **cartas de alforria** → Lei dos Sexagenários (1885)

⚠ In **1890** the republic ordered slavery archives destroyed ("queima dos arquivos"). **Church books survived because they belonged to the Church.** That is why the parish is the priority.

### ★ Getting the enslaver's name when you don't have one

This is usually the blocking step, and the **Almanak solves it**. Its municipal sections carry a heading such as **`Fazendeiros de Café`** — in a slaveholding region, effectively the list of the town's slaveholders, forty to fifty names. That converts "indexed by owner, so unusable" into a finite candidate list to put against the 1872 matrícula and the comarca inventários.

A man's **disappearance** from successive Almanak years brackets his death, which dates an inventário request. Confirm the bracket with the full-name search, not the short name.

### ★★ The nação, and the phrase ladder that reaches it

Parish registers record the ***nação*** — angola, benguela/benguella, congo, cabinda, cassange, gege, monjolo, rebolo, moçambique, mina, nagô, quilimane, inhambane. For a descendant of an enslaved African this single word is usually the highest-value datum obtainable.

If the parish books are lost or unfilmed, **newspapers are an independent channel to the same fact**:

- **Anúncios de escravos fugidos** — standard form: *"fugiu a escrava [name], de nação [x], de propriedade de [owner], no município de [y]"*. Name, nação, owner and place in one sentence. The **Jornal do Commercio** and the **Correio Mercantil** were the main venues.
- **Listas do Fundo de Emancipação** — published by município: name, age, **nação**, owner.

**Do not search `"de nação"` on its own.** Stopwords are dropped, so it degrades to *nação* and returns over a million pages. Climb this ladder instead, one rung per query, recording the count at every rung:

| Rung | Query | What it gives |
|---|---|---|
| 1 | `"<Name>"` | the aperture, and the control that proves the corpus is live |
| 2 | `"escrava <Name>"` | the advertisements — usually a two-figure number |
| 3 | ★ `"<Name> de nação"` | **the nação sentence itself, at phrase level** |
| 4 | ★★ `"<Name> de nação <nation>"` | the nação, named, in print |
| 5 | `"<Name> de nação" <município>` / `<owner surname>` | the tie to a place or a family |

Rungs 3 and 4 are exact phrases, so a hit is a **sentence**, not a page-level coincidence — that is the whole value of the ladder. Rung 5 is a page-level AND on a broadsheet full of classifieds and proves far less; say so when reporting it.

Work rung 4 by running every nação in turn, in both spellings. A single hit dates and locates an advertisement stating an African origin.

⚠ Rungs 2 and 3 often return **disjoint sets** — different advertisements, probably different people with the same name. Check whether any edition appears in both before treating them as one person. A name match is not an identification: ask what would raise it to one (the município, the owner's surname, an age) and test for that explicitly.

**Extending the sentence when the image is gated.** You can still reconstruct wording by extending the phrase one word at a time (`"<Name> de nação <nation> de propriedade de"`) and watching where it drops to zero. Commas are ignored by the index, so punctuation does not break a phrase; a wrong word does. The owner's name is usually four or five words past the nação.

## ★★ THE HEMEROTECA — the working recipe

The Hemeroteca Digital Brasileira (`memoria.bn.gov.br`) is the most under-used Brazilian corpus, and **it holds the full imperial Almanak run** — `Almanak Administrativo, Mercantil e Industrial do Rio de Janeiro, 1844–1885`, 61,370 pages. You do **not** need CRL, which renders blank to automation.

**It will not run a bare search. The missing step is the Locality tab.**

1. Open `memoria.bn.gov.br/hdb/periodico.aspx`
2. Click the **Locality** tab
3. Locality → type the state code (e.g. `RJ`) → select it from the list
4. Newspaper then auto-fills to **"Todos (N)"** and Period to **"Todos"** — that is the whole point
5. Type the phrase **in quotation marks** → **Search**

It then searches **millions of pages across thousands of titles** in one query — for RJ, 13,501,530 pages across 2,734 periodicals.

⚠ The entry form is built from Telerik RadComboBox widgets with no native `<select>`. Options populate only on a **real** click, never a programmatic one. Do steps 1–5 with coordinate clicks and screenshots.

### ★ After the first search, drive it by URL

The results page URL is parameterizable and reproducible. This is far more reliable than clicking, and it is how every subsequent query should be run:

```
memoria.bn.gov.br/DocReader/docmulti.aspx?bib=[cache]<TOKEN>.DocLstX&Pesq=<url-encoded query>
```

Navigate with a new `Pesq` and the same locality scope re-runs. The `[cache]` token is session-scoped and expires — re-derive it by running the Locality recipe once.

In-page alternative (survives until a full postback wipes your globals):

```js
const box = document.getElementById('PesquisarTxt');
const btn = document.querySelector('[id$=PesquisarBtn_input]');
Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(box, q);
box.dispatchEvent(new Event('input',{bubbles:true}));
box.dispatchEvent(new Event('change',{bubbles:true}));
btn.click();
```

Unlike the entry form, **the results page scripts fine** — read totals and rows from the DOM rather than from screenshots. Keep returned strings short; large HTML dumps come back as `[BLOCKED: Cookie/query string data]`.

### ⛔⛔ THE STALE-RENDER TRAP

**The grid keeps displaying the previous query's numbers while the new one runs, with no spinner.** A screenshot or DOM read taken ten seconds after Search will often show the *old* total, and it looks exactly like a real answer. In one session this produced four wrong findings, including two zeros that were really twos.

Worse: a missing `Matchs` label means *either* zero results *or* still loading. The two states are indistinguishable from the number alone.

**The readiness check — do this on every single query:**

1. Before searching, capture a fingerprint: the results `<tbody>` **element identity** plus the first few rows' text.
2. After searching, poll until that `<tbody>` **node has been replaced**. Telerik swaps the node on re-render, so this fires even when the new result is textually identical to the old — which a text-only fingerprint cannot detect.
3. Return READY/PENDING alongside every number, and **never quote a PENDING number**.
4. Re-poll rather than re-search; results usually land in 5–10 s but sometimes 25 s.

⚠ Do **not** put the polling loop inside an `await` in one scripting call — it holds the debugger channel open and times out at 45 s, sometimes after the searches have already run. **Fire the query in one call, sleep, read in a second call.**

### Multi-term queries AND at the page level

Unquoted terms and multiple quoted phrases intersect. Verified two ways: a nonsense second term zeroes the result, and a second term present on every hit page leaves the count unchanged. Useful for triage — but remember:

- **Stopwords are dropped** (`"de nação"` → *nação*, 1.3 M pages)
- **Hyphens split** (`"Barra-Mansa"` → 1.1 M pages)
- **Commas are ignored**, so `"Agueda de nação"` matches text printed *Agueda, de nação*
- The intersection is **page-level** on a broadsheet carrying hundreds of unrelated advertisements. It narrows; it does not link.

### Reading results

Results open in a NEW TAB, pre-sorted by match count, one row per periodical. The Options column's `+` opens a menu whose items sit at row_y **+14 / +40 / +65 / +91**:

- **Go to first page…** · **Go to first match…** · **Match list…** · **Library info…**

⚠ The menu needs **~4 seconds** to paint. Clicking the second item too early lands on a grid row and opens the wrong periodical. Always screenshot between the two clicks, and re-check row positions after any re-sort.

★ **Every row of the Matches list is clickable** and navigates to that exact page, yielding a durable URL:

```
DocReader.aspx?bib=<BIB>&pesq=<PHRASE>&pasta=ano%20<YYYY>\edicao%20<NNNNN>&pagfis=<N>
```

That is how to collect a precise citation for **every** match, not just the first — "Go to first match…" only ever gives you one.

★ **The Description filter box** above the grid filters the periodical list by title. Typing a town name is the fastest way to discover whether a **local** newspaper for that município exists in the corpus — a 56-page small-town weekly of the right years is a complete read, unlike a metropolitan daily.

⛔ **Since 3 October 2025 the Hemeroteca CAPTCHA-gates the page images.** Do not attempt the CAPTCHA, and do not look for a route around it. Collect the full citation — periodical, ano, edição, pagfis, bib — and hand the URL to the researcher to open and read.

## The corpus map

| Corpus | Holds | Notes |
|---|---|---|
| **FamilySearch** indexed + full-text + catalogue | civil registration, Catholic parish records | Different coverage per route — run all three |
| **★ Hemeroteca Digital Brasileira** | newspapers **and the full imperial Almanak**: runaway ads, emancipation lists, obituaries, *missa de sétimo dia*, **editais de inventário** | See the recipe above. CAPTCHA on images |
| **Almanak Laemmert 1844–1889** | per município: Camara Municipal, Juizes de Paz, **Officiaes de Justiça**, tabelliães, **Fazendeiros de Café / proprietários** | Best reached through the Hemeroteca. ⚠ The Biblioteca Nacional's *other* online copy is **1891–1940** — too late for imperial research |
| **Relatórios dos Presidentes da Província** | matrícula statistics, official lists, Fundo de Emancipação | Digitized, full-text, chronically under-used |
| **Arquivo Nacional (SIAN)** | 1872 matrícula, ingênuos, alforrias | Registration required |
| **APERJ / state archives** | comarca inventários | Often un-filmed |

⚠ **The Almanak was issued in TWO volumes per year — Corte and Província.** Only the Província volume carries municipal officeholder rosters. Diagnose before trusting a negative: a Província volume has dozens of `Camara Municipal` and `Juizes de Paz` matches; a Corte volume has **zero** and cannot answer any município question however large the file is.

**Internet Archive full-text**: `archive.org/search?query=<terms>&sin=TXT` searches inside scanned volumes. Page-level AND — both phrases must be on the same page.

## Grepping a scanned volume

Far faster than any book reader: load `archive.org/download/<identifier>/<FILE>_djvu.txt` and regex it.

⚠⚠ **The file STREAMS. A partial load produces false zeros.** The same volume has read 31K, then 127K, then 720K, then 3.95M characters on successive reads of one page. Before trusting any count:

1. Poll the length until it stops growing
2. Sanity-check a marker you know is there — a full provincial Almanak has **dozens** of `Officiaes de Justi` matches, not five
3. Confirm the volume is the complete edition, not a partial or index-only file

⚠⚠ **archive.org's full-text SEARCH is not the same corpus as the items' djvu.txt files.** A phrase can return **0 results** via `&sin=TXT` while being demonstrably printed in a volume archive.org hosts. **A `sin=TXT` zero is not a trustworthy negative** — grep the file to confirm.

## Calibrate expectations to the aperture

Before spending days on a printed source, ask how many people it could possibly name. One parish in 1883 recorded **29 eleitores** — twenty-nine qualified voters in the whole freguezia. Almanacs and newspapers cover the propertied and the officeholding. A labouring or formerly enslaved family will not be in them, and that is the size of the aperture, not a research failure.

Say so plainly rather than grinding. But note the two corollaries: **the enslaver IS in those sources**, which is often the way through when the ancestor is not — and **the enslaved person is in the advertisements**, the one genre where they are named, described and located by their own given name.

## Report what you actually have

Keep three levels separate and never let them blur:

1. **Citation** — periodical, year, edition, page. Earned by the search.
2. **Co-occurrence** — two terms on one page. Narrows the field; proves nothing.
3. **Identification** — this record is about this ancestor. Requires a matching parent, place, date or owner, and is almost never established by a given name alone.

A common given name in a metropolitan daily is level 1. Write it up as level 1, state what would raise it to level 3, and test for that rather than asserting it. Log the queries that came back **empty** too, with the control that proves the corpus was live — a recorded negative is what stops the next session repeating the work.