---
name: "genealogy-partner-sites"
description: "Search FamilySearch's partner sites from their free public pages, with no account and no subscription — Ancestry, MyHeritage, Findmypast, Filae, Geneanet, Storied, American Ancestors, NewspaperArchive and Portuguese tombo.pt. Covers what each one shows for free, hand-built and tested URL recipes, measured coverage for Brazil, Portugal and Italy, and how to get back from a partner hit to a free image. This never signs up, signs in, starts a trial, enters personal data, pays, or solves a CAPTCHA. Use to find out whether a partner holds anything on a name before deciding a subscription is worth activating."
---

# Partner sites without an account

FamilySearch lists eight partners at `/en/access/member-subscriptions` (Ancestry, MyHeritage, Storied,
NewspaperArchive, Findmypast, American Ancestors, Filae, Geneanet). The eligibility line reads
*"Members of The Church of Jesus Christ of Latter-day Saints can subscribe at no cost"*; DNA kits are
excluded. The Church-account gate sits behind each **JOIN FOR FREE** button.

⛔ This skill never signs up, signs in, starts a trial, enters personal data, pays, or solves a CAPTCHA.
Creating an account needs the person's explicit go-ahead and their own password entry. Search only for
**deceased** people. On cookie banners choose the most privacy-preserving option; if a site offers only
"agree", stop and tell the person.

Every tree hit is a lead, never evidence — several cite "FamilySearch Family Tree" as their source and
are circular. Judge identity on spouse and parents, then prove it from the act.

## 1. What works with no account

| Site | Anonymous search | Free | Locked |
|---|---|---|---|
| **Geneanet** | ✅ + free tree pages | name, spouse, years and places, tree owner; **tree page: parents, siblings, grandparents, exact dates, notes, sources, inconsistency flags** | spelling variants, radius search, messaging owners |
| **Ancestry.com** | ✅ | name, collection, event type; **image id `FS_<DGS>_<frame>`** | dates/places/relatives masked `xxxx`; record pages paywalled |
| MyHeritage | ⛔ hCaptcha "Security check" | — | the person must try it by hand |
| Findmypast | ⛔ redirects to login | — | — |
| Storied | ⛔ "Page Not Found" logged out | — | — |
| Filae | ✅ | name, years, event; relatives masked | details |
| Geni | ✅ public profiles | lifespan, named relatives (living hidden) | — |
| American Ancestors | ✅ | name, database, volume/page | images |
| tombo.pt (Portugal) | ✅ finding aid | every digitised parish book with dates and Digitarq links | not name-indexed |
| Digitarq (Portugal) | ⚠ accept-only cookie notice | — | ask the person to open it |

## 2. URL recipes (all built by hand and tested)

**Geneanet search**
`https://en.geneanet.org/fonds/individus/?go=1&nom=<SURNAME>&prenom=<GIVEN>&size=50`
+ `&country__0__=BRA|PRT|ITA` · `&place__0__=Genzano+di+Lucania` · `&type_periode=birth_between&from=1770&to=1780` · `&page=N`.
The form also takes father/mother/spouse names (`nom_pere`, `prenom_pere`, `nom_mere`, `prenom_mere`,
`nom_conjoint`, `prenom_conjoint`). Read results with `get_page_text` after ~7 s: each hit shows
name, spouse, owner ("Family tree of <owner>"), years and places.

**Geneanet tree person — take the link, don't build it.** The pattern is
`https://gw.geneanet.org/<owner>?lang=en&n=<surname+words>&p=<given+words>[&oc=N]`, but guessed
URLs fail on accents, compound surnames (*"Custódia de Oliveira"* vs *"de Oliveira"*) and the `oc`
homonym counter ("Individual not found"). Collect the real links from the results page:

```js
[...new Set([...document.querySelectorAll('a[href*="gw.geneanet.org"]')].map(a=>a.href))]
  .join(' ').replace(/[?&=]/g,' _ ')
```

Not every hit exposes a link; when one is missing, open the spouse's page and follow the link from
there. A Cloudflare check runs first and passes on its own after ~6–8 s.

**Ancestry search:** `https://www.ancestry.com/search/?name=<Given>_<Surname>&birth=<YYYY>_<place-slug>&death=<YYYY>_<place-slug>&count=50`
(place slug like `niteroi-rio+de+janeiro-brazil`). One collection, exact surname:
`/search/collections/<dbid>/?name=_<Surname>&name_x=_1` — `9799` = Rio de Janeiro civil registration,
`1030` = public member trees. `&keyword=` is too loose to use.

