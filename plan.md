# Plan: HYP3R00T Profile README Generator

**Status:** in-progress
**Last updated:** 2026-06-17

This document captures the architectural decisions for the rewrite of the
HYP3R00T GitHub profile README generator. Each decision follows the
Architecture Decision Record (ADR) shape: context, decision, consequences,
alternatives considered.

The plan is being negotiated iteratively. Decisions marked **ACCEPTED** are
locked. The "Open decisions" section at the bottom lists items still under
discussion.

---

## D1 — Project objective

**Status:** ACCEPTED

**Context.** The repo *is* the user's GitHub profile. The Python project
generates `README.md` from `config.yaml` via Jinja2 templates, fetching
live content (RSS, YouTube API) for time-sensitive sections. A daily
GitHub Actions cron plus a push-to-main trigger re-runs the generator
and commits the result. The user-facing purpose is to eliminate the
manual upkeep of keeping the profile's blog-roll and video-roll current.

**Decision.** Keep the existing model: declarative YAML config → render
→ write README → CI regenerates. We're not replacing it; we're improving
its structure so it scales as new block types are added.

**Consequences.** All downstream decisions stay within the existing
Python + Jinja2 + GitHub Actions stack. The repo continues to be both
the source and the artifact.

---

## D2 — Drop CLI subcommands

**Status:** ACCEPTED

**Context.** The original `src/main.py` had a single `main()` function;
there was no CLI. The script does one job: load config, render, write
README.

**Decision.** The entry point is `python -m hyp3r00t` only. No argparse,
no subcommands. Bad config raises and the CI run fails.

**Alternatives considered.** A CLI with `build` / `validate` /
`list-blocks` subcommands. Rejected because the script has one job;
adding subcommands is ceremony for ceremony's sake. Validation happens
implicitly at render time — if you want a "validate-only" workflow step,
the script itself reports the error on its own run.

**Consequences.** No `validate` or `list-blocks` subcommand. The script
fails loudly on bad config; CI catches it.

---

## D3 — Code / data separation

**Status:** ACCEPTED

**Context.** The repo currently has confusing directory structure:
`src/` holds Python, `blocks/` holds sample content, `templates/` holds
Jinja templates, `src/blocks/` holds more Python. Two directories named
`blocks/`. A forker who wants to personalize the README has to figure
out which of these to edit.

**Decision.** Split the repo into two layers:

- **Code layer** — `src/hyp3r00t/`. The Python package, including the
  block logic.
- **Data layer** — repo root. `config.yaml`, `content/*.md` (user-authored
  markdown snippets), `assets/*` (images, gifs).

A forker should be able to personalize the profile by editing only the
data layer.

**Alternatives considered.** Keeping all data inside the package
(under `src/hyp3r00t/`). Rejected because it couples personalization to
code edits.

**Consequences.** The package never reads user-authored markdown from
inside itself; it reads from the repo root. Block `path:` values in
`config.yaml` point at repo-root paths like `./content/about.md`.

---

## D4 — Static block shape

**Status:** ACCEPTED

**Context.** Two block kinds exist: **static** (just markdown, inlined
verbatim) and **dynamic** (fetcher + template, regenerated on each
run). The simplest block is the static one — a `.md` file that gets
copy-pasted into the README at the position `order:` specifies.

**Decision.** Static blocks (`about`, `banner`, `badges`, `social`,
`custom`) do NOT get their own directories in `src/hyp3r00t/blocks/`.
The "logic" of a static block is just "read the path the config points
at, or take inline content, and inline it verbatim". That logic is
shared in the renderer.

**Alternatives considered.** Directory per block always (uniform
structure). Rejected because static blocks don't need any boilerplate —
a `__init__.py` + `template.md` pair to render `{{ content }}` is
over-engineering for the trivial case.

**Consequences.** `src/hyp3r00t/blocks/` only contains directories for
dynamic blocks. Static block data lives at repo root under `content/`.

---

## D5 — Block disable mechanism

**Status:** ACCEPTED

**Context.** Some sections of the README should be optional. The
current `config.yaml` shows the pattern: most sections are commented
out with `#`, leaving only `about` enabled.

**Decision.** A block instance is disabled by commenting out its line
in `order:` in `config.yaml`. No separate `enabled:` flag.

**Alternatives considered.** An `enabled: true/false` flag per instance.
Rejected because YAML comment-out is the existing convention, requires
no extra field, and keeps the toggle visible in the same line as the
block reference.

