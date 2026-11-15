# Adding or changing a skill

## The shape

One folder per skill under `skills/`, containing `SKILL.md`:

```markdown
---
name: my-skill-name
description: "What it does, then when to use it. Trigger terms first."
---

# Title

Instructions.
```

Rules the upload enforces, so `make check` enforces them too:

- `name` must equal the folder name exactly, be 1–64 characters of lowercase letters,
  digits and hyphens, and contain neither "claude" nor "anthropic".
- `description` must be non-empty, at most 1024 characters, and free of angle brackets.
- Only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`
  are permitted in frontmatter. Claude Code accepts more fields; a claude.ai or Skills
  API upload **hard-errors** on any of them, so they stay out of this repo.

Run before every commit:

```bash
make check     # validate
make zips      # build dist/<skill>.zip, one per skill
```

## Never commit

**A living person's name, date of birth, or profile ID.** This is the easiest mistake to
make in genealogy and the hardest to undo — a public repo keeps it in history after you
delete the line. A skill must never hardcode one tree's living boundary; it asks the user
for theirs at the start of the run. `make check` warns on any vital date from 1930 on and
on bare PIDs in prose. Read every warning; don't clear them by loosening the pattern.

Deceased ancestors in worked examples are fine, and they are what make these skills
teachable. Record arks and film numbers are public identifiers and are fine.

## Writing a skill that works

**Describe for triggering.** The description is the only part Claude reads before
deciding to load the file. Put the capability and its trigger terms in the first
sentence; the rest can elaborate. "Use when…" clauses earn their space.

**Write what broke, not what should work.** The value in this repo is the traps — the
field that accepts a programmatic value and saves nothing, the filter that silently does
nothing, the index that spells a surname three ways. A skill that only describes the
happy path is a manual, and Claude does not need a manual.

**Date every measurement.** Coverage counts, test logs and "this returned N hits" go
stale. Put the month in the heading so the next reader knows what they are trusting. Say
what to re-run instead of trusting it.

**Say what the skill will not do.** The ordinance and partner-site skills both state
their boundaries — no sign-ups, no credentials, no CAPTCHAs, consent before any action
attributable to the user. Those lines are load-bearing.

**One skill, one job.** If two skills would answer the same request, one should say which
to prefer, or they should be merged. Two competing descriptions make the choice worse,
not better.
