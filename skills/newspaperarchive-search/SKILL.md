---
name: "newspaperarchive-search"
description: "Search NewspaperArchive through the free FamilySearch partnership, driven entirely by URL. Covers the tags URL grammar, why a pf/pl tag hit is fuzzy and not a name match, pulling every result row in one call, turning a row into a citable URL, verifying that a hit is really your ancestor, reading the page image, sourcing it back to FamilySearch, token discipline on large result sets, and proving a negative. Use when a name has stalled in the record index, when you want an obituary, or when a person exists in the tree only as somebody's parent and needs dating."
---

# NewspaperArchive, driven by URL

NewspaperArchive is free with a FamilySearch account. It is a different corpus from parish and
civil registers: it reaches people who appear in *no* vital record — as a creditor, a voter, a
mourner, a defendant, a name in a subscription list — and it is often the only channel that
dates a person who exists in the tree only as somebody's parent.

Use it when a name has stalled in the record index, when you want an obituary, or when you need
to attach a date or a place to a person who only ever appears as a relative of someone else.

## 0. Access

- Entitlement page: `https://www.familysearch.org/en/access/newspaperarchive`
- One-time link-up: `https://newspaperarchive.com/signup-with-familysearch/`
- Check you are signed in before concluding anything: a signed-out session returns thin or empty
  results that look exactly like a real negative. Signed in, the page header shows the account
  name and `window.dataLayer` carries `Logged_In=True`.
- FamilySearch also has a name-only handoff form at `/en/search/newspapers/`. Ignore it — it
  exposes fewer filters than building the URL yourself.

## 1. The one structural fact

`/search/` is a **POST form that 302s to `/tags/`**. There is no separate results page.
**`/tags/?...` is the results page and it is fully URL-addressable.**

So never drive the search form. Build the URL, navigate once, read once. Everything below
assumes that.

## 2. URL grammar — `https://newspaperarchive.com/tags/?…`

| Param | Meaning | Example |
|---|---|---|
| `pep` | **Exact phrase.** `-`, `+` and `%20` are all word separators | `pep=justino-dos-reis` |
| `pw` | Exclude words | `pw=cabral` |
| `pf` / `pl` | Person-tag given name / surname — **fuzzy, see §3** | `pf=antonio-justino&pl=dos-reis` |
| `pci` | Country id (`7`=USA, `39`=Brazil) | `pci=39` |
| `psi` / `pc` / `pt` | State id / city id / publication id | `psi=82&pc=3489&pt=28926` |
| `date_mode` | `on` \| `range` \| `before` \| `after` | `date_mode=range` |
| `date` | Single date for `on`/`before`/`after`, `YYYY-MM-DD` | `date=1857-04-12` |
| `date_start` / `date_end` | Range bounds, `YYYY-MM-DD` | `date_start=1850-01-01&date_end=1860-12-31` |
| `date_precision` | Fuzz around `date`: `exact,1d,1w,2w,1m,3m,6m,1y,2y,5y,10y,20y` | `date_precision=1y` |
| `pr` | Results per page — **10, 20, 30, 50 only.** `100` silently falls back to 10 | `pr=50` |
| `page` | 1-based results page | `page=2` |
| `psb` | Sort: `relevance`, `date`, `dateasc`, `dateadded`, `dateaddedasc` | `psb=dateasc` |

Always set `pr=50`. Default 10 means five times the page loads for the same hits.

Accents are ASCII-folded server-side (`José Antônio` → `jose-antonio`). Either form works; write
the folded one. A trailing slash after the last value is cosmetic — drop it.

**Not URL-addressable:** the "All Words" and "Any Word" keyword modes are POST/session state
only. If you need them you must use the form; otherwise express the query as `pep` + `pw`.

To enumerate ids: `GET /search/advancesearch/LocationDropDownPopulateAjaxV1?CountryId=&StateId=&CityId=&PublicationId=`
cascades country → state → city → publication.

## 3. ⚠ `pf`/`pl` is fuzzy. A tag hit is not a name match.

This is the trap that will waste your day. `/tags/?pf=…&pl=…` is a **people-name tag index**
that matches loosely across tokens. Searching `pf=antonio-justino&pl=dos-reis&pci=39` returns
four Brazilian hits — and not one of them is a man of that name. They are other people whose
names happen to contain *Antonio*, *dos Reis* and so on, scattered across the same page.

**Rule: `pf`/`pl` casts a net. `pep` is the only thing that is evidence.**

Work in that order:
1. `pf`/`pl` wide, to learn whether the corpus holds anything near the name at all.
2. Re-run the surviving candidates as `pep=<the full phrase>`.
3. Read the snippet and confirm the phrase is literally there before you believe the hit.

OCR routinely breaks a name across the match, so a `pep` zero is not proof of absence — but a
`pf`/`pl` hit is never proof of presence.

## 4. The cheap read — every row in one call

