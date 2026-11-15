---
name: "familysearch-ordinance-requests"
description: "Walk a list of ancestors on FamilySearch, open each profile's Ordinances tab, and request the ordinances shown green and Ready. Reservation is a real action on the user's own account under FamilySearch's Reservation Policy, so this settles the scope and asks for consent once before any clicking, and applies the deceased, 110-year and living-relative checks first. Covers reading every ordinance row before touching anything, driving the reservation dialog, clicking FamilySearch's React UI reliably, and reporting what was reserved."
---

# Requesting FamilySearch ordinances, profile by profile

Opens each person's **Ordinances** tab and requests the ordinances FamilySearch shows as green
**Ready**. Ordinance reservation is a real action on the user's own account under FamilySearch's
**Reservation Policy**, so scope and consent come first and the clicking comes second.

> **Who this is for.** Temple ordinance reservation is available to members of The Church of
> Jesus Christ of Latter-day Saints, through a FamilySearch account linked to Church membership.
> If the user is not a member, the Ordinances tab offers nothing to request — say so once and
> stop, rather than working the list. Every other skill in this set is open to any
> FamilySearch account.

---

## 1. Settle the scope before opening a browser

**Never run this against "everyone in the tree".** Work from an explicit list.

Accept either:
- a list of PIDs the user gives, or
- a branch they name — expand it to PIDs yourself, then **show the list back** before acting.

Then drop anyone for whom **any** of these is true, and record why:

| Skip when | Why |
|---|---|
| not marked **Deceased** | living people have no ordinance data |
| **born within the last 110 years** and not a direct ancestor | FamilySearch requires the closest living relative's permission |
| at or below the living boundary the user set | see §2 |
| the relationship doesn't fit the Reservation Policy | the dialog makes the user attest that it does |
| ordinances are already Reserved / Shared with Temple / In Progress / Completed by anyone | not yours to request |

★ The skip list, with reasons, is **part of the deliverable** — not noise to swallow.

## 2. ⛔ The living boundary

Every tree has a generation below which nobody is a candidate, whatever FamilySearch's Deceased
flag says — a relative who is alive, or recently dead with living children who have the say.
**FamilySearch's own flags are not sufficient: a living person is sometimes recorded as deceased.**

**Establish the boundary before the run, from the user, and hold it:**

1. Ask the user to name the most recent generation that is in scope — by PID, or as "nobody at or
   below my grandparents".
2. Treat that person and **everyone descending from them** as out of scope. Nothing is created,
   edited, reserved or requested for them.
3. If a PID in the list falls below the line, **skip it and say so** in the skip list. Never
   quietly include it.
4. Keep no names in this file. The boundary belongs to the user's session, not to the skill.

## 3. Ask once, then run

Requesting is user-attributable and the modal footer makes them agree they are following the
Reservation Policy. So:

1. Print the final table — **name, PID, which ordinances are green** — plus the skip list.
2. Ask for **one explicit go-ahead**.
3. After that, work the whole list without stopping to re-ask.
4. Anything unexpected mid-run (an unfamiliar spouse on a sealing, a status you don't recognise):
   **skip it, log it, keep going.** Never guess.

## 4. Tools

Load the browser tools in a single call:

```
ToolSearch: select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__browser_batch,mcp__claude-in-chrome__javascript_tool
```

Call `tabs_context_mcp` first and work in one tab for the whole run.

## 5. Per person

```
https://www.familysearch.org/tree/person/details/{PID}
```

**Ordinances** is the last tab (About · Details · Sources · Collaborate · Memories · Time Line ·
Ordinances). Try `/tree/person/ordinances/{PID}` directly; if it doesn't resolve, click the tab.

### Read every row before touching anything

Six rows, each with a letter badge and a status:

| Badge | Ordinance |
|---|---|
| **B** | Baptism |
| **C** | Confirmation |
| **I** | Initiatory |
| **E** | Endowment |
| **SP** | Sealing to Parents |
| **SS** | Sealing to Spouse |

⚠ **Read the status word, not the colour.** A 0.65-scale screenshot is far too coarse to judge a
badge by hue. Zoom the row region, or pull the text with `javascript_tool`. Only the literal
status **Ready** is requestable.

### The dialog

- The **REQUEST** button at the top requests everything at once.
- Each row also has its **own REQUEST** link.

All six Ready → use the top button. Mixed → use the per-row links, or use the top button and
**untick** the rows that were not Ready.

The modal is titled **Request Family Names** and arrives with everything pre-ticked: the person,
then `B C`, `I`, `E`, `SP`, `SS`.

★★ **Check SP and SS before confirming.** The modal prints the **Parents** and **Spouse** it will
use, with their PIDs. If those are not the relationships you expect for this person, **untick that
box and log it** — a sealing attached to the wrong relationship is a wrong record, and the modal
is the only place it is shown.

Then click **REQUEST** and confirm the page comes back with the new status.

## 6. Clicking FamilySearch reliably

Hard-won and worth obeying:

- **Use real `left_click` at computed coordinates.** Synthetic `element.click()` is ignored by
  several FamilySearch controls.
- **The first click after a layout change often does nothing.** Re-screenshot and click again
  rather than assuming it worked.
- **Dialogs move as their content grows.** Never reuse a button coordinate from before you typed
  or ticked something — take a fresh screenshot and re-measure.
- **Verify after every state change.** Screenshot or re-read the row; don't infer success from the
  click returning.
- Checkbox mis-clicks are easy on dense rows — after ticking/unticking, **zoom and confirm** which
  boxes are actually checked before pressing REQUEST.

## 7. Report

Finish with one table:

| Person | PID | Requested | Skipped (reason) | Failed |
|---|---|---|---|---|

And state plainly how many requests were actually submitted. If the user wants to undo any of
them, reservations can be released from their own FamilySearch reservation list — say so rather
than attempting it unasked.