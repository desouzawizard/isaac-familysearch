---
name: "familysearch-catalog-and-images"
description: "Find, open and read FamilySearch record images that no index or full-text search reaches — unfilmed-but-catalogued books, unindexed films, names the index mangled, and the one page the machine index failed on. Covers settling the jurisdiction first, reading catalog film lists and their access rights, the Images API (GraphQL, bearer token), locating a page by date inside a film, reading past the viewer's zoom cap via DeepZoom tiles, checking the tree before calling it a find, and attaching with a citation that verifies. Use when a record should exist but name search and full-text both come back empty."
---

# Catalog → film → page → attach

Use this when a record *should* exist but name search and full-text find nothing. The usual reason
is not that the record is missing: the image is **unindexed**, **badly indexed** (a 1875 Genzano birth
was indexed as "Parisi" for *Passeri*), or the one page the machine index **failed on**. The fix is
to go to the film and read the page.

The pipeline, every time:

0. **Jurisdiction** — where was the family *on that date*? Settle it before opening any film.
1. **Catalog** — which film/DGS holds the series, and can this account see it?
2. **Images API** — list the image groups and every image ark in them.
3. **Locate** — bracket the date with index dates, or binary-search with corner grids.
4. **Read** — DeepZoom tiles at ~1:1. Never trust a snippet or an index value.
5. **Check the tree** — is it already attached? Then attach and **verify by API**.

All calls run from any signed-in `familysearch.org` tab via JavaScript.

## 0. Jurisdiction first

⛔ A perfect search of the wrong parish is worth nothing. Tested 13 Nov 2026: a whole July 1881
sequence in the Uberabinha (MG) marriage book was read page by page for a couple who, it turned out,
had moved by ox cart to Campo Grande (then Mato Grosso) in November 1880 — their wedding place,
"Fazenda Progresso", was in Mato Grosso. Before browsing:

