---
name: "familysearch-platform-api-reads"
description: "Read FamilySearch's /platform API from a signed-in browser tab — tree/person/family pulls, duplicate checks, place and jurisdiction history, date standardizing, watching profiles for edits. Read-only, human-paced, the user's own session. Use alongside the familysearch-tree/catalog/fulltext skills, not instead of them."
---

# FamilySearch `/platform` read API, from a signed-in tab

The documented `/platform` API is callable same-origin from any signed-in `www.familysearch.org`
tab. It is the clean way to pull tree data, check for duplicates before creating a person, and
look up historical place jurisdictions. It is **read-only here** and complements the other
FamilySearch skills — it does **not** replace record search (`/service/search/hr/v2/personas`)
or full text.

## Boundaries — do not cross
- Calls use the person's **own session token** — legitimate use of their own credentials.
- **Never print the token.** Extract it, use it in the header, keep it off screen.
- **Read-only.** Writes (notes, match-status, merges) go through the reviewed workflows, not here.
- **Human pace. Stop on any 403 / 429 / licence notice.** The `blocked by security service` 403s
  come from the site's bot-detection (Imperva), and full text is a separately licensed service.
  Do **not** engineer around those controls — it risks the account. Back off instead.
- **No living people** in descendancy/search pulls.
- Read the image before any value reaches the tree — unchanged.

## Setup (paste once per page load; navigation wipes `window`)
```js
window.__tok=(document.cookie.match(/fssessionid=([^;]+)/)||[])[1];   // bearer = session id; NEVER print it
window.__api=async(path,accept)=>{const r=await fetch(path,{headers:{accept:accept||'application/x-fs-v1+json',authorization:'Bearer '+window.__tok}});
  return {s:r.status, pt:r.headers.get('x-processing-time'), ra:r.headers.get('retry-after'),
          etag:r.headers.get('etag'), warn:(r.headers.get('warning')||'').slice(0,200),
          body:await r.text()};};   // cookie alone => 401; the Bearer header is required
```

## The three things that bite
1. **Accept header is per-resource. A wrong one returns 406.**

   | Resource | Accept |
   |---|---|
   | persons, relationships, families, parents/spouses/children, notes, sources, ancestry, descendancy | `application/x-fs-v1+json` |
   | records personas, collection & place *descriptions* | `application/x-gedcomx-v1+json` |
   | tree search, places search, change feeds | `application/x-gedcomx-atom+json` |
   | `/platform/dates` | `text/plain` |
   | `/platform/places/types` | `application/json` |

   Fallback when you can't set Accept: append `.json` to the path.
2. **The real error is in the `Warning` header, not the body.** The body just says
   "Failure in upstream call". The header names the bad term / bad date / bad facet.
3. **Throttle budget is processing-time, not call count.** ~18 s of execution per 1-minute window,
   per user. Every response carries **`X-PROCESSING-TIME` (ms)** — reads cost ~10-15 ms, so the
   documented throttle is miles away; the bot-layer is the real limit. On **429**/**503** honor
   **`Retry-After`** (seconds).

## Tree search — `GET /platform/tree/search` (Accept atom+json)
Response: `results`, `entries[].id`, `entries[].score`, `entries[].content.gedcomx.persons[]`
(each with `display{name,lifespan,birthPlace,deathPlace}`).
- ✅ terms: `q.givenName`, `q.surname`, `q.sex`; `q.birthLikeDate/Place`, `q.deathLikeDate/Place`,
  `q.marriageLikePlace`, `q.residencePlace`; `q.anyDate`, `q.anyPlace`; `q.fatherGivenName`,
  `q.motherGivenName`, `q.parentGivenName`, `q.spouseGivenName/Surname`, `q.otherGivenName`;
  `.from`/`.to` ranges; `q.<name>.exact=on` **only when another non-name/non-year term is present**.
- ⛔ no child term (`q.childGivenName` 400), no `q.miscKeyword` (400 despite the docs), no `q.id`;
  dates must be `[+/-]YYYY[-MM[-DD]]` (no `~`); one value per term.
- **Wildcards work**: `q.givenName=Agued*&q.surname=Concei*`.
- ⚠⚠ **`q.*` terms SCORE, they do not FILTER** — adding terms barely moves `results` (stays in the
  millions). Read the top entries; never trust the count. To actually narrow, use **`f.*` filters**
  discovered from facets: add `m.defaultFacets=on` and read each facet's exact `params`. Real place
  filters are `f.birthLikePlace0` (continent) / `1` (`8,Brazil`) / `2` (`8,Brazil,Rio de Janeiro`);
  count facets stop at level 2. `offset+count < 5000`, `count ≤ 100`.
- ★ **Use it as a duplicate check before Add Child / Add Spouse** — stronger than the dialog's own
  check, which has missed spelling variants.

## Person & family — Accept x-fs-v1+json
- `/platform/tree/persons/{pid}` — full person + relationships + sourceDescriptions.
- `…/{pid}/families` | `/parents` | `/spouses` | `/children` — family in one call (`display` on each).
- `/platform/tree/ancestry?person=&generations=` and `…/descendancy?person=&generations=`.
- `…/{pid}/changes` (atom) — who edited, when: finds collaborators.
- `…/{pid}/notes`, `/sources`, `/matches` (204 = none). `/platform/records/search` is **404** —
  record search stays on `/service/search/hr/v2/personas`.
- ★ **Watch a profile cheaply:** keep the `ETag`, resend with `If-None-Match: <etag>` → **304**
  when unchanged, full body when a contributor edited it.

## Places — `GET /platform/places/search?q=` (atom+json) + `/description/{id}` (+`/children`)
`q` syntax: `name:"…"` (wildcards `*` `?`, not leading; `~` suffix = fuzzy), `partialName:` for
type-ahead, `+date:+YYYY/+YYYY` (signs on both ends), `+parentId:ID~` (descendants), `+typeId:`,
`latitude`/`longitude`/`distance`. Each result's `display.type` and `temporalDescription.formal`
(e.g. `+1857/`) give the valid window.
- ★ **This is the tool for "what was this place called on that date".** A municipality often has a
  start year; before it the records sit under the parent jurisdiction (worked example: a town that
  only became a município in 1857 was a *district of the neighbouring seat* before then — pre-1857
  records are filed under that seat). Historical and modern places can carry **different ids**.
- `/platform/places/types` (Accept `application/json`) lists the type vocabulary; `…/{id}/children`
  with a type filter finds a place's cemeteries / civil-registration districts.

## Dates — `GET /platform/dates?date=<text>` (Accept text/plain)
Returns the standardized form (`c. 1858` → `about 1858`). Check a date here before typing it into a
vitals dialog, since the dialog only saves a value it can standardize.

## Quick capability map
| Want | Call |
|---|---|
| duplicate check before creating a person | `tree/search` + `f.*` place filter |
| family / pedigree in one pull | `…/{pid}/families`, `ancestry`, `descendancy` |
| who else edits this family | `…/{pid}/changes` |
| notice when a profile changes | conditional GET with `If-None-Match` |
| what a place was called in year Y; its cemeteries/registries | `places/search`, `…/description/{id}/children` |
| standardize a date before saving | `platform/dates` |
| what a collection indexes | `records/collections/{id}` (`recordDescriptors`) |