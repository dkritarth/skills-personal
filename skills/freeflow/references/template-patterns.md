# FreeFlow draft layout patterns

Conventions for plan/dashboard-shaped HTML drafts. Not mandatory - a simple mockup or single-idea page doesn't need any of this. Pull individual patterns as needed; don't cargo-cult the whole set into a two-paragraph draft.

## Stack

Load everything from CDN, nothing local:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
<script src="https://unpkg.com/lucide@latest"></script>
```

Call `lucide.createIcons()` in a trailing `<script>` if any `<i data-lucide="...">` icons are used.

Base shell: `bg-slate-950 text-slate-100` dark canvas, `max-w-7xl` centered container, rounded-2xl bordered cards (`border-slate-800 bg-slate-900/80`) as the repeating unit for every section.

## Sticky table of contents

A `<aside class="sticky top-4 ... lg:block">` with anchor links (`href="#section-id"`) to each `<section id="section-id">` below. Hide below `lg` breakpoint (`hidden lg:block`) - mobile gets linear scroll instead.

## Status / metadata banner

Header card with title, a right-aligned pill showing generation time, and a row of small pill badges for metadata (author, mode, signal count, whatever's relevant). Pills: `rounded-full bg-slate-800 px-3 py-1 text-xs`.

## Progress meters

Card with a label, a big number/state, and a thin progress bar underneath:

```html
<div class="mt-3 h-2 rounded-full bg-slate-800">
  <div class="h-2 w-[78%] rounded-full bg-emerald-400"></div>
</div>
```

Vary the bar color by semantics: `emerald` for good/on-track, `cyan` for neutral/informational, `amber`/`red` for risk or blocked.

## Striped status tables

Standard `<table>` with `divide-y divide-slate-800`, header row `text-slate-400 uppercase text-xs`, body rows alternating `bg-slate-900/40` for zebra striping. Use for timelines, task lists, comparison rows - anything tabular.

## Nested progressive disclosure

Native `<details>/<summary>` blocks, styled (`rounded-xl border border-slate-800 p-4`), nested when a task has sub-tasks. No JS needed - browser handles expand/collapse natively. Prefer this over hand-rolled JS accordions.