- Check migration dates (notebooks, children's birthplaces, the family book) against the event date.
- A child's birth year bounds a marriage: a son born 1882 means the wedding was before 1882.
- Place clues from trees and books are good for *where* even when their dates are wrong.
- Write the chosen jurisdiction and the evidence for it at the head of your notes.

## 0b. Setup (paste once per page load — navigation wipes `window`)

```js
window.out = s => String(s).replace(/[?&=]/g,' ').slice(0,1200);   // the bridge blocks ? & = and >~1 KB
window.__tok = (document.cookie.match(/fssessionid=([^;]+)/)||[])[1];  // bearer for /platform and GraphQL
window.__get = async u => { for (let k=0;k<5;k++){ const r=await fetch(u,{headers:{accept:'application/json'}});
  const t=await r.text(); if (r.ok && t.length>2) return JSON.parse(t); await new Promise(z=>setTimeout(z,1200*(k+1))); }
  throw new Error('gave up'); };                                       // empty bodies = throttling; retry
window.__gql = async q => { for (let k=0;k<6;k++){ const r=await fetch('/records/images/orchestration/',{method:'POST',
  headers:{'content-type':'application/json',authorization:'Bearer '+window.__tok},body:JSON.stringify({query:q})});
  if (r.status===200) return r.json(); await new Promise(z=>setTimeout(z,1500)); } return null; };  // first calls often 503
const AL='M9S3Q7W4HCZ8D6XFNJVK2LGP5RTYB1';
const enc=n=>{n=+n; if(!n) return AL[0]; let s=''; while(n>0){ s=AL[n%30]+s; n=Math.floor(n/30);} return s;};
window.__apid2ark = ap => { const p=ap.split('-'); const a=enc(p[1]), b=enc(p[2]), c=enc(p[3]);
  return '3:1:'+(enc(a.length)+enc(b.length)+a+b+c).match(/.{1,4}/g).join('-'); };
// self-test: TH-1971-33393-411-80 → 3:1:3QS7-L943-36L ; TH-909-64949-88293-95 → 3:1:3Q9M-CSDQ-13H3-3
```

Rules: **one worker** for bulk crawls (four parallel workers produced 83 silent failures); pace
150–250 ms; park big results on `window` and page them back; launch long jobs detached and poll.
**Navigating the tab kills a detached job** — finish it or read its state before moving on.

## 1. Catalog — what was filmed, and who may see it

| Call | Returns |
|---|---|
| `GET /service/search/catalog/v3/search?count=100&m.defaultFacets=on&m.queryRequireDefault=on&q.place=<City, State, Country>&q.place.exact=on` | `totalHits`, `searchHits[].metadataHit.metadata.identifier.value` → `…/koha:N` or `olib:N`, `title[0].value`. Also takes `q.keywords`, `q.title`, `q.filmNumber`, `q.availability=Online` |
| `GET /search/orchestration/catalog/<koha:N \| olib:N>` | **every film row + access rights in one call**: `copies[]{publicNote, callNumber, dgs, item}`, `dgsPermissions[]{dgsNumber, imagePermissions[]}`. For `olib:` records: `source.film_note` (⚠ an object, not an array, when there is one row) with `digital_film_rights` |
| `GET /service/search/catalog/catpl/place/<placeSetId>` | parent/child places and **former names with dates** |
| UI film link | `/en/search/catalog/film?dgs=<9-digit DGS>&cat=<id>&i=0` |

Permission words: `ThemisPrmAnyone` = online · `Fhlc`+`Affiliate` = **FamilySearch Center / affiliate
library only** · `LdsMember` = signed-in Church members · `NoAccess` (often just covers/first frames)
· `Sensitive`.

**List a whole place:** search → ids → orchestration per id at 200 ms. 17 places took < 40 s.
Repeat with `q.keywords=<town>`: records are often filed under a neighbour, a diocese or an old name.
A place whose titles are all "Cartório …" has **no parish books filmed** (Campo Grande, MS: six
records, all civil) — say so instead of browsing.

⚠ The catalog's volume notes beat the viewer's headings. Three times the viewer label was wrong
("Births 1876–79" opened at 1866; a "Death" group was a birth register; "1954" meant 1854).
**Open the first image and read its date before trusting either.**

⛔ **The catalog's *place* is a claim too.** Tested 15 Nov 2026: koha:23252, filed under Itatiaia and Resende (Rio de Janeiro), indexed into the **RJ** Catholic collection, is really **Santo Antônio do Itatiaia, Ouro Branco (Minas Gerais)** plus **N.S. da Boa Viagem, Itabirito (MG)**. The image heading reads «deste Bispado de Marianna… Comarca de Villa Rica». Clues in the record itself: originals held at a different state's archive (Arquivo Arquidiocesano de Mariana), and a note naming another state's town. **Before treating a film as a jurisdiction's books, read one image's own heading** (bishopric, comarca, parish dedication). One call. The flip side: a misfiled film's personas sit in the wrong state's collection, so a search in the right state misses them.

## 2. Images API (GraphQL, bearer token required)

```js
// groups on a film
await window.__gql('{ search(searchInput:{imageGroupNumbers:["004000522"], page:1, pageSize:50}) { totalCount groups { id groupName childCount dateRange{fromTimestamp toTimestamp} metadata{title volume imageGroupNumber} coverages{recordType{name}} } } }');
// groups for a place AND everything under it — place is an Int (unquoted). A quoted id returns null.
// id lookup: GET /service/standards/place/ws-ui/places/request?text=<name>&pagesize=6&output=summary&partial=true&hideUnsearchable=true
// ⚠ totalCount comes back 0 on place searches — page until groups is empty.
await window.__gql('{ search(searchInput:{place:5730, startDate:"1870", endDate:"1895", page:1, pageSize:100}) { groups { id dateRange{fromTimestamp toTimestamp} metadata{title creator imageGroupNumber} coverages{place{fullName} recordType{name}} } } }');
// groups by keyword — for pseudo-places and single-word towns only (see Place traps)
await window.__gql('{ search(searchInput:{keyword:"Indianópolis", page:1, pageSize:100}) { totalCount groups { id childCount dateRange{fromTimestamp toTimestamp} metadata{title volume imageGroupNumber} coverages{recordType{name}} } } }');
// every image of a group, in viewer order (includes restricted frames)
await window.__gql('{ a: artifactChildren(groupIds:["M9SM-PLR"]){ imageApids } }');
// the viewer's Image Index for up to ~4 images per call (cap 200 personas)
await window.__gql('{ getPersonasByArtifact(artifactArks:["3:1:939J-R297-HK"], page:1, pageSize:200){ personas{ id personaData{ name isPrincipal } relations{ name relationType } } } }');
// ark → APID
await window.__gql('{ imageApid(imageArk:"3:1:3QS7-L943-36L") }');
```

Place traps: historical place ids are **separate buckets** (Genzano has three ids; query each). Some
parishes sit under a pseudo-place ("Diocese de Uberlândia") — a place search returns 0 while
`keyword:` finds 86 groups. **Fully locked films do not appear at all**, so a zero here is not "not
filmed" — check the catalog. `indexedChildCount` does not mean name-indexed.

⛔ **`keyword:` matches the words separately.** `"Mato Grosso"` returned São Miguel do **Mato**
(Portugal) and **Grosso** (Piedmont) and nothing from the state. Use `place:` for any multi-word name.

★ **To prove a state or town has no parish books:** page `place:<id>` to the end and tally
`coverages` by place and record type. Mato Grosso do Sul = 1,093 groups, all civil except two
1922–42 baptism books, 1990s religious marriages and three "Campo Grande" baptism books of
1777–1814. Check `metadata.creator` on any surprising hit: those three were Campo Grande, **Rio de
Janeiro**, filed under the wrong place.

A keyword index scan of whole groups is cheap: 1,184 personas across two 1876–1920 marriage books
in about a minute (4 images per call, 220 ms apart). Grep personas and their relations together.

## 3. Locating the page

**A. Bracket with index dates (fastest).** ⛔ Pick the fact that matches the record type. Taking
the first dated fact returns **estimated birth years** on marriage books (a test returned 1860–1866
for pages written in 1884). Tested helpers:

```js
window.__evdate = async (personaId, typeRx) => {
  const r = await fetch('/platform/records/personas/'+personaId.replace('1:1:',''),
    {headers:{accept:'application/x-gedcomx-v1+json', authorization:'Bearer '+window.__tok}});
  if (!r.ok) return '';
  const g = await r.json(), fs = [];
  (g.persons||[]).forEach(p=>(p.facts||[]).forEach(f=>fs.push(f)));
  (g.relationships||[]).forEach(x=>(x.facts||[]).forEach(f=>fs.push(f)));
  const hit = fs.find(f => typeRx.test(String(f.type||'')) && f.date && f.date.original);
  return hit ? hit.date.original : '';
};
// one line per image: persona count, first and last principal's event date
window.__dates = async (groupId, from, to, typeRx) => {
  const ap = (await window.__gql('{ a: artifactChildren(groupIds:["'+groupId+'"]){ imageApids } }')).data.a[0].imageApids;
  const rows = [];
  for (let i=from-1; i<Math.min(to, ap.length); i++) {
    const ark = window.__apid2ark(ap[i]);
    const j = await window.__gql('{ getPersonasByArtifact(artifactArks:["'+ark+'"], page:1, pageSize:200){ personas{ id personaData{ isPrincipal } } } }');
    const ps = ((j&&j.data&&j.data.getPersonasByArtifact)||{}).personas||[], pr = ps.filter(x=>x.personaData.isPrincipal);
    const d1 = pr[0] ? await window.__evdate(pr[0].id, typeRx) : '';
    const d2 = pr.length>1 ? await window.__evdate(pr[pr.length-1].id, typeRx) : '';
    rows.push('i'+(i+1)+' n'+ps.length+' '+(d1||'-')+(d2&&d2!==d1?' .. '+d2:''));
    await new Promise(r=>setTimeout(r,200));
  }
  return rows;
};
// window.__dates('M9SM-PLR', 1, 20, /Marriage/i)   — /Baptism|Christening/i, /Death|Burial/i
```

Reading the output:
- Trust the **day-month sequence**, not the year digits (machine years: 1886 for 1881, 1800, 1000…).
- ★ **n0, n1, or a principal with a `null` name** = the page the indexer could not read. That is where
  an unfindable record most likely is — read it first.
- Then list every couple on the bracketing images with their dates (one call per image) before
  reading pixels — it tells you which half of which page to zoom.
- Books are not always one sequence: late registrations, a chapel section, or a section for enslaved
  people's marriages can sit at the end of the same group.

**B. Corner grids (when nothing is indexed).** Overlay the top-left 2×2 tiles of 8–12 images in one
screenshot, read the year headers, halve, repeat. Measured: 108 images → the right month in 4 probes +
3 grids.

## 4. Reading the page — DeepZoom tiles

```js
window.__setB = ap => window.__B='https://sg30p0.familysearch.org/service/records/storage/deepzoomcloud/dz/v1/apid:'+ap+'/image_files/';
window.__probe=(L,c,r)=>new Promise(res=>{const i=new Image();i.onload=()=>res(1);i.onerror=()=>res(0);i.src=window.__B+L+'/'+c+'_'+r+'.jpg';});
window.__stackF=(L,c0,c1,r0,r1,sc,f)=>{document.getElementById('__ov')?.remove(); const ov=document.createElement('div'); ov.id='__ov';
  ov.style.cssText='position:fixed;inset:0;background:#fff;z-index:2147483647;overflow:hidden'; document.body.appendChild(ov);
  for(let c=c0;c<=c1;c++)for(let r=r0;r<=r1;r++){const im=document.createElement('img'); im.src=window.__B+L+'/'+c+'_'+r+'.jpg';
  im.style.cssText=`position:absolute;left:${(c-c0)*256*sc}px;top:${(r-r0)*256*sc}px;width:${256*sc}px;filter:${f||''}`; ov.appendChild(im);} };
// ⛔ wait for every tile before the screenshot — otherwise half the page is white
window.__ready = async () => { const imgs=[...document.querySelectorAll('#__ov img')];
  await Promise.all(imgs.map(i=>i.complete?1:new Promise(r=>{i.onload=r;i.onerror=r;})));
  return imgs.filter(i=>i.naturalWidth>0).length+'/'+imgs.length; };
```

- ⛔ The tile path must be `apid:<APID>`; the `<ark>` form returns nothing. Load as `<img>` from the
  `sg30p0` host (fetch to that host is CORS-blocked), **or** `fetch` the same path on
  `www.familysearch.org` (`/service/records/storage/deepzoomcloud/dz/v1/apid:<APID>/…`) with the
  bearer header. Fetched tiles can be drawn into one `<canvas>` with `createImageBitmap`, which lets
  you crop to an exact pixel region and wait on a single promise.
- **Get the max level from the descriptor, no probing:** `…/apid:<APID>/image.xml` returns
  `<Size Width Height>`; max level = ceil(log2(longer side)) (12, 13 or 14 — it varies within one
  film). Level L pixel coordinates = full-size coordinates ÷ 2^(max−L).
- **Measure the viewport every session** (`window.innerWidth` against the screenshot width). It has
  been 2560→1568 (×0.61) and 2174→1456 (×0.67) on the same machine. Overview at L11 (scale
  ~1.2) to find the entries; read at max level, scale 0.8–1.25. `grayscale(1) contrast(1.3–1.4)`.
- Call `__stackF` → `__ready()` → screenshot, every time.
- Remove the overlay (`#__ov`) before using the page again.

## 5. Before calling it a find — check the tree

In one run, two of five reported "finds" were **already attached** to the person. Check first:

```js
const j = await window.__get('/service/tree/tf/person/'+PID+'/entityref?version=2');
const refs = j.entityRefs.filter(x=>x.value.type==='SOURCE');   // value.uri = source id; attribution.changeMessage = reason
// per ref: GET /platform/sources/descriptions/<uri> (accept application/x-fs-v1+json + bearer) → titles, about (the ark), citations, notes
```

Match on both the `1:1:` persona and the `3:1:` image ark — a record can be attached either way.
Also compare a record's lists against the tree: the 1912 death list of eleven children exposed a
wife attached as her husband's sister and two duplicate daughters.

## 6. Attaching

**Indexed record → Source Linker:**
`/search/linker?pal=%2Fark%3A%2F61903%2F1%3A1%3A<PERSONA>&id=<PID>` → ATTACH on the record person →
tag checkboxes appear (Name, Sex, Birth…). ⛔ **Untick Name when the index misspells the person** (the
image is evidence; the index's spelling is not). Click the textarea, **type** the reason, click ATTACH.
The JS bridge sometimes fails on the linker page — drive it with `find` refs and real clicks.

**Image-only record → person's Sources tab → + ADD SOURCE → Add New Source.** Fields: Event Date
(pick the standardised suggestion) · Title (required, 255) · Web Page = the image ark URL · Citation
(1,000) · Notes = the transcription (10,000) · Reason (1,500) · vital-tag chips. **Click into each
field and type** — injected values can read back filled and save blank. The + ADD SOURCE menu often
needs a screenshot and a coordinate click: its items report as hidden to `find`.

Reasons: bilingual (EN + PT), quote the original language, say why it is this person and what you
deliberately did *not* tag. Keep under ~1,800 characters: longer reasons are accepted and silently
not saved.

**Verify every save** with the §5 calls: ref present, `about` = the right ark, reason length > 0,
tags as intended. A toast saying "Record attached" is not verification.

## 7. Traps

- ⛔ An agent's or OCR's transcription is a lead. A read of the 1912 death list turned "the late
  Francisco Lino" into what the page says: *"filhos da finada sua filha Francisca Lina Pereira"*.
- Index personas mislabel roles (a declarant son indexed as "Father", the widow as "Mother").
- Multi-item films: one DGS can hold several towns (Corleto Perticara deaths, then Genzano births).
- Group date metadata is approximate; first and last frames of a group are often locked.
- A `q.filmNumber` index search on a multi-item DGS returns every item.
- Session expired = 503 `text/html` or a redirect to `ident.familysearch.org`. Stop; never sign in for the person.

## 8. Worked examples

| Target | Route | Result |
|---|---|---|
| Biase Antonio Passeri, b. 11 Mar 1875, Genzano | catalog koha:779447 → DGS 7198936 item 2 (viewer said "1876–79"; catalog said 1866–79) → act 50, `3:1:3QS7-L943-36L` | Read on tiles; index had "Parisi". Attached via Source Linker, Name unticked, verified |
| Manoel Lino de Rezende † 6 May 1912, Campo Grande | olib:2813626 → DGS 102683526 imgs 201–202 | Already on him. Read the children's list; attached as a new image source to his son José (parentage evidence) |
| José Lino Pereira × Maria Custódia, c. 1881 | Uberabinha marriage books 2–4 (DGS 4000522): `__dates` bracketed July 1881 to book 3 images 7–8; every July entry read (9 Jul ×5, 16 Jul, 30 Jul ×3, 6 Aug). Indianópolis 1876–1920 index scanned | **Absent — wrong jurisdiction.** The wedding was at Fazenda Progresso, Mato Grosso, after the Nov 1880 move; a son was born 1882. The catalog holds no Campo Grande parish books. Lesson now step 0 |