`POST /search/searchresults/SortSearchResults` with a single field `sortUrl` = any hand-built
`/tags/` URL returns the whole result set as JSON. It honours every parameter in §2, so you can
page and sort without rendering anything.

Its `pContent` is an HTML fragment, not records, so parse it. This snippet returns compact rows
and nothing else:

```js
const sortUrl = 'https://newspaperarchive.com/tags/?pep=justino-dos-reis&pr=50&psb=dateasc&page=1';
const res = await fetch('/search/searchresults/SortSearchResults', {
  method:'POST',
  headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'},
  body:new URLSearchParams({sortUrl})
});
const j = await res.json();
const doc = new DOMParser().parseFromString(j.pContent, 'text/html');
const rows = [...doc.querySelectorAll('div.searchRecordList')].map(r => {
  const m = (r.getAttribute('onclick')||'').match(/CreateNewURL\('?(\d+)'?,\s*'?(\d+)'?/);
  const d = r.querySelector('.detail');
  return {
    img: m ? m[1] : '', art: m ? m[2] : '',
    paper: (d.querySelector('h3')||{}).textContent.trim(),
    meta:  (d.querySelector('span')||{}).textContent.trim(),   // date, city, state, country
    snip: ((d.querySelector('.text p')||{}).textContent||'').trim().slice(0,200)
  };
});
JSON.stringify({total:j.pNumberOfNAResults, window:j.pCurrentContent, rows})
  .replace(/[?=&]/g,'_')
```

Notes that matter:
- The onclick ids are **quoted strings** — `CreateNewURL('410799213','3', event)`. A regex
  expecting bare digits silently matches nothing and you get empty ids on every row.
- Cap `snip` at ~200 chars. The full snippets are the bulk of the tokens and you only need
  enough to see whether the phrase is there.
- Some harnesses reject tool output containing `?`, `=` or `&` as query-string data. End every
  snippet with `.replace(/[?=&]/g,'_')`.
- `j.pNumberOfNAResults` is the total, `j.pCurrentContent` the window ("101-150").

## 5. Turning a row into a citable URL

Result rows have **no href** — `href="javascript:void(0)"`, resolved at click time. Resolve them
yourself, and only for rows that survived §3 and §6:

```js
const body = new URLSearchParams({imageId, articleId});
const j = await fetch('/Search/SearchResults/CreateNewUrlForSearchresults', {
  method:'POST',
  headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'},
  body
}).then(r=>r.json());
// j.Url -> https://newspaperarchive.com/o-jornal-do-porto-may-30-1872-p-2/
// j.PageNumber -> 2
```

The shape is `/{paper-slug}-{mon}-{dd}-{yyyy}-p-{page}/` — stable, human-readable, and the right
thing to put in a citation.

## 6. Verifying it is your person

A newspaper hit is weaker evidence than a parish entry: it has no fixed fields and no clerk
vouching for identity. Walk the ladder and stop at the first failure.

1. **Is the phrase actually there?** Read the snippet. If the match came from `pf`/`pl`, assume
   it is not until you have seen the words adjacent.
2. **Place.** Does the paper circulate where your person lived? A Lisbon paper is not evidence
   for a man in Rio de Janeiro, however exact the name.
3. **Date window.** Does the issue fall inside the person's attested lifespan plus a plausible
   margin? A hit after a documented death is a different man until proven otherwise.
4. **Co-occurring names — the strongest single test.** Look for a spouse, an in-law, a business
   partner, a known neighbour in the same paragraph. One corroborating relative beats a perfect
   name match on its own.
5. **Honorific and occupation.** *Capitão*, *Dom*, *fazendeiro*, *negociante* — these narrow
   identity hard, and they also tell you which other record classes (notarial, probate) to search.
6. **The negative control.** Run the surname alone against the same paper and date range. If
   there are forty of them, a bare name match carries almost no weight; if there are two, it
   carries a lot.

**Never let a snippet reach the tree without the page.** OCR invents words and mis-segments
names routinely. Open the page and read the passage before you attach anything.

## 7. Reading the page itself

Open `j.Url` and use the viewer: zoom, and its own find-on-page, which searches the OCR of that
issue. The viewer's `window.pages` holds the sibling image ids for the whole issue, so once you
have one page you can reach the rest of that day's paper.

The viewer serves DeepZoom tiles. If you read them by stacking tiles into an overlay and
screenshotting, **check `window.innerWidth` first**: screenshots are commonly downscaled
relative to the CSS viewport (e.g. a 2560px viewport captured at 1568px, a factor of 0.61), so
tiles laid out at scale 1.0 arrive at 61% of native and handwriting or small type goes soft.
Lay them at ~1.6 to land near 1:1.

Unverified: a direct full-page JPEG endpoint and a JSON OCR endpoint exist
(`pdftojp2.newspaperarchive.com/IIPViewerWeb/webresources/…`) but are CORS-blocked from the main
origin and 404 when mirrored onto it. Do not build on them without testing them first.

