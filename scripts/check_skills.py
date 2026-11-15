#!/usr/bin/env python3
"""Validate every skill in skills/ before upload.

Checks the things that actually make a claude.ai upload fail, plus a privacy
lint for the mistake that is easiest to make in genealogy: committing a living
relative's name and date of birth.

    python3 scripts/check_skills.py      # or: make check
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")

# Fields the Agent Skills spec allows for a claude.ai / Skills API upload.
# Anything else is a hard error on upload, not a warning.
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}

MONTHS = ("jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
          "|january|february|march|april|june|july|august|september|october|november|december")
# A vital-event marker and a year from 1930 on, on the same line: possible living person.
LIVING = re.compile(
    r"(?:\bb\.|\bborn\b|\bd\.|\bdied\b|\bdob\b|†|\bb:\s)"
    r"[^\n]{0,40}?"
    r"(?:(?:" + MONTHS + r")[^\n]{0,12}?)?"
    r"\b(19[3-9]\d|20[0-2]\d)\b",
    re.I,
)
# A bare person PID in prose. Record and image arks (1:1:, 3:1:, and the
# three-segment forms) are public record identifiers, not people, so they are excluded.
PID = re.compile(r"(?<![:\-\w])([A-Z0-9]{4}-[A-Z0-9]{3,4})(?![\-\w])")
ARK_CONTEXT = re.compile(r"\d:1:|groupIds|artifactArks|imageApids|\bDGS\b|\bapid\b", re.I)

errors, warnings = [], []


def frontmatter(text):
    m = re.match(r"^---\n(.*?\n)---\n(.*)", text, re.S)
    if not m:
        return None, None
    fields, order = {}, []
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km:
            key = km.group(1)
            fields[key] = km.group(2).strip()
            order.append(key)
        elif key and line.startswith((" ", "\t")):
            fields[key] += " " + line.strip()
    return fields, m.group(2)


def unquote(s):
    if len(s) > 1 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    return s.replace('\\"', '"').replace("\\'", "'")


def main():
    if not os.path.isdir(ROOT):
        print(f"no skills/ directory at {ROOT}")
        return 1

    slugs = sorted(d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d)))
    if not slugs:
        print("skills/ is empty")
        return 1

    for slug in slugs:
        path = os.path.join(ROOT, slug, "SKILL.md")
        label = f"skills/{slug}"

        if not os.path.isfile(path):
            errors.append(f"{label}: no SKILL.md")
            continue

        text = open(path, encoding="utf-8").read()
        fields, body = frontmatter(text)

        if fields is None:
            errors.append(f"{label}: SKILL.md must open with a --- frontmatter block on line 1")
            continue

        name = unquote(fields.get("name", ""))
        desc = unquote(fields.get("description", ""))

        if not name:
            errors.append(f"{label}: frontmatter has no name")
        elif name != slug:
            errors.append(f"{label}: name '{name}' must equal the folder name '{slug}'")

        if not re.fullmatch(r"[a-z0-9-]{1,64}", name or ""):
            errors.append(f"{label}: name must be 1-64 chars of lowercase letters, digits, hyphens")
        if "claude" in name.lower() or "anthropic" in name.lower():
            errors.append(f"{label}: name may not contain 'claude' or 'anthropic'")

        if not desc:
            errors.append(f"{label}: frontmatter has no description")
        elif len(desc) > 1024:
            errors.append(f"{label}: description is {len(desc)} chars, limit 1024")
        elif len(desc) < 80:
            warnings.append(f"{label}: description is only {len(desc)} chars — thin for triggering")

        if "<" in desc or ">" in desc:
            errors.append(f"{label}: description may not contain angle brackets")

        extra = set(fields) - ALLOWED
        if extra:
            errors.append(f"{label}: frontmatter field(s) not allowed on upload: {sorted(extra)}")

        if not (body or "").strip():
            errors.append(f"{label}: SKILL.md has frontmatter but no instructions")

        for n, line in enumerate(text.splitlines(), 1):
            if LIVING.search(line):
                warnings.append(f"{label}:{n}: vital date from 1930 on — living person? {line.strip()[:70]}")
            if not ARK_CONTEXT.search(line):
                for pid in PID.findall(line):
                    warnings.append(f"{label}:{n}: bare FamilySearch PID in prose: {pid}")

    for w in warnings:
        print(f"warn   {w}")
    for e in errors:
        print(f"ERROR  {e}")

    print(f"\n{len(slugs)} skill(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    if errors:
        print("Fix the errors — an upload will reject these.")
        return 1
    if warnings:
        print("Warnings are judgement calls. Check each before publishing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