**Consequences.** Matches the existing pattern in `config.yaml`. One
place to toggle visibility — the `order:` list.

---

## D6 — Explicit `order:` list in `config.yaml`

**Status:** ACCEPTED

**Context.** The original `config.yaml` relied on Python 3.7+ dict
iteration order to determine block sequence. Reordering required moving
YAML keys around; commenting out a middle block silently shifted
subsequent blocks up. The sequence was invisible without reading the
file linearly.

**Decision.** `config.yaml` has an explicit top-level `order:` list that
declares the sequence of block instances. Per-instance settings live
under their own top-level keys below.

**Alternatives considered.**

- *Implicit YAML key order* (current state) — rejected; fragile and
  invisible.
- *Separate `layout.yaml` for order only* — rejected; two files to keep
  in sync for no real win on a one-person project.
- *Filename-prefix in `blocks/` directory* (e.g. `01-banner.md`) —
  rejected; forces `git mv` to reorder.

**Consequences.** Sequence is visible at a glance when opening the file.
Reordering = edit the list. Disabling = comment out a line. Two clearly
separated concerns: order in `order:`, data in the per-instance keys.

---

## D7 — Central block-type registry in code

**Status:** ACCEPTED

**Context.** Blocks need to be discoverable by name. When the runtime
sees `- blog/personal` in `order:`, it needs to find the fetcher and
template for the `blog` type. The mapping from type name to behavior
must live somewhere.

**Decision.** The central registry is a dict in
`src/hyp3r00t/blocks/__init__.py` mapping `type_name → TypeSpec`. Each
TypeSpec has a fetcher (or `None` for static) and a template path.
Adding a block type = new directory under `src/hyp3r00t/blocks/` + one
entry in the registry.

**Alternatives considered.**

- *Filesystem auto-discovery* (scan `blocks/`, infer block type from
  shape) — rejected; implicit filesystem conventions are fragile and
  the static-vs-dynamic distinction gets fuzzy.
- *Decorator self-registration* (`@register_block("blog")`) — rejected;
  still requires an explicit import somewhere, so it's the registry in
  disguise with extra steps.

**Consequences.** Block catalog is visible in one file. No magic, no
filesystem conventions to remember. Adding a type is one extra line in
a dict.

---

## D8 — Instance model: multiple instances per type

**Status:** ACCEPTED

**Context.** Today the system has singletons (one `blog`, one `youtube`,
one `about`). Real use cases need multiple instances of the same type:
two RSS feeds (your blog + a team blog), multiple `custom` sections at
different positions (awards, speaking, books), etc. The OO framing:
**types** are the class catalog; **instances** are concrete uses of
those types.

**Decision.** Distinguish **types** (the catalog, in code) from
**instances** (concrete uses, in `config.yaml`). Each instance has an
ID in `<type>/<instance>` form, even for singletons. The type prefix
maps to the central registry; the settings live under the full ID key.

Example:

```yaml
order:
  - about/main
  - badges/main
  - blog/personal
  - blog/team
  - custom/awards
  - custom/speaking

about/main:
  path: ./content/about.md

blog/personal:
  rss_url: https://rajeshdas.dev/rss.xml
  max_posts: 5

blog/team:
  rss_url: https://team-blog.example/rss.xml
  max_posts: 3

custom/awards:
  content: |
    ## Awards
    ...
```

**Alternatives considered.**

- *Bare IDs with `type:` field per instance* — rejected; the `type:`
  field is metadata the user has to remember to set on every instance
  and is invisible in the `order:` list.
- *Bare IDs with implicit singleton convention* — rejected; inconsistent
  (singletons have bare names, multi-instance types have prefixes), and
  forces renaming when going from 1 to 2 instances.

**Consequences.** Unlimited instances per type. Order list is
self-documenting (the type prefix is visible in each ID). Adding a
second instance of an existing type is one new entry, no code changes.

---

## Open decisions

These have not been finalized yet:

- **Templates/ directory fate** — keep `templates/` separate vs.
  co-locate with blocks vs. drop Jinja.
- **`schema/config.schema.json` fate** — keep as docs vs. delete vs.
  regenerate from code.
- **CI workflow changes** — `git add README.md` fix, validate step,
  fetch caching, trigger strategy.
- **Cleanup list** — which existing files (`src/main.py`, `src/utils.py`,
  `src/blocks/__init__.py`, etc.) to delete.
- **Tests strategy** — smoke test, unit tests, CI integration.