## 8. Sourcing it to FamilySearch

On the person's Sources tab, **+ ADD SOURCE** offers *Add New Source*, *Add New Memory Source*,
*Attach From Source Box*. The first two open the same **Create Source** dialog.

There is **no auto-cite** — pasting a URL prefills nothing. Compose all of it yourself.

| Field (`name`) | Required | Limit | What to put |
|---|---|---|---|
| Date (date field) | no | 150 | The issue date, e.g. `30 May 1872` |
| `sourceTitle` | **yes** | 255 | `Portugal, O Jornal do Porto, 30 May 1872 — José Justino dos Reis` |
| `webPageType` | — | — | radio: `URL` (default) or `MEMORY` |
| `sourceWebPage` | no | 1500 | the resolved `/{paper}-{mon}-{dd}-{yyyy}-p-{n}/` URL |
| `sourceCitation` | no | 1000 | paper, place, date, page, database and access date |
| `sourceNotes` | no | 10000 | **the transcription**, plus what identifies the person |
| `sourceChangeReason` | no | 1500 | why this is him — the §6 reasoning in one or two sentences |
| vital tag chips | no | — | Name · Sex · Birth · Christening · Death · Burial, toggled before saving |
| `sourceAddSourceBox` | no | — | checkbox, **checked by default** |

Citation template:

> "<Paper Title>" (<City>, <State/Province>, <Country>), <DD Mon YYYY>, p. <n>; digital image,
> *NewspaperArchive* (<url> : accessed <date>).

Two things to get right:

- **The URL is behind a paywall for anyone without the entitlement.** A source whose only content
  is a link is useless to the next researcher. Put the full transcription in `sourceNotes` so the
  source stands on its own.
- **For anything important, clip the image and use the Memory route.** Upload the clipping under
  the person's Memories, then create the source with `Add a Memory` → *Select From Gallery*. The
  image then lives on FamilySearch, survives NewspaperArchive, and still carries the citation,
  notes and vital tags.

Tag only the vitals the article actually evidences. A name in a subscription list evidences Name
and nothing else.

⚠ If working under FamilySearch **Helper mode**, every source you add is logged under the person
you are helping, not under your own account. Say so before you start.

## 9. Token discipline

- Never `get_page_text` a results page. It returns the whole chrome, the filter panel and the
  recent-search list for no gain. Use §4.
- One navigation per query, not one per filter. Build the full URL first.
- `pr=50` always.
- Resolve URLs (§5) only for rows that survived verification, not for the whole page.
- Cap snippets at ~200 chars in the extractor, not after the fact.
- When sweeping many names, loop `sortUrl` inside a single JS call and return one compact table.

## 10. Proving a negative

Before reporting "not in NewspaperArchive", establish the corpus covers the place and period at
all. Run a control phrase that must appear if the corpus is live there — a common word in the
right language, or the place name itself — scoped with the same `pci`/`psi`/date filters. A zero
on the control means your negative is void: you have measured coverage, not absence.

Also check which countries actually hold the language you need. Lusophone holdings, for example,
are heavily **Portugal** (Lisbon, Porto) with only a thin Brazilian slice — a Brazilian zero may
simply mean the Brazilian papers are not digitised, while the same name is abundant in Portugal.

## 11. Worked example

Target: **Antonio Justino dos Reis**, coffee fazendeiro, Barra Mansa / Rio de Janeiro, attested
1856–1877.

1. Wide net: `/tags/?pci=39&pf=antonio-justino&pl=dos-reis&pr=50&psb=dateasc` → **4 hits**,
   all *Astrea*, Rio de Janeiro, 1828–1830. Reading the snippets, **none is him** — they are
   Manoel Alves dos Reis, Antonio Joaquim dos Reis, José Antonio de Azevedo. Fuzzy tag matches,
   and all a generation too early. This is §3 in action.
2. Exact: `/tags/?pep=antonio-justino-dos-reis` → **0**.
3. Loosen one token: `/tags/?pep=justino-dos-reis&pr=50&psb=dateasc` → **26**, all **Portugal** —
   José, Ignacio and Julião Justino dos Reis in Lisbon and Porto, 1871–1909.
4. Same phrase scoped to Brazil, `&pci=39` → **0**.

**Conclusion: the phrase does not occur in the Brazilian holdings.** That is a real, citable
negative for the Brazil-side search, and the 26 Portuguese hits are a separate question — whether
the family is Portuguese in origin — not a match to be attached.

Note what made this cheap: four URLs, no form interaction, no page text dumps.

## 12. Known limits

- "All Words" / "Any Word" keyword modes have no URL form.
- `pr=100` silently degrades to 10.
- `plo` changes result counts; its meaning is undetermined. Leave it out.
- `px`, `pfp`, `pubid` appear in the site's JS and do nothing when set.
- Facet arrays in the `SortSearchResults` response come back empty; read facets from the rendered
  page if you need them.
- Clip and download quotas are untested. Assume a limit exists.