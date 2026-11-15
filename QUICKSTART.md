# Quickstart — your first research session

For someone who has these skills installed and wants to start finding ancestors.
If you haven't installed them yet, see [README.md](README.md).

---

## 1. What you need

| | |
|---|---|
| **A free FamilySearch account** | familysearch.org. Everything here runs against the signed-in site. Claude will not create the account or enter your password — sign in yourself, in the browser Claude is driving. |
| **Claude with code execution on** | Settings → Capabilities → *Create and edit files*. Skills don't load without it. |
| **A browser Claude can drive** | Claude in Chrome, or the desktop app's built-in browser. These skills operate the live site; they are not web-search recipes. |
| **About two hours** | A first session that ends with one properly sourced fact is a good first session. |

**Scope.** The FamilySearch mechanics here work anywhere. The archive-specific
knowledge is Brazilian, Portuguese and Italian — see *What generalizes* in the README
before using this on another country.

---

## 2. Start from what you know, not from the internet

The most common way genealogy stalls is starting in the middle — picking a famous
surname, or an interesting 1700s person someone else's tree claims, and working outward
from a person you cannot connect to yourself.

Before the first search, write down, on paper:

- Your parents and grandparents: full names, including maiden names.
- For each: roughly when and where born, married, died. "Around 1935, somewhere near
  Barra Mansa" is a usable answer. A guess marked as a guess is fine; a guess recorded
  as a fact is the thing that poisons a tree.
- Which relatives are still alive and might know more. **Ask them first.** A living
  great-aunt outperforms every archive in this repo, and she will not be available
  indefinitely.
- Any documents in the house: certificates, a family bible, the back of a photograph,
  immigration papers, a funeral card.

Then find your known people in the FamilySearch tree, or create them. That is your
anchor. Everything the skills do extends outward from a person you are certain about.

---

## 3. Your first session

Open a chat with the browser connected, sign in to FamilySearch in it, and paste
something like this:

> I'm researching my family on FamilySearch. My grandfather was **[full name]**, born
> about **[year]** in **[town, state, country]**, married **[name]** around **[year]**.
> His FamilySearch PID is **[PID, if you have it]**.
>
> I want to find his parents and confirm them from an actual record image, not from
> another user's tree. Work one step at a time and show me what you find before you
> change anything in the tree. If a search comes back empty, prove the corpus is
> searchable before telling me the record doesn't exist.

That last sentence matters more than it looks. It invokes the rule the skills are built
around, and it is the difference between "no records exist" and "I searched badly."

---

## 4. The loop

One person, one question, one record type, every time:

1. **Pick the question.** Not "research my grandfather" — *"who were his parents?"* or
   *"when exactly did he die?"*
2. **Pick the record class that would answer it.** A marriage act names both sets of
   parents. A death record names the surviving spouse and often the children. A baptism
   names the parents and both sets of grandparents.
3. **Search.** Claude will load the right skill. Expect spelling variants to be tried —
   full-text matching is literal, so `Justyno` and `Justino` are different searches.
4. **Open the image.** An index entry or a hint is a lead. The image is the evidence.
   Read it, or have Claude read it to you with the original-language wording quoted.
5. **Record it properly.** Every fact attached to the tree gets a reason containing the
   original-language quotation and the record's ark URL. If you skip this, you will not
   be able to tell your conclusions from your assumptions in six months. Neither will
   anyone else.
6. **Log the negative.** "Searched Mococa marriages 1875–1890, control word confirmed
   present, no Moreira" is a durable result worth as much as a find. It stops the next
   session repeating the same month of work.

Then pick the next question.

---

## 5. Mistakes these skills exist to prevent

| Don't | Because |
|---|---|
| Accept a Record Hint without opening the record | The matcher used the name as its *input*. The name agreeing proves nothing. Check the other people named on the record. |
| Trust a zero result | Until a control word proves that corpus is searchable, an empty search means nothing at all. |
| Copy people in from another user's tree | Submitted trees are leads. Nothing from one belongs in your tree without a primary image. |
| Use a confidence score to decide | Two hints with identical scores can be one correct and one a different family. Use the score to order your reading only. |
| Read a place out of the catalogue path | `Niterói › Icaraí › Nascimentos` names the office that kept the book, not where the event happened. |
| Add anything about a living relative | Living people do not belong in a public tree, and ordinance work has hard boundaries. Establish your living boundary before you start. |

---

## 6. When you get stuck

Ask Claude to run the research audit:

> Audit where I've got to on this line. Which of my negatives are actually void?

That loads `genealogy-research-audit`, which starts by asking how many *distinct*
archives you have searched. Hundreds of searches against one platform ending in "this is
the edge of the archive" is usually the edge of that platform. There are nine checks and
they are ordered deliberately.