★ **Back to free images:** an Ancestry image id `FS_004349458_01931` opens on FamilySearch at
`https://www.familysearch.org/search/film/004349458?i=1930` (i = frame − 1). Ancestry's Brazilian and
Portuguese collections are mostly FamilySearch mirrors, so a masked hit can be read for free.

★ **Masks keep word lengths.** Ancestry and Filae draw each hidden word with the same number of `x`s,
so `xxxx xxxxx xx xxxxxxx` can be tested against *João Alves de Rezende*. A filter, never evidence.

**Filae:** `https://www.filae.com/search?ln=<surname>&fn=<given>&sy=<from>&ey=<to>&ps=50` (+ `ffn/fln`,
`mfn/mln`, `pfn/pln` for father, mother, partner).
**Geni:** `https://www.geni.com/search?search_type=people&names=<full+name>`.
**American Ancestors:** `https://www.americanancestors.org/search/database-search?lastname=<x>&firstname=<y>`.
**tombo.pt:** `/d/<district>` → `/m/<municipality>` → `/f/<parish>`; each book links to
`digitarq.arquivos.pt/fileViewer/<id>`.

## 3. Coverage for Brazil, Portugal and Italy (measured)

- **Geneanet** is the only partner with real hits for this kind of family: deep Minas Gerais founder
  lines, Minho (Portugal) lines, and pre-1809 Genzano baptism dates in one tree.
- **Ancestry**: Brazil and Portugal holdings are mostly FamilySearch mirrors; no Basilicata civil records.
- Findmypast, American Ancestors, Storied, Filae: nothing for Rio de Janeiro, São Paulo, Minas Gerais,
  Basilicata or northern Portugal.
- NewspaperArchive has its own skill (`newspaperarchive-search`); its Brazilian holding is two papers.

## 4. Method

1. Run Geneanet first, filtered by country and a birth window; also run the **spouse's** name — a
   couple is often findable from one side only.
2. Open the tree pages of hits whose spouse matches (via collected links, §2).
3. Note what the tree adds (parents, exact dates, places, grandparents) and what it cites.
   - Cites only "FamilySearch Family Tree" → circular. It may preserve an **older state** of the
     FamilySearch tree: useful for *where* and for tracing when an error entered, not for dates.
   - ★ Geneanet prints **"Inconsistencies"** at the top of a person page (e.g. *"Was '4 years old' at
     date of marriage"*). A free sign that the tree copied a bad date.
4. For each claim, find the primary record: FamilySearch catalog/images, or tombo.pt → Digitarq for
   Portuguese parishes.
5. Ancestry: use it to discover which FamilySearch film/frame holds a record (the `FS_` id), then read
   it on FamilySearch.
6. Log every lead with its exact URL, and every rejection with its reason (wrong spouse, wrong parish,
   impossible dates, famous namesake).

## 5. Worked leads

- Geneanet `frida63` took Capitão João Pereira da Rocha (b. 1774 Itabirito) two generations into
  Portugal — father b. 16 Apr 1745 at Paço Vedro de Magalhães, Ponte da Barca — and tombo.pt showed
  that parish's 1729–1777 baptism book is online at Digitarq.
- Geneanet `sertanista` gave Manoel Lino de Rezende's grandparents and brothers, but a different birth
  year and wedding farm from the 1858 marriage act. The act wins.
- Ancestry's "Paulino José Soares, marriage, Niterói" resolved via the `FS_` id to a namesake
  (married 1895 to someone else). Not attached.
- ★ 13 Nov 2026: a search on Maria Custódia de Oliveira found only Pouso Alegre namesakes; the
  **husband's** search (José Lino Pereira, BRA) found `frida63`'s couple with the wedding at
  **"Faz Progresso, MS"**. The page cites only the FamilySearch tree and flags the groom as 4 at
  marriage — the date is junk — but the *place* moved the hunt from Minas Gerais to Mato Grosso, where
  the family had moved in 1880, after a full month of the wrong parish's register had been read.

## 6. Which to activate (if the person decides to)

1. **Geneanet** — real hits, and an account allows contacting tree owners about their sources.
2. **MyHeritage** — untested (CAPTCHA); worth one manual trial by the person first.
3. Ancestry — low priority for Brazil/Portugal/Italy; the `FS_` bridge already reaches the images